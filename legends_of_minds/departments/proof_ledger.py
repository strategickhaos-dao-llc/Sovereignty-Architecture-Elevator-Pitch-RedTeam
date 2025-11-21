"""
Legends of Minds - Proof Action Ledger
Immutable audit trail of all code/config/files generated
"""

import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ProofEntry:
    """Immutable proof entry for audit trail"""
    id: int
    timestamp: str
    action: str
    department: str
    data: Dict
    hash: str
    previous_hash: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)
    
    def compute_hash(self) -> str:
        """Compute SHA-256 hash of entry"""
        entry_str = json.dumps({
            "id": self.id,
            "timestamp": self.timestamp,
            "action": self.action,
            "department": self.department,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(entry_str.encode()).hexdigest()


class ProofLedger:
    """Manage immutable proof action ledger"""
    
    def __init__(self, db_path: str = "/var/legends_of_minds/proof_ledger.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        """Initialize SQLite database for proof ledger"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proof_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                department TEXT NOT NULL,
                data TEXT NOT NULL,
                hash TEXT NOT NULL,
                previous_hash TEXT,
                verified INTEGER DEFAULT 1
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON proof_ledger(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_department ON proof_ledger(department)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_action ON proof_ledger(action)
        """)
        
        conn.commit()
        conn.close()
        
        logger.info(f"Proof ledger initialized at {self.db_path}")
    
    def add_entry(self, action: str, department: str, data: Dict) -> ProofEntry:
        """Add immutable entry to proof ledger"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get previous hash for chaining
        cursor.execute("SELECT hash FROM proof_ledger ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        previous_hash = result[0] if result else None
        
        # Create entry
        entry = ProofEntry(
            id=0,  # Will be set by database
            timestamp=datetime.utcnow().isoformat(),
            action=action,
            department=department,
            data=data,
            hash="",  # Will be computed
            previous_hash=previous_hash
        )
        
        # Compute hash
        entry.hash = entry.compute_hash()
        
        # Insert into database
        cursor.execute("""
            INSERT INTO proof_ledger (timestamp, action, department, data, hash, previous_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entry.timestamp,
            entry.action,
            entry.department,
            json.dumps(entry.data),
            entry.hash,
            entry.previous_hash
        ))
        
        entry.id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Added proof ledger entry {entry.id}: {action} in {department}")
        return entry
    
    def get_entries(self, limit: int = 100, department: Optional[str] = None) -> List[ProofEntry]:
        """Get proof ledger entries"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if department:
            cursor.execute("""
                SELECT id, timestamp, action, department, data, hash, previous_hash
                FROM proof_ledger
                WHERE department = ?
                ORDER BY id DESC
                LIMIT ?
            """, (department, limit))
        else:
            cursor.execute("""
                SELECT id, timestamp, action, department, data, hash, previous_hash
                FROM proof_ledger
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
        
        entries = []
        for row in cursor.fetchall():
            entry = ProofEntry(
                id=row[0],
                timestamp=row[1],
                action=row[2],
                department=row[3],
                data=json.loads(row[4]),
                hash=row[5],
                previous_hash=row[6]
            )
            entries.append(entry)
        
        conn.close()
        return entries
    
    def verify_chain(self) -> Dict:
        """Verify integrity of proof ledger chain"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, action, department, data, hash, previous_hash
            FROM proof_ledger
            ORDER BY id ASC
        """)
        
        entries = cursor.fetchall()
        conn.close()
        
        if not entries:
            return {"status": "verified", "entries": 0}
        
        errors = []
        previous_hash = None
        
        for row in entries:
            entry = ProofEntry(
                id=row[0],
                timestamp=row[1],
                action=row[2],
                department=row[3],
                data=json.loads(row[4]),
                hash=row[5],
                previous_hash=row[6]
            )
            
            # Verify hash
            computed_hash = entry.compute_hash()
            if computed_hash != entry.hash:
                errors.append(f"Entry {entry.id}: Hash mismatch")
            
            # Verify chain
            if entry.previous_hash != previous_hash:
                errors.append(f"Entry {entry.id}: Chain broken")
            
            previous_hash = entry.hash
        
        if errors:
            logger.error(f"Proof ledger verification failed: {errors}")
            return {
                "status": "failed",
                "entries": len(entries),
                "errors": errors
            }
        
        logger.info(f"Proof ledger verified: {len(entries)} entries")
        return {
            "status": "verified",
            "entries": len(entries)
        }
    
    def get_stats(self) -> Dict:
        """Get proof ledger statistics"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM proof_ledger")
        total = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT department, COUNT(*) as count
            FROM proof_ledger
            GROUP BY department
        """)
        by_department = {row[0]: row[1] for row in cursor.fetchall()}
        
        cursor.execute("""
            SELECT action, COUNT(*) as count
            FROM proof_ledger
            GROUP BY action
        """)
        by_action = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            "total_entries": total,
            "by_department": by_department,
            "by_action": by_action
        }


# Global proof ledger instance
proof_ledger = ProofLedger()
