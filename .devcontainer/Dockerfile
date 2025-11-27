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

# Install b3sum (BLAKE3)
RUN curl -sL https://github.com/BLAKE3-team/BLAKE3/releases/download/1.5.0/b3sum_linux_x64_bin -o /usr/local/bin/b3sum \
    && chmod +x /usr/local/bin/b3sum

# Install IPFS
RUN curl -sL https://dist.ipfs.tech/kubo/v0.24.0/kubo_v0.24.0_linux-amd64.tar.gz | tar xz \
    && mv kubo/ipfs /usr/local/bin/ \
    && rm -rf kubo

# Install Cosign
RUN curl -sLO https://github.com/sigstore/cosign/releases/download/v2.2.2/cosign-linux-amd64 \
    && mv cosign-linux-amd64 /usr/local/bin/cosign \
    && chmod +x /usr/local/bin/cosign

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
