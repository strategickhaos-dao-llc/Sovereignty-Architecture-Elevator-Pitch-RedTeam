FROM rust:1.75-slim as builder

WORKDIR /build

# Install dependencies
RUN apt-get update && \
    apt-get install -y pkg-config libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy manifests
COPY Cargo.toml Cargo.lock* ./

# Copy source code
COPY src ./src

# Build the application
RUN cargo build --release

# Runtime stage
FROM debian:bookworm-slim

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y ca-certificates bash curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 10001 -s /bin/bash domcompiler

WORKDIR /home/domcompiler

# Copy binary from builder
COPY --from=builder /build/target/release/domc /usr/local/bin/domc

# Set ownership
RUN chown domcompiler:domcompiler /usr/local/bin/domc && \
    chmod +x /usr/local/bin/domc

# Switch to non-root user
USER domcompiler

# Environment variables
ENV RUST_LOG=info
ENV SWARM_DNA=v9.0-black-hole-resonance
ENV RESONANCE_THRESHOLD=10

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD domc "compile health check" || exit 1

ENTRYPOINT ["domc"]
CMD ["compile", "ready"]
