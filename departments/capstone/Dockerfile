# ============================================
# CAPSTONE DEPARTMENT
# Course: CS 499
# ============================================
FROM ubuntu:22.04

LABEL maintainer="StrategicKhaos DAO LLC"
LABEL course.phase="capstone"
LABEL course.ids="CS499"
LABEL description="Computer Science Capstone Project"

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install comprehensive toolset for capstone
RUN apt-get update && apt-get install -y \
    # Build essentials
    build-essential \
    cmake \
    # Languages
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    openjdk-21-jdk \
    # DevOps tools
    docker.io \
    git \
    curl \
    wget \
    # Documentation
    pandoc \
    texlive-latex-base \
    # Utilities
    vim \
    nano \
    jq \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install Python libraries for capstone
RUN pip3 install --no-cache-dir \
    flask \
    django \
    fastapi \
    uvicorn \
    requests \
    pytest \
    jupyter \
    pandas \
    numpy \
    matplotlib

# Install kubectl for Kubernetes integration
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/

# Create workspace
WORKDIR /workspace

# Create capstone project structure
RUN mkdir -p /workspace/CS499/{project,documentation,presentation,artifacts}
RUN mkdir -p /workspace/CS499/project/{src,tests,config,deploy}

# Copy department files
COPY --chown=1000:1000 . /workspace/department/

# Capstone project README
RUN echo "# CS 499 - Computer Science Capstone" > /workspace/CS499/README.md && \
    echo "" >> /workspace/CS499/README.md && \
    echo "## Project: Sovereignty Architecture Integration" >> /workspace/CS499/README.md && \
    echo "" >> /workspace/CS499/README.md && \
    echo "This capstone project demonstrates mastery of:" >> /workspace/CS499/README.md && \
    echo "- Software Engineering principles" >> /workspace/CS499/README.md && \
    echo "- Cybersecurity best practices" >> /workspace/CS499/README.md && \
    echo "- Full-stack development" >> /workspace/CS499/README.md && \
    echo "- DevOps and cloud deployment" >> /workspace/CS499/README.md

# Default command
CMD ["bash"]
