# ============================================
# CORE PROGRAMMING DEPARTMENT
# Courses: CS 210, CS 230, CS 250, CS 340
# ============================================
FROM eclipse-temurin:21-jdk

LABEL maintainer="StrategicKhaos DAO LLC"
LABEL course.phase="core-programming"
LABEL course.ids="CS210,CS230,CS250,CS340"
LABEL description="Core programming and software development courses"

# Install additional tools
RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    git \
    curl \
    wget \
    vim \
    nano \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Python for multi-language support (CS 210)
RUN pip3 install --no-cache-dir \
    flask \
    django \
    requests \
    pytest

# Install Maven and Gradle for Java builds
RUN apt-get update && apt-get install -y \
    maven \
    && rm -rf /var/lib/apt/lists/*

# Create workspace
WORKDIR /workspace

# Create course directories
RUN mkdir -p /workspace/{CS210,CS230,CS250,CS340}

# CS 210 - Programming Languages
RUN echo "# CS 210 - Programming Languages" > /workspace/CS210/README.md

# CS 230 - Operating Platforms
RUN echo "# CS 230 - Operating Platforms" > /workspace/CS230/README.md

# CS 250 - Software Development Lifecycle
RUN echo "# CS 250 - Software Development Lifecycle" > /workspace/CS250/README.md

# CS 340 - Client/Server Development
RUN echo "# CS 340 - Client/Server Development" > /workspace/CS340/README.md

# Copy department files
COPY --chown=1000:1000 . /workspace/department/

# Default command
CMD ["bash"]
