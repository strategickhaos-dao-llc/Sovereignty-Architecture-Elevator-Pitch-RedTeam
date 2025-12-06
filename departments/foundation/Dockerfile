# ============================================
# FOUNDATION DEPARTMENT
# Courses: MAT 243, IT 145, PHY 150
# ============================================
FROM ubuntu:22.04

LABEL maintainer="StrategicKhaos DAO LLC"
LABEL course.phase="foundation"
LABEL course.ids="MAT243,IT145,PHY150"
LABEL description="Foundation courses for CS/Cybersecurity degree"

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install base tools
RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    vim \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install Python scientific libraries for MAT 243 (Statistics)
RUN pip3 install --no-cache-dir \
    numpy \
    pandas \
    scipy \
    matplotlib \
    seaborn \
    jupyter \
    statsmodels

# Install Java for IT 145 (Application Development)
RUN apt-get update && apt-get install -y \
    openjdk-21-jdk \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Create workspace
WORKDIR /workspace

# Create course directories
RUN mkdir -p /workspace/{MAT243,IT145,PHY150}

# Copy spellbooks if available
COPY --chown=1000:1000 . /workspace/department/

# Default command
CMD ["bash"]
