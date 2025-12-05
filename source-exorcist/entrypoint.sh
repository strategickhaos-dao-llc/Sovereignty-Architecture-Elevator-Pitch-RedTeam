#!/bin/bash
set -e

echo "========================================"
echo "Source Exorcist - Container Starting"
echo "========================================"
echo ""

# Check if watchlist exists
if [ ! -f "watchlist.yaml" ]; then
    echo "ERROR: watchlist.yaml not found!"
    echo "Please mount your watchlist.yaml file."
    exit 1
fi

# Ensure directories exist
mkdir -p reports checksums

# Execute the command passed to the container
exec "$@"
