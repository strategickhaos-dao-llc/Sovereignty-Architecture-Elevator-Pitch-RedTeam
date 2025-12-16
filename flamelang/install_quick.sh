#!/bin/bash
# FlameLang Quick Installation Script
# Installs all dependencies for C++ and Rust benchmarks

set -e

echo "🔥 FlameLang Quick Install"
echo "=========================="
echo ""

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "Cannot detect OS"
    exit 1
fi

echo "Detected OS: $OS"
echo ""

# Ubuntu/Debian installation
if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    echo "Installing for Ubuntu/Debian..."
    
    echo "→ Updating package lists..."
    sudo apt update
    
    echo "→ Installing C++ build tools..."
    sudo apt install -y build-essential g++-11 cmake ninja-build
    
    echo "→ Installing C++ libraries..."
    sudo apt install -y libboost-all-dev libeigen3-dev
    
    echo "→ Installing Google Benchmark..."
    if ! pkg-config --exists benchmark; then
        echo "  Building from source..."
        cd /tmp
        git clone https://github.com/google/benchmark.git
        cd benchmark
        mkdir -p build && cd build
        cmake .. -DCMAKE_BUILD_TYPE=Release -DBENCHMARK_ENABLE_TESTING=OFF
        make -j$(nproc)
        sudo make install
        cd /tmp && rm -rf benchmark
    else
        echo "  Already installed ✓"
    fi
    
    echo "→ Installing Rust..."
    if ! command -v rustc &> /dev/null; then
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        source "$HOME/.cargo/env"
    else
        echo "  Already installed ✓"
    fi
    
    echo "→ Installing Rust tools..."
    cargo install cargo-criterion flamegraph --quiet || true
    
    echo "→ Installing Python tools..."
    sudo apt install -y python3-pip python3-venv
    pip3 install pandas matplotlib jinja2 pytest --quiet
    
    echo "→ Installing documentation tools..."
    sudo apt install -y doxygen graphviz

# macOS installation
elif [ "$OS" = "darwin" ]; then
    echo "Installing for macOS..."
    
    if ! command -v brew &> /dev/null; then
        echo "Please install Homebrew first: https://brew.sh"
        exit 1
    fi
    
    echo "→ Installing C++ build tools..."
    brew install gcc@11 llvm cmake ninja
    
    echo "→ Installing C++ libraries..."
    brew install boost eigen google-benchmark
    
    echo "→ Installing Rust..."
    if ! command -v rustc &> /dev/null; then
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        source "$HOME/.cargo/env"
    else
        echo "  Already installed ✓"
    fi
    
    echo "→ Installing Rust tools..."
    cargo install cargo-criterion flamegraph --quiet || true
    
    echo "→ Installing Python tools..."
    brew install python@3.10
    pip3 install pandas matplotlib jinja2 pytest --quiet
    
    echo "→ Installing documentation tools..."
    brew install doxygen graphviz

else
    echo "Unsupported OS: $OS"
    echo "Please see OS_INVENTORY.md for manual installation instructions"
    exit 1
fi

echo ""
echo "✓ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Build C++ benchmarks:"
echo "     cd benchmarks && mkdir build && cd build"
echo "     cmake .. -DCMAKE_BUILD_TYPE=Release && make"
echo "     ./cpp_benchmark"
echo ""
echo "  2. Run Rust benchmarks:"
echo "     cd benchmarks && cargo bench"
echo ""
echo "  3. Read the documentation:"
echo "     less README.md"
echo ""
echo "🔥 Happy benchmarking!"
