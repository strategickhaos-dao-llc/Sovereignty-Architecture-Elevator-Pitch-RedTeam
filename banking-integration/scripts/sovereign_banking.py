#!/usr/bin/env python3
"""
Sovereign Banking Integration
StrategicKhaos DAO LLC - Automated Charitable Distribution System

This module implements the 7% charitable distribution mechanism with:
- NATS message queue integration for transaction events
- Sequence.io API for banking operations
- Real-time Discord notifications
- Full audit logging with cryptographic verification
- Thread Bank (FDIC-insured) backend

Authorization: Board Resolution 2025-12-004
"""

import asyncio
import json
import logging
import os
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
from decimal import Decimal, ROUND_DOWN

try:
    from nats.aio.client import Client as NATS
    import aiohttp
except ImportError:
    print("Installing required dependencies...")
    import subprocess
    subprocess.check_call(["pip", "install", "nats-py", "aiohttp"])
    from nats.aio.client import Client as NATS
    import aiohttp

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('sovereign_banking')

# Configuration from environment variables
SEQUENCE_API_KEY = os.getenv('SEQUENCE_API_KEY')
SEQUENCE_API_URL = os.getenv('SEQUENCE_API_URL', 'https://api.getsequence.io/v1')
NATS_URL = os.getenv('NATS_URL', 'nats://localhost:4222')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

# Entity configuration (from Board Resolution 2025-12-004)
STRATEGICKHAOS_EIN = '39-2900295'
VALORYIELD_EIN = '39-2923503'
CHARITABLE_PERCENTAGE = Decimal('0.07')  # 7% to charity
OPERATING_PERCENTAGE = Decimal('0.93')   # 93% to operations


class BankingIntegrationError(Exception):
    """Custom exception for banking integration errors"""
    pass


class SovereignBankingProcessor:
    """
    Main processor for sovereign banking integration.
    Handles transaction routing, distribution calculation, and audit logging.
    """
    
    def __init__(self):
        if not SEQUENCE_API_KEY:
            raise BankingIntegrationError("SEQUENCE_API_KEY environment variable not set")
        
        self.session: Optional[aiohttp.ClientSession] = None
        self.nats_client: Optional[NATS] = None
        self.transaction_count = 0
        
    async def initialize(self):
        """Initialize HTTP session and NATS connection"""
        self.session = aiohttp.ClientSession(
            headers={
                'Authorization': f'Bearer {SEQUENCE_API_KEY}',
                'Content-Type': 'application/json'
            }
        )
        
        self.nats_client = NATS()
        await self.nats_client.connect(NATS_URL)
        logger.info(f"Connected to NATS at {NATS_URL}")
        
    async def close(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
        if self.nats_client:
            await self.nats_client.close()
            
    async def process_transaction(self, msg):
        """
        Process incoming transaction from NATS queue.
        
        Expected message format:
        {
            "transaction_id": "unique_id",
            "amount": 1000.00,
            "source": "revenue_stream_name",
            "timestamp": "2025-12-05T14:00:00Z",
            "metadata": {...}
        }
        """
        try:
            data = json.loads(msg.data.decode())
            logger.info(f"Processing transaction: {data.get('transaction_id')}")
            
            # Validate transaction data
            if 'amount' not in data:
                raise BankingIntegrationError("Transaction missing 'amount' field")
            
            amount = Decimal(str(data['amount']))
            if amount <= 0:
                raise BankingIntegrationError(f"Invalid amount: {amount}")
            
            # Calculate distribution (7% charity, 93% operations)
            charity_amount = (amount * CHARITABLE_PERCENTAGE).quantize(
                Decimal('0.01'), rounding=ROUND_DOWN
            )
            operating_amount = (amount * OPERATING_PERCENTAGE).quantize(
                Decimal('0.01'), rounding=ROUND_DOWN
            )
            
            # Ensure total doesn't exceed original (due to rounding)
            total = charity_amount + operating_amount
            if total > amount:
                operating_amount = amount - charity_amount
            
            logger.info(
                f"Distribution: ${amount} total -> "
                f"${charity_amount} charity (7%) + "
                f"${operating_amount} operations (93%)"
            )
            
            # Execute transfers via Sequence API
            charity_result = await self._transfer_to_valoryield(
                charity_amount, 
                data.get('transaction_id'),
                data.get('source', 'unknown')
            )
            
            operating_result = await self._transfer_to_strategickhaos(
                operating_amount,
                data.get('transaction_id'),
                data.get('source', 'unknown')
            )
            
            # Generate audit record
            audit_record = self._generate_audit_record(
                data, charity_amount, operating_amount,
                charity_result, operating_result
            )
            
            # Store audit record
            await self._store_audit_record(audit_record)
            
            # Send Discord notification
            await self._notify_discord(audit_record)
            
            self.transaction_count += 1
            logger.info(
                f"Transaction {data.get('transaction_id')} processed successfully. "
                f"Total processed: {self.transaction_count}"
            )
            
        except Exception as e:
            logger.error(f"Error processing transaction: {e}", exc_info=True)
            await self._notify_error(msg.data.decode(), str(e))
            
    async def _transfer_to_valoryield(
        self, 
        amount: Decimal, 
        transaction_id: str,
        source: str
    ) -> Dict[str, Any]:
        """Transfer funds to ValorYield Engine (501c3, EIN 39-2923503)"""
        payload = {
            "amount": float(amount),
            "to_account": f"valoryield_ein_{VALORYIELD_EIN.replace('-', '_')}",
            "memo": f"Automated 7% charitable distribution - TX:{transaction_id}",
            "metadata": {
                "entity": "ValorYield Engine",
                "ein": VALORYIELD_EIN,
                "tax_status": "501(c)(3)",
                "source_transaction": transaction_id,
                "revenue_source": source,
                "distribution_date": datetime.utcnow().isoformat(),
                "board_resolution": "2025-12-004"
            }
        }
        
        async with self.session.post(
            f"{SEQUENCE_API_URL}/transfers",
            json=payload
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                raise BankingIntegrationError(
                    f"ValorYield transfer failed: {response.status} - {error_text}"
                )
            result = await response.json()
            logger.info(f"ValorYield transfer completed: {result.get('transfer_id')}")
            return result
            
    async def _transfer_to_strategickhaos(
        self,
        amount: Decimal,
        transaction_id: str,
        source: str
    ) -> Dict[str, Any]:
        """Transfer funds to StrategicKhaos DAO LLC (EIN 39-2900295)"""
        payload = {
            "amount": float(amount),
            "to_account": f"strategickhaos_ein_{STRATEGICKHAOS_EIN.replace('-', '_')}",
            "memo": f"Operating capital - 93% allocation - TX:{transaction_id}",
            "metadata": {
                "entity": "StrategicKhaos DAO LLC",
                "ein": STRATEGICKHAOS_EIN,
                "jurisdiction": "Wyoming",
                "source_transaction": transaction_id,
                "revenue_source": source,
                "distribution_date": datetime.utcnow().isoformat(),
                "board_resolution": "2025-12-004"
            }
        }
        
        async with self.session.post(
            f"{SEQUENCE_API_URL}/transfers",
            json=payload
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                raise BankingIntegrationError(
                    f"StrategicKhaos transfer failed: {response.status} - {error_text}"
                )
            result = await response.json()
            logger.info(f"StrategicKhaos transfer completed: {result.get('transfer_id')}")
            return result
            
    def _generate_audit_record(
        self,
        original_tx: Dict[str, Any],
        charity_amount: Decimal,
        operating_amount: Decimal,
        charity_result: Dict[str, Any],
        operating_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate cryptographically verifiable audit record"""
        record = {
            "audit_id": f"audit_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}",
            "timestamp": datetime.utcnow().isoformat(),
            "original_transaction": {
                "id": original_tx.get('transaction_id'),
                "amount": str(original_tx.get('amount')),
                "source": original_tx.get('source'),
            },
            "distribution": {
                "charity": {
                    "entity": "ValorYield Engine",
                    "ein": VALORYIELD_EIN,
                    "amount": str(charity_amount),
                    "percentage": "7%",
                    "transfer_id": charity_result.get('transfer_id'),
                    "status": charity_result.get('status')
                },
                "operations": {
                    "entity": "StrategicKhaos DAO LLC",
                    "ein": STRATEGICKHAOS_EIN,
                    "amount": str(operating_amount),
                    "percentage": "93%",
                    "transfer_id": operating_result.get('transfer_id'),
                    "status": operating_result.get('status')
                }
            },
            "compliance": {
                "board_resolution": "2025-12-004",
                "approved_date": "2025-12-05",
                "distribution_mechanism": "automated",
                "verification_method": "SHA256"
            }
        }
        
        # Generate SHA256 hash for integrity verification
        record_json = json.dumps(record, sort_keys=True)
        record['sha256_hash'] = hashlib.sha256(record_json.encode()).hexdigest()
        
        return record
        
    async def _store_audit_record(self, record: Dict[str, Any]):
        """Store audit record for compliance and verification"""
        # In production, this would write to a secure audit database
        # For now, write to local audit log file
        audit_log_path = os.getenv('AUDIT_LOG_PATH', '/var/log/sovereign-banking/audit.jsonl')
        
        try:
            os.makedirs(os.path.dirname(audit_log_path), exist_ok=True)
            with open(audit_log_path, 'a') as f:
                f.write(json.dumps(record) + '\n')
            logger.info(f"Audit record stored: {record['audit_id']}")
        except Exception as e:
            logger.error(f"Failed to store audit record: {e}")
            # In production, this should trigger alerts
            
    async def _notify_discord(self, audit_record: Dict[str, Any]):
        """Send transaction notification to Discord"""
        if not DISCORD_WEBHOOK_URL:
            logger.warning("DISCORD_WEBHOOK_URL not set, skipping notification")
            return
            
        charity = audit_record['distribution']['charity']
        operations = audit_record['distribution']['operations']
        
        embed = {
            "title": "💰 Automated Distribution Complete",
            "color": 0x00FF00,  # Green
            "fields": [
                {
                    "name": "Original Amount",
                    "value": f"${audit_record['original_transaction']['amount']}",
                    "inline": True
                },
                {
                    "name": "Source",
                    "value": audit_record['original_transaction']['source'],
                    "inline": True
                },
                {
                    "name": "\u200b",
                    "value": "\u200b",
                    "inline": False
                },
                {
                    "name": "🎯 ValorYield Engine (501c3)",
                    "value": f"${charity['amount']} ({charity['percentage']})",
                    "inline": True
                },
                {
                    "name": "⚔️ StrategicKhaos DAO",
                    "value": f"${operations['amount']} ({operations['percentage']})",
                    "inline": True
                },
                {
                    "name": "\u200b",
                    "value": "\u200b",
                    "inline": False
                },
                {
                    "name": "Audit ID",
                    "value": audit_record['audit_id'],
                    "inline": False
                },
                {
                    "name": "Verification Hash",
                    "value": f"`{audit_record['sha256_hash'][:16]}...`",
                    "inline": False
                }
            ],
            "footer": {
                "text": "Board Resolution 2025-12-004 | Cryptographically Verified"
            },
            "timestamp": audit_record['timestamp']
        }
        
        payload = {
            "embeds": [embed]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(DISCORD_WEBHOOK_URL, json=payload) as response:
                    if response.status != 204:
                        logger.warning(f"Discord notification failed: {response.status}")
        except Exception as e:
            logger.error(f"Failed to send Discord notification: {e}")
            
    async def _notify_error(self, transaction_data: str, error_message: str):
        """Send error notification to Discord"""
        if not DISCORD_WEBHOOK_URL:
            return
            
        embed = {
            "title": "⚠️ Transaction Processing Error",
            "color": 0xFF0000,  # Red
            "fields": [
                {
                    "name": "Error",
                    "value": error_message[:1000],  # Limit length
                    "inline": False
                },
                {
                    "name": "Transaction Data",
                    "value": f"```json\n{transaction_data[:500]}\n```",
                    "inline": False
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        payload = {"embeds": [embed]}
        
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(DISCORD_WEBHOOK_URL, json=payload)
        except Exception as e:
            logger.error(f"Failed to send error notification: {e}")


async def main():
    """Main entry point for sovereign banking processor"""
    logger.info("Starting Sovereign Banking Integration...")
    logger.info(f"StrategicKhaos DAO LLC (EIN: {STRATEGICKHAOS_EIN})")
    logger.info(f"ValorYield Engine (EIN: {VALORYIELD_EIN})")
    logger.info(f"Distribution: {CHARITABLE_PERCENTAGE*100}% charity, {OPERATING_PERCENTAGE*100}% operations")
    
    processor = SovereignBankingProcessor()
    
    try:
        await processor.initialize()
        
        # Subscribe to revenue incoming events
        await processor.nats_client.subscribe(
            "revenue.incoming",
            cb=processor.process_transaction
        )
        
        logger.info("Subscribed to revenue.incoming topic")
        logger.info("Sovereign Banking Integration is now running...")
        
        # Keep the service running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        await processor.close()


if __name__ == '__main__':
    asyncio.run(main())
