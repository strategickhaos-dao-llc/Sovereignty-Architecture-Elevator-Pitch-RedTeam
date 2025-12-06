"""
Trading Arsenal - Data Service
Handles market data ingestion from Polygon and Coingecko
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

import pandas as pd
import numpy as np
import aiohttp


logger = logging.getLogger(__name__)


@dataclass
class DataConfig:
    """Data service configuration"""
    polygon_api_key: str = ""
    coingecko_api_key: str = ""
    data_dir: Path = field(default_factory=lambda: Path("/var/trading/data"))
    cache_ttl_minutes: int = 15
    rate_limit_calls_per_min: int = 5
    

@dataclass
class OHLCVBar:
    """Single OHLCV bar"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    symbol: str
    source: str = "polygon"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "symbol": self.symbol,
            "source": self.source
        }


class DataCache:
    """In-memory cache for market data"""
    
    def __init__(self, ttl_minutes: int = 15):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl = timedelta(minutes=ttl_minutes)
    
    def get(self, key: str) -> Optional[pd.DataFrame]:
        """Get cached data if not expired"""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        if datetime.now(timezone.utc) - entry["timestamp"] > self._ttl:
            del self._cache[key]
            return None
        
        return entry["data"]
    
    def set(self, key: str, data: pd.DataFrame) -> None:
        """Cache data with timestamp"""
        self._cache[key] = {
            "data": data,
            "timestamp": datetime.now(timezone.utc)
        }
    
    def clear(self) -> None:
        """Clear all cached data"""
        self._cache.clear()


class PolygonDataProvider:
    """Polygon.io data provider for stocks"""
    
    BASE_URL = "https://api.polygon.io"
    
    def __init__(self, api_key: str, rate_limit: int = 5):
        self.api_key = api_key
        self.rate_limit = rate_limit
        self._last_call = datetime.now(timezone.utc)
        self._call_count = 0
    
    async def _rate_limit(self) -> None:
        """Simple rate limiting"""
        now = datetime.now(timezone.utc)
        if (now - self._last_call).total_seconds() >= 60:
            self._call_count = 0
            self._last_call = now
        
        if self._call_count >= self.rate_limit:
            wait_time = 60 - (now - self._last_call).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(wait_time)
            self._call_count = 0
            self._last_call = datetime.now(timezone.utc)
        
        self._call_count += 1
    
    async def get_bars(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        timeframe: str = "day"
    ) -> List[OHLCVBar]:
        """Fetch OHLCV bars from Polygon"""
        await self._rate_limit()
        
        url = f"{self.BASE_URL}/v2/aggs/ticker/{symbol}/range/1/{timeframe}/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
        params = {"apiKey": self.api_key, "adjusted": "true", "sort": "asc", "limit": 50000}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        logger.error(f"Polygon API error: {response.status}")
                        return []
                    
                    data = await response.json()
                    results = data.get("results", [])
                    
                    bars = []
                    for bar in results:
                        bars.append(OHLCVBar(
                            timestamp=datetime.fromtimestamp(bar["t"] / 1000, tz=timezone.utc),
                            open=bar["o"],
                            high=bar["h"],
                            low=bar["l"],
                            close=bar["c"],
                            volume=bar["v"],
                            symbol=symbol,
                            source="polygon"
                        ))
                    
                    return bars
                    
        except Exception as e:
            logger.error(f"Error fetching Polygon data for {symbol}: {e}")
            return []
    
    async def get_tickers(self, market: str = "stocks") -> List[str]:
        """Get available tickers"""
        await self._rate_limit()
        
        url = f"{self.BASE_URL}/v3/reference/tickers"
        params = {"apiKey": self.api_key, "market": market, "active": "true", "limit": 1000}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        return []
                    
                    data = await response.json()
                    return [t["ticker"] for t in data.get("results", [])]
                    
        except Exception as e:
            logger.error(f"Error fetching Polygon tickers: {e}")
            return []


class CoingeckoDataProvider:
    """Coingecko data provider for crypto"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    PRO_BASE_URL = "https://pro-api.coingecko.com/api/v3"
    
    def __init__(self, api_key: str = "", rate_limit: int = 10):
        self.api_key = api_key
        self.rate_limit = rate_limit
        self.base_url = self.PRO_BASE_URL if api_key else self.BASE_URL
        self._last_call = datetime.now(timezone.utc)
        self._call_count = 0
    
    async def _rate_limit(self) -> None:
        """Rate limiting for API calls"""
        now = datetime.now(timezone.utc)
        if (now - self._last_call).total_seconds() >= 60:
            self._call_count = 0
            self._last_call = now
        
        if self._call_count >= self.rate_limit:
            wait_time = 60 - (now - self._last_call).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(wait_time)
            self._call_count = 0
            self._last_call = datetime.now(timezone.utc)
        
        self._call_count += 1
    
    async def get_historical(
        self,
        coin_id: str,
        days: int = 365,
        vs_currency: str = "usd"
    ) -> List[OHLCVBar]:
        """Fetch historical OHLC data"""
        await self._rate_limit()
        
        url = f"{self.base_url}/coins/{coin_id}/ohlc"
        params = {"vs_currency": vs_currency, "days": str(days)}
        headers = {"x-cg-pro-api-key": self.api_key} if self.api_key else {}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status != 200:
                        logger.error(f"Coingecko API error: {response.status}")
                        return []
                    
                    data = await response.json()
                    
                    bars = []
                    for candle in data:
                        timestamp, o, h, l, c = candle
                        bars.append(OHLCVBar(
                            timestamp=datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc),
                            open=o,
                            high=h,
                            low=l,
                            close=c,
                            volume=0.0,  # OHLC endpoint doesn't include volume
                            symbol=coin_id.upper(),
                            source="coingecko"
                        ))
                    
                    return bars
                    
        except Exception as e:
            logger.error(f"Error fetching Coingecko data for {coin_id}: {e}")
            return []
    
    async def get_top_coins(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get top coins by market cap"""
        await self._rate_limit()
        
        url = f"{self.base_url}/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": str(limit),
            "page": "1",
            "sparkline": "false"
        }
        headers = {"x-cg-pro-api-key": self.api_key} if self.api_key else {}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status != 200:
                        return []
                    
                    return await response.json()
                    
        except Exception as e:
            logger.error(f"Error fetching top coins: {e}")
            return []


class DataService:
    """Main data service orchestrating all data providers"""
    
    def __init__(self, config: DataConfig):
        self.config = config
        self.cache = DataCache(config.cache_ttl_minutes)
        self.polygon = PolygonDataProvider(config.polygon_api_key, config.rate_limit_calls_per_min)
        self.coingecko = CoingeckoDataProvider(config.coingecko_api_key)
        
        # Ensure data directory exists
        config.data_dir.mkdir(parents=True, exist_ok=True)
    
    async def get_market_data(
        self,
        symbols: List[str],
        asset_class: str = "equity",
        lookback_days: int = 365
    ) -> pd.DataFrame:
        """Get market data for multiple symbols"""
        cache_key = f"{asset_class}:{':'.join(sorted(symbols))}:{lookback_days}"
        
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached
        
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=lookback_days)
        
        all_bars = []
        
        if asset_class == "equity":
            for symbol in symbols:
                bars = await self.polygon.get_bars(symbol, start_date, end_date)
                all_bars.extend(bars)
        elif asset_class == "crypto":
            for symbol in symbols:
                bars = await self.coingecko.get_historical(symbol.lower(), days=lookback_days)
                all_bars.extend(bars)
        
        if not all_bars:
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame([bar.to_dict() for bar in all_bars])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        self.cache.set(cache_key, df)
        
        return df
    
    async def save_to_parquet(self, df: pd.DataFrame, filename: str) -> Path:
        """Save DataFrame to Parquet format"""
        filepath = self.config.data_dir / f"{filename}.parquet"
        df.to_parquet(filepath, engine='pyarrow', compression='snappy')
        logger.info(f"Saved data to {filepath}")
        return filepath
    
    async def load_from_parquet(self, filename: str) -> Optional[pd.DataFrame]:
        """Load DataFrame from Parquet"""
        filepath = self.config.data_dir / f"{filename}.parquet"
        if not filepath.exists():
            return None
        
        return pd.read_parquet(filepath)
    
    def get_universe(self, tier: str = "tier_0") -> Dict[str, List[str]]:
        """Get trading universe based on tier"""
        universes = {
            "tier_0": {
                "equity": [
                    "SPY", "QQQ", "IWM", "DIA",  # Major indices
                    "XLK", "XLF", "XLE", "XLV", "XLI", "XLU", "XLP", "XLB", "XLY",  # Sectors
                    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA"  # Top tech
                ],
                "crypto": [
                    "bitcoin", "ethereum", "solana", "cardano"
                ]
            },
            "tier_1": {
                "equity": [
                    "VTI", "VEA", "VWO", "BND", "TLT", "GLD", "SLV"
                ],
                "crypto": [
                    "polkadot", "avalanche-2", "chainlink", "uniswap"
                ]
            }
        }
        
        return universes.get(tier, universes["tier_0"])
    
    async def health_check(self) -> Dict[str, Any]:
        """Check data service health"""
        status = {
            "polygon_configured": bool(self.config.polygon_api_key),
            "coingecko_configured": bool(self.config.coingecko_api_key),
            "data_dir_exists": self.config.data_dir.exists(),
            "cache_size": len(self.cache._cache),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return status
