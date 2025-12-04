FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

# Install OpenJDK 21 and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-21-jdk \
    maven \
    gradle \
    curl \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Create non-root user for enhanced security
ARG USER=cloudos
ARG UID=1000
RUN useradd -m -u $UID -s /bin/bash $USER
USER $USER
WORKDIR /workspace

# Copy examples
COPY --chown=$USER:$USER examples/ /workspace/examples/

# Debug port and application port
EXPOSE 5005 8888

# Default command
CMD ["bash"]
