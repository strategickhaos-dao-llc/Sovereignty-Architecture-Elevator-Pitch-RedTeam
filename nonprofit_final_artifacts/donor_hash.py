#!/usr/bin/env python3
# donor_hash.py — SHA-256 + Salt + GPG → Arweave
import hashlib
import uuid
import os
import sys

# Try to import gnupg, but make it optional for testing
try:
    import gnupg
    GPG_AVAILABLE = True
    gpg = gnupg.GPG()
except ImportError:
    GPG_AVAILABLE = False
    print("WARNING: gnupg module not installed. Install with: pip install python-gnupg", file=sys.stderr)
    print("         Donor records will be hashed but not GPG-signed.", file=sys.stderr)

def immortalize_donor(name, email, amount):
    salt = uuid.uuid4().hex
    donor_hash = hashlib.sha3_256(f"{name}{email}{amount}{salt}".encode()).hexdigest()
    record = f"{donor_hash} | {amount} USD | {uuid.uuid4()} | ValorYield 7% routed"
    
    # Create donors directory if it doesn't exist
    os.makedirs("donors", exist_ok=True)
    
    # Sign with GPG if available
    if GPG_AVAILABLE:
        signed = gpg.sign(record)
        with open(f"donors/{donor_hash}.asc", "w") as f:
            f.write(str(signed))
        print(f"Donor immortalized (GPG-signed) → donors/{donor_hash}.asc")
    else:
        # Save unsigned for testing purposes
        with open(f"donors/{donor_hash}.txt", "w") as f:
            f.write(record)
        print(f"Donor immortalized (unsigned) → donors/{donor_hash}.txt")
        print(f"Note: Install python-gnupg for GPG signing")
    
    print(f"Arweave upload pending → _Orchestra.ps1 --immortalize-donors")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: donor_hash.py <name> <email> <amount>")
        sys.exit(1)
    
    immortalize_donor(sys.argv[1], sys.argv[2], sys.argv[3])
