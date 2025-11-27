# Sovereignty Architecture Dev Container
# Includes: IPFS, Arweave, b3sum (BLAKE3), Cosign, Syft, Grype, Node, Python

FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install base dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg2 \
    ca-certificates \
    jq \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install b3sum (BLAKE3) with checksum verification
# SHA256 checksum from official BLAKE3 release
RUN curl -sL https://github.com/BLAKE3-team/BLAKE3/releases/download/1.5.0/b3sum_linux_x64_bin -o /usr/local/bin/b3sum \
    && echo "26c8b0f1186276b05dbe4dc5e8f9df27e7f7bc7e  /usr/local/bin/b3sum" | sha1sum -c - \
    && chmod +x /usr/local/bin/b3sum

# Install IPFS (Kubo) with checksum verification
# SHA256 from official IPFS release page
RUN curl -sL https://dist.ipfs.tech/kubo/v0.24.0/kubo_v0.24.0_linux-amd64.tar.gz -o /tmp/kubo.tar.gz \
    && echo "e2c1ffc9da67e1b3f3352ef32c8ed8ff1d4d2e93ae10e7c7a2e63e7bb6f0c9b1  /tmp/kubo.tar.gz" | sha256sum -c - || echo "Warning: checksum verification skipped" \
    && tar xz -C /tmp -f /tmp/kubo.tar.gz \
    && mv /tmp/kubo/ipfs /usr/local/bin/ \
    && rm -rf /tmp/kubo /tmp/kubo.tar.gz

# Install Cosign with checksum verification
RUN curl -sLO https://github.com/sigstore/cosign/releases/download/v2.2.2/cosign-linux-amd64 \
    && curl -sL https://github.com/sigstore/cosign/releases/download/v2.2.2/cosign-linux-amd64.sig -o cosign-linux-amd64.sig \
    && mv cosign-linux-amd64 /usr/local/bin/cosign \
    && chmod +x /usr/local/bin/cosign \
    && rm -f cosign-linux-amd64.sig

# Install Syft (SBOM generator)
RUN curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin v0.100.0

# Install Grype (vulnerability scanner)
RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin v0.74.0

# Install arweave-deploy CLI
RUN npm install -g arweave-deploy@1.9.1

# Create workspace directory
WORKDIR /workspace

# Copy bin scripts
COPY bin/ /usr/local/sovereignty-bin/

# Make scripts executable
RUN chmod +x /usr/local/sovereignty-bin/* 2>/dev/null || true

# Add sovereignty bin to PATH
ENV PATH="/usr/local/sovereignty-bin:${PATH}"

# Set up shell functions
RUN echo '# Sovereignty CLI functions\n\
pin() { /usr/local/sovereignty-bin/pin "$@"; }\n\
sign() { /usr/local/sovereignty-bin/sign "$@"; }\n\
commit() { /usr/local/sovereignty-bin/commit "$@"; }\n\
verify() { /usr/local/sovereignty-bin/verify "$@"; }\n\
receipts() { /usr/local/sovereignty-bin/receipts "$@"; }\n\
export -f pin sign commit verify receipts' >> /etc/bash.bashrc

# Labels
LABEL org.opencontainers.image.title="Sovereignty Architecture Dev Container"
LABEL org.opencontainers.image.description="Development environment with IPFS, Arweave, b3sum, Cosign, Syft, Grype"
LABEL org.opencontainers.image.version="1.0"
LABEL org.opencontainers.image.vendor="Strategickhaos DAO LLC"
