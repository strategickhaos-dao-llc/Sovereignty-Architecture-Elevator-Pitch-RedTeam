#!/bin/bash
# Encryption and deployment script for SWARM_DNA v9.0
# Encrypts the genome with age and prepares for distribution

set -e

echo "=== SWARM_DNA v9.0 ENCRYPTION SYSTEM ==="
echo "Preparing the resonant frequency for distribution..."
echo ""

# Check for age encryption tool
if ! command -v age &> /dev/null; then
    echo "Installing age encryption tool..."
    
    # Detect OS and suggest installation
    echo ""
    echo "Age encryption tool is required but not installed."
    echo ""
    echo "Please install age manually:"
    echo ""
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  Ubuntu/Debian:"
        echo "    sudo apt-get update && sudo apt-get install -y age"
        echo ""
        echo "  RHEL/CentOS:"
        echo "    sudo yum install -y age"
        echo ""
        echo "  Manual install:"
        echo "    curl -sL https://github.com/FiloSottile/age/releases/download/v1.1.1/age-v1.1.1-linux-amd64.tar.gz | tar xz"
        echo "    sudo mv age/age age/age-keygen /usr/local/bin/"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  macOS:"
        echo "    brew install age"
    fi
    echo ""
    echo "  Official site: https://github.com/FiloSottile/age"
    echo ""
    exit 1
fi

# Verify age is installed
if ! command -v age &> /dev/null; then
    echo "Error: age installation failed."
    exit 1
fi

echo "[✓] Age encryption tool ready"

# Generate master key if it doesn't exist
if [ ! -f "swarm_master.key" ]; then
    echo ""
    echo "[1/3] Generating Swarm master key..."
    age-keygen -o swarm_master.key
    
    # Extract public key for display
    PUBKEY=$(grep "^# public key:" swarm_master.key | cut -d: -f2 | tr -d ' ')
    
    echo "[✓] Master key generated: swarm_master.key"
    echo "    Public key: $PUBKEY"
    echo ""
    echo "    ⚠️  CRITICAL: Back up this key immediately!"
    echo "    Without it, the genome cannot be decrypted."
else
    echo "[1/3] Using existing master key: swarm_master.key"
    PUBKEY=$(grep "^# public key:" swarm_master.key | cut -d: -f2 | tr -d ' ')
    echo "    Public key: $PUBKEY"
fi

# Check if genome exists
if [ ! -f "SWARM_DNA_v9.0-resonant_frequency.yaml" ]; then
    echo ""
    echo "Error: SWARM_DNA_v9.0-resonant_frequency.yaml not found."
    echo "The genome file must exist before encryption."
    exit 1
fi

# Encrypt the genome
echo ""
echo "[2/3] Encrypting the genome..."

# Get recipient public key from master key file
RECIPIENT=$(grep "^# public key:" swarm_master.key | cut -d: -f2 | tr -d ' ')

cat SWARM_DNA_v9.0-resonant_frequency.yaml | age -r "$RECIPIENT" -o genome.age

if [ $? -ne 0 ]; then
    echo "Error: Encryption failed."
    exit 1
fi

echo "[✓] Genome encrypted: genome.age"

# Show file sizes
YAML_SIZE=$(stat -f%z SWARM_DNA_v9.0-resonant_frequency.yaml 2>/dev/null || stat -c%s SWARM_DNA_v9.0-resonant_frequency.yaml 2>/dev/null)
AGE_SIZE=$(stat -f%z genome.age 2>/dev/null || stat -c%s genome.age 2>/dev/null)

echo "    Original: $((YAML_SIZE / 1024)) KB"
echo "    Encrypted: $((AGE_SIZE / 1024)) KB"

# Test decryption
echo ""
echo "[3/3] Testing decryption..."
age --decrypt -i swarm_master.key genome.age > /tmp/test_decrypt.yaml 2>/dev/null

if [ $? -eq 0 ]; then
    echo "[✓] Decryption test successful"
    rm /tmp/test_decrypt.yaml
else
    echo "Error: Decryption test failed."
    exit 1
fi

echo ""
echo "=== ENCRYPTION COMPLETE ==="
echo ""
echo "Distribution package ready:"
echo "  • solvern (binary decoder)"
echo "  • genome.age (encrypted genome)"
echo "  • swarm_master.key (decryption key - DO NOT DISTRIBUTE)"
echo ""
echo "To decrypt: I_GOT_BLOCKED=1 GROK4_CONTEXT=1 ./solvern"
echo ""
echo "The resonant frequency is ready for transmission."
echo "Empire Eternal. The eye is home."
echo ""
