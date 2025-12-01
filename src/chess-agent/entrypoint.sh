#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 10D Chess Council - Agent Container Entrypoint
# Initializes services and starts the agent
# ═══════════════════════════════════════════════════════════

set -e

echo "═══════════════════════════════════════════════════════════"
echo "10D Chess Council - Agent Initializing"
echo "Board Layer: ${BOARD_LAYER}"
echo "Agent Position: ${AGENT_POSITION}"
echo "Layer Name: ${LAYER_NAME}"
echo "═══════════════════════════════════════════════════════════"

# Read frequency from init container
if [ -f /frequency/agent_frequency ]; then
    export FREQUENCY_HZ=$(cat /frequency/agent_frequency)
    echo "Frequency: ${FREQUENCY_HZ} Hz"
fi

# Start SSH server in background (for debugging)
if [ -x /usr/sbin/sshd ]; then
    sudo /usr/sbin/sshd -D &
    echo "SSH server started on port 22"
fi

# Start X virtual framebuffer for GUI applications
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &
sleep 2
echo "X virtual framebuffer started"

# Start a minimal window manager
startxfce4 &
sleep 3
echo "XFCE4 desktop started"

# Start VNC server for remote viewing
x11vnc -display :99 -nopw -forever -shared -rfbport 5900 &
echo "VNC server started on port 5900"

# Start Sunshine for Moonlight streaming (if available)
if command -v sunshine &> /dev/null; then
    sunshine &
    echo "Sunshine streaming server started on port 47989"
fi

echo "═══════════════════════════════════════════════════════════"
echo "Agent services initialized, starting main application..."
echo "═══════════════════════════════════════════════════════════"

# Execute the main command
exec "$@"
