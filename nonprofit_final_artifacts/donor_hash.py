#!/usr/bin/env python3
# donor_hash.py — SHA-256 + Salt + GPG → Arweave
import hashlib
import uuid
import gnupg
import os

gpg = gnupg.GPG()

def immortalize_donor(name, email, amount):
    salt = uuid.uuid4().hex
    donor_hash = hashlib.sha3_256(f"{name}{email}{amount}{salt}".encode()).hexdigest()
    record = f"{donor_hash} | {amount} USD | {uuid.uuid4()} | ValorYield 7% routed"
    signed = gpg.sign(record)
    
    # Create donors directory if it doesn't exist
    os.makedirs("donors", exist_ok=True)
    
    with open(f"donors/{donor_hash}.asc", "w") as f:
        f.write(str(signed))
    
    print(f"Donor immortalized → donors/{donor_hash}.asc")
    print(f"Arweave upload pending → _Orchestra.ps1 --immortalize-donors")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: donor_hash.py <name> <email> <amount>")
        sys.exit(1)
    
    immortalize_donor(sys.argv[1], sys.argv[2], sys.argv[3])
