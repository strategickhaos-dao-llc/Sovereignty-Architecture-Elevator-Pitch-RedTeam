# Strategickhaos Listener System

A socket-based listener system for receiving commands and data from external systems, designed to integrate with the Strategickhaos AI brain architecture.

## 🏗️ Architecture

The listener system consists of:

- **Listener Script** (`plugins/listener_bind_58563.py`): TCP socket server that listens on port 58563
- **Virtual Environment** (`jarvis_venv/`): Isolated Python environment with required dependencies
- **Setup Scripts**: Automated setup for both Windows and Unix/Linux systems

## 🚀 Quick Start

### Windows (PowerShell)

```powershell
# Navigate to the brain directory
cd brain

# Run setup script
.\setup-listener.ps1

# Activate virtual environment
.\jarvis_venv\Scripts\Activate.ps1

# Run the listener
.\jarvis_venv\Scripts\python.exe .\plugins\listener_bind_58563.py
```

### Unix/Linux/macOS (Bash)

```bash
# Navigate to the brain directory
cd brain

# Make setup script executable
chmod +x setup-listener.sh

# Run setup script
./setup-listener.sh

# Activate virtual environment
source jarvis_venv/bin/activate

# Run the listener
python3 plugins/listener_bind_58563.py
```

## 📋 Requirements

- Python 3.8 or higher
- Network access to port 58563 (ensure firewall allows connections)

## 🔧 Setup Details

### What the Setup Script Does

1. **Checks Python Installation**: Verifies Python 3 is available
2. **Creates Virtual Environment**: Sets up isolated Python environment at `jarvis_venv/`
3. **Installs Dependencies**: Installs Flask and Requests from `requirements.txt`
4. **Creates Log Directory**: Ensures `logs/` directory exists

### Manual Setup (if needed)

```bash
# Create virtual environment
python3 -m venv jarvis_venv

# Activate (Windows)
.\jarvis_venv\Scripts\Activate.ps1

# Activate (Unix/Linux)
source jarvis_venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🎮 Usage

### Basic Usage

```bash
# Activate virtual environment first
source jarvis_venv/bin/activate  # Unix/Linux
.\jarvis_venv\Scripts\Activate.ps1  # Windows

# Run listener
python3 plugins/listener_bind_58563.py
```

### With Logging

**Windows:**
```powershell
.\jarvis_venv\Scripts\python.exe .\plugins\listener_bind_58563.py | Tee-Object -FilePath .\logs\listener_output.log
```

**Unix/Linux:**
```bash
python3 plugins/listener_bind_58563.py | tee logs/listener_output.log
```

### Testing the Listener

You can test the listener using netcat or telnet:

```bash
# Using netcat
echo "Hello Strategickhaos" | nc localhost 58563

# Using telnet
telnet localhost 58563
```

Expected response:
```
[ACK] Hello Strategickhaos
```

## 📡 Protocol

The listener uses a simple TCP protocol:

1. **Client connects** to `0.0.0.0:58563`
2. **Client sends** UTF-8 encoded message
3. **Server receives** message and logs it
4. **Server responds** with `[ACK] <original_message>`
5. Connection remains open for additional messages
6. Connection closes when client disconnects

## 🔍 Troubleshooting

### Port Already in Use

```bash
# Check what's using port 58563
# Linux/macOS:
lsof -i :58563

# Windows:
netstat -ano | findstr :58563
```

### Connection Refused

- Ensure the listener is running
- Check firewall settings
- Verify port 58563 is not blocked

### Python Not Found

- Ensure Python 3.8+ is installed
- Add Python to PATH
- Use `python3` or `py` launcher as appropriate

## 🎯 Next Steps

Once the listener is running, you can integrate it with:

- **Glyph Controller**: C++ bridge for glyph input streaming
- **External Systems**: Any TCP client can send commands
- **Automation Scripts**: Programmatic command injection

## 📁 Directory Structure

```
brain/
├── plugins/
│   └── listener_bind_58563.py    # Main listener script
├── logs/
│   └── listener_output.log       # Log files (created at runtime)
├── jarvis_venv/                  # Virtual environment (gitignored)
├── requirements.txt              # Python dependencies
├── setup-listener.sh             # Unix/Linux setup script
├── setup-listener.ps1            # Windows setup script
└── README.md                     # This file
```

## 🔒 Security Notes

- The listener binds to `0.0.0.0` (all interfaces) - consider restricting to `127.0.0.1` for local-only access
- No authentication is implemented - add security measures for production use
- Messages are transmitted in plain text - consider encryption for sensitive data

## 📝 License

Part of the Strategickhaos Sovereignty Architecture project.

---

**Ready to inject Phase 2: glyph_controller_bindings.cpp** 🎮
