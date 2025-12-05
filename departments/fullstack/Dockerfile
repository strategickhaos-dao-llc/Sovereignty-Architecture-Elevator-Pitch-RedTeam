# ============================================
# FULL-STACK DEPARTMENT
# Course: CS 465
# ============================================
FROM node:20-bookworm

LABEL maintainer="StrategicKhaos DAO LLC"
LABEL course.phase="fullstack"
LABEL course.ids="CS465"
LABEL description="Full-Stack Development course"

# Install additional tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    wget \
    vim \
    nano \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python backend frameworks
RUN pip3 install --no-cache-dir --break-system-packages \
    flask \
    django \
    fastapi \
    uvicorn \
    sqlalchemy \
    psycopg2-binary \
    python-dotenv

# Install global Node.js packages for frontend
RUN npm install -g \
    @angular/cli \
    create-react-app \
    vite \
    typescript \
    ts-node \
    nodemon

# Create workspace
WORKDIR /workspace

# Create project structure
RUN mkdir -p /workspace/{frontend,backend,shared,docs}

# Initialize frontend project template
RUN mkdir -p /workspace/templates

# CS 465 specific directories
RUN mkdir -p /workspace/CS465/{projects,assignments,labs}

# Copy department files
COPY --chown=1000:1000 . /workspace/department/

# Expose ports
EXPOSE 3000 5000 8080

# Default command
CMD ["bash"]
