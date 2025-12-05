# ============================================
# CYBERSECURITY DEPARTMENT
# Courses: CYB 200, CYB 210, CYB 220, CYB 240, CYB 300, CYB 320
# ============================================
FROM kalilinux/kali-rolling

LABEL maintainer="StrategicKhaos DAO LLC"
LABEL course.phase="cybersecurity"
LABEL course.ids="CYB200,CYB210,CYB220,CYB240,CYB300,CYB320"
LABEL description="Cybersecurity concentration courses"

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install security tools
RUN apt-get update && apt-get install -y \
    # Network Security (CYB 210)
    nmap \
    wireshark \
    tcpdump \
    netcat-traditional \
    # Penetration Testing (CYB 320)
    metasploit-framework \
    burpsuite \
    sqlmap \
    nikto \
    dirb \
    # Digital Forensics (CYB 300)
    autopsy \
    sleuthkit \
    foremost \
    volatility3 \
    # General tools
    python3 \
    python3-pip \
    git \
    curl \
    wget \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Install Python security libraries using virtual environment
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir \
    scapy \
    requests \
    cryptography \
    pycryptodome \
    python-nmap \
    impacket

ENV PATH="/opt/venv/bin:$PATH"

# Create workspace
WORKDIR /workspace

# Create course directories
RUN mkdir -p /workspace/{CYB200,CYB210,CYB220,CYB240,CYB300,CYB320}

# Copy department files
COPY --chown=1000:1000 . /workspace/department/

# Security notice
RUN echo "WARNING: This container contains security testing tools." > /workspace/SECURITY_NOTICE.txt && \
    echo "Use only in authorized testing environments." >> /workspace/SECURITY_NOTICE.txt && \
    echo "Never use against systems without explicit permission." >> /workspace/SECURITY_NOTICE.txt

# Default command
CMD ["bash"]
