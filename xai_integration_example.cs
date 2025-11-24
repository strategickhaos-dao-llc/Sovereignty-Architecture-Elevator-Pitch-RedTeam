// StrategicKhaos XAI Integration Example
// Complete cTrader bot with XAI integration

using System;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using cAlgo.API;
using cAlgo.API.Indicators;
using cAlgo.API.Internals;

namespace cAlgo.Robots
{
    [Robot(TimeZone = TimeZones.UTC, AccessRights = AccessRights.FullAccess)]
    public class PidRancoXaiBot : Robot
    {
        #region Parameters
        
        // Trading Parameters
        [Parameter("Position Size (lots)", DefaultValue = 0.1)]
        public double PositionSize { get; set; }
        
        [Parameter("Stop Loss (pips)", DefaultValue = 50)]
        public int StopLossPips { get; set; }
        
        [Parameter("Take Profit (pips)", DefaultValue = 100)]
        public int TakeProfitPips { get; set; }
        
        // herLove Parameters
        [Parameter("herLove Base Level", DefaultValue = 75)]
        public double HerLoveBase { get; set; }
        
        [Parameter("herLove Sensitivity", DefaultValue = 0.5)]
        public double HerLoveSensitivity { get; set; }
        
        // XAI Parameters
        [Parameter("XAI Enabled", DefaultValue = true)]
        public bool XaiEnabled { get; set; }
        
        [Parameter("XAI Service URL", DefaultValue = "http://localhost:5000")]
        public string XaiServiceUrl { get; set; }
        
        [Parameter("XAI Timeout (seconds)", DefaultValue = 5)]
        public int XaiTimeoutSeconds { get; set; }
        
        [Parameter("XAI Verbose Logging", DefaultValue = true)]
        public bool XaiVerbose { get; set; }
        
        #endregion
        
        #region Private Fields
        
        private HttpClient xaiClient;
        private RelativeStrengthIndex rsi;
        private ExponentialMovingAverage ema21;
        private int sessionLossCount = 0;
        private double sessionStartBalance;
        private double currentHerLove;
        
        #endregion
        
        #region Robot Lifecycle
        
        protected override void OnStart()
        {
            Print("╔══════════════════════════════════════════════════════════╗");
            Print("║   StrategicKhaos PID-RANCO v1.2 + XAI Integration        ║");
            Print("║   The First Trading Bot That Reads Market's Mind         ║");
            Print("╚══════════════════════════════════════════════════════════╝");
            
            // Initialize indicators
            rsi = Indicators.RelativeStrengthIndex(Bars.ClosePrices, 14);
            ema21 = Indicators.ExponentialMovingAverage(Bars.ClosePrices, 21);
            
            // Initialize session tracking
            sessionStartBalance = Account.Balance;
            currentHerLove = HerLoveBase;
            
            // Initialize XAI client
            InitializeXaiClient();
            
            Print($"Bot initialized. XAI: {(XaiEnabled ? "ACTIVE" : "DISABLED")}");
            Print($"Initial herLove: {currentHerLove:F0}");
        }
        
        protected override void OnBar()
        {
            // Update herLove based on performance
            UpdateHerLove();
            
            // Check for trading signals
            CheckForSignals();
        }
        
        protected override void OnStop()
        {
            Print("Bot stopped. Session summary:");
            Print($"Final Balance: {Account.Balance:C}");
            Print($"Session P&L: {(Account.Balance - sessionStartBalance):C}");
            Print($"Final herLove: {currentHerLove:F0}");
            
            xaiClient?.Dispose();
        }
        
        #endregion
        
        #region Trading Logic
        
        private void CheckForSignals()
        {
            // Don't trade if already in position
            if (Positions.Count > 0)
                return;
            
            // Get current indicators
            double currentRsi = rsi.Result.LastValue;
            double currentPrice = Symbol.Bid;
            double ema21Value = ema21.Result.LastValue;
            
            // Long signal: RSI oversold + price below EMA + herLove sufficient
            if (currentRsi < 30 && currentPrice < ema21Value && currentHerLove > 50)
            {
                ConsiderTrade("ENTER_LONG", TradeType.Buy);
            }
            // Short signal: RSI overbought + price above EMA + herLove sufficient
            else if (currentRsi > 70 && currentPrice > ema21Value && currentHerLove > 50)
            {
                ConsiderTrade("ENTER_SHORT", TradeType.Sell);
            }
        }
        
        private async void ConsiderTrade(string decision, TradeType tradeType)
        {
            Print($"─────────────────────────────────────────────────────────");
            Print($"Trade Signal: {decision}");
            Print($"Current herLove: {currentHerLove:F0}");
            
            // Ask XAI for analysis and approval
            bool shouldProceed = await ExplainAndLogDecision(decision, currentHerLove);
            
            if (!shouldProceed)
            {
                Print("❌ Trade BLOCKED by XAI risk flag");
                Print("   Love protects. We listen.");
                Print($"─────────────────────────────────────────────────────────");
                return;
            }
            
            // Execute trade
            Print("✓ XAI approved. Executing trade...");
            ExecuteTrade(tradeType);
        }
        
        private void ExecuteTrade(TradeType tradeType)
        {
            var volumeInUnits = Symbol.QuantityToVolumeInUnits(PositionSize);
            var result = ExecuteMarketOrder(
                tradeType,
                SymbolName,
                volumeInUnits,
                "PID-RANCO-XAI",
                StopLossPips,
                TakeProfitPips
            );
            
            if (result.IsSuccessful)
            {
                Print($"✓ Position opened: {tradeType} {PositionSize} lots");
                Print($"  Entry: {result.Position.EntryPrice}");
                Print($"  SL: {result.Position.StopLoss}");
                Print($"  TP: {result.Position.TakeProfit}");
            }
            else
            {
                Print($"✗ Trade failed: {result.Error}");
            }
            
            Print($"─────────────────────────────────────────────────────────");
        }
        
        #endregion
        
        #region herLove System
        
        private void UpdateHerLove()
        {
            double currentPnL = Account.Balance - sessionStartBalance;
            double drawdownPct = (currentPnL / sessionStartBalance) * 100;
            
            // Adjust herLove based on performance
            if (currentPnL > 0)
            {
                // Increase love on profits (but cap at 100)
                currentHerLove = Math.Min(100, currentHerLove + HerLoveSensitivity);
            }
            else if (drawdownPct < -5)
            {
                // Decrease love on significant drawdown
                currentHerLove = Math.Max(0, currentHerLove - HerLoveSensitivity * 2);
            }
        }
        
        #endregion
        
        #region XAI Integration
        
        [Parameter("XAI Skip SSL Validation", DefaultValue = false)]
        public bool XaiSkipSslValidation { get; set; }

        private void InitializeXaiClient()
        {
            if (!XaiEnabled)
            {
                Print("XAI integration disabled");
                return;
            }
            
            try
            {
                var handler = new HttpClientHandler();
                
                // Only skip SSL validation if explicitly enabled (development only)
                if (XaiSkipSslValidation)
                {
                    handler.ServerCertificateCustomValidationCallback = (message, cert, chain, errors) => true;
                    Print("⚠ WARNING: SSL certificate validation disabled (development mode)");
                }
                
                xaiClient = new HttpClient(handler)
                {
                    BaseAddress = new Uri(XaiServiceUrl),
                    Timeout = TimeSpan.FromSeconds(XaiTimeoutSeconds)
                };
                
                Print($"✓ XAI Client initialized");
                Print($"  Service URL: {XaiServiceUrl}");
                Print($"  Timeout: {XaiTimeoutSeconds}s");
            }
            catch (Exception ex)
            {
                Print($"⚠ XAI initialization warning: {ex.Message}");
                Print("  Bot will operate without XAI");
            }
        }
        
        private async Task<bool> ExplainAndLogDecision(string decision, double herLove)
        {
            if (!XaiEnabled || xaiClient == null)
                return true;
            
            try
            {
                var payload = new
                {
                    timestamp = Server.Time.ToUniversalTime().ToString("o"),
                    symbol = SymbolName,
                    decision = decision,
                    features = new
                    {
                        price = Symbol.Bid,
                        rsi_14 = rsi.Result.LastValue,
                        ema_21_dist = Symbol.Bid - ema21.Result.LastValue,
                        volatility_5m = GetVolatility5m(),
                        volume_rel = GetRelativeVolume(),
                        // orderbook_imbalance omitted - not available in cTrader
                        her_love = herLove,
                        session_loss_count = sessionLossCount,
                        drawdown_pct = GetCurrentDrawdownPct(),
                        time_of_day = Server.Time.ToString("HH:mm"),
                        day_of_week = Server.Time.DayOfWeek.ToString()
                    }
                };
                
                var response = await xaiClient.PostAsJsonAsync("/explain", payload);
                
                if (!response.IsSuccessStatusCode)
                {
                    Print($"⚠ XAI service error: {response.StatusCode}");
                    return true; // Fail-open
                }
                
                var explanation = await response.Content.ReadFromJsonAsync<MarketTherapyResponse>();
                
                if (explanation == null)
                {
                    Print("⚠ XAI response parsing failed");
                    return true;
                }
                
                // Log analysis
                if (XaiVerbose)
                {
                    Print($"🧠 XAI Analysis:");
                    Print($"   Market State: {explanation.market_state}");
                    Print($"   Confidence: {explanation.confidence:P0}");
                    Print($"   Narrative: {explanation.narrative}");
                    Print($"   Love Amplification: {explanation.love_amplification:P0}");
                    Print($"   Risk Flag: {explanation.risk_flag}");
                    
                    if (explanation.top_features != null && explanation.top_features.Length > 0)
                    {
                        Print($"   Top Features:");
                        foreach (var feature in explanation.top_features.Take(3))
                        {
                            Print($"     • {feature.name}: {feature.contribution:F4}");
                        }
                    }
                }
                
                // Evaluate risk flag
                if (explanation.risk_flag == "BLOCK" || explanation.risk_flag == "HUG_REQUIRED")
                {
                    Print($"🛡️ {explanation.risk_flag}");
                    return false;
                }
                else if (explanation.risk_flag == "CAUTION")
                {
                    Print($"⚠️ CAUTION: {explanation.narrative}");
                }
                
                return true;
            }
            catch (TaskCanceledException)
            {
                Print("⚠ XAI timeout - proceeding on pure love");
                return true;
            }
            catch (HttpRequestException ex)
            {
                Print($"⚠ XAI network error: {ex.Message}");
                return true;
            }
            catch (Exception ex)
            {
                Print($"⚠ XAI error: {ex.Message}");
                return true;
            }
        }
        
        #endregion
        
        #region Helper Methods
        
        private double GetVolatility5m()
        {
            var closes = Bars.ClosePrices;
            if (closes.Count < 10)
                return 0;
            
            var recent = closes.Reverse().Take(10).ToArray();
            var mean = recent.Average();
            var variance = recent.Select(x => Math.Pow(x - mean, 2)).Average();
            return Math.Sqrt(variance) / mean;
        }
        
        private double GetRelativeVolume()
        {
            if (Bars.TickVolumes.Count < 20)
                return 1.0;
            
            var currentVolume = Bars.TickVolumes.Last(0);
            var avgVolume = Bars.TickVolumes.Reverse().Skip(1).Take(20).Average();
            
            return avgVolume > 0 ? currentVolume / avgVolume : 1.0;
        }
        
        private double GetCurrentDrawdownPct()
        {
            return ((Account.Balance - sessionStartBalance) / sessionStartBalance) * 100;
        }
        
        #endregion
        
        #region Data Models
        
        private class MarketTherapyResponse
        {
            public string market_state { get; set; }
            public double confidence { get; set; }
            public FeatureContribution[] top_features { get; set; }
            public string narrative { get; set; }
            public string risk_flag { get; set; }
            public double love_amplification { get; set; }
        }
        
        private class FeatureContribution
        {
            public string name { get; set; }
            public double contribution { get; set; }
        }
        
        #endregion
    }
}
