# ============================================
# SOFTWARE ENGINEERING DEPARTMENT
# Courses: CS 319, CS 350, CS 405, CS 410
# ============================================
FROM ubuntu:22.04

LABEL maintainer="StrategicKhaos DAO LLC"
LABEL course.phase="software-engineering"
LABEL course.ids="CS319,CS350,CS405,CS410"
LABEL description="Software Engineering concentration courses"

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install development tools
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
    nodejs \
    npm \
    # Reverse engineering tools (CS 405)
    gdb \
    radare2 \
    binwalk \
    # Static analysis
    cppcheck \
    && rm -rf /var/lists/*

# Install Java 21
RUN apt-get update && apt-get install -y \
    openjdk-21-jdk \
    maven \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install Python security/engineering libraries
RUN pip3 install --no-cache-dir \
    flask \
    django \
    fastapi \
    uvicorn \
    pytest \
    bandit \
    safety \
    pylint \
    black

# Install Node.js UI/UX tools (CS 319)
RUN npm install -g \
    create-react-app \
    @angular/cli \
    vue-cli

# Create workspace
WORKDIR /workspace

# Create course directories
RUN mkdir -p /workspace/{CS319,CS350,CS405,CS410}

# Copy department files
COPY --chown=1000:1000 . /workspace/department/

# Default command
CMD ["bash"]
