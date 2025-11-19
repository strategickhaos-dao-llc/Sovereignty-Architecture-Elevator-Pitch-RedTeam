# 🚀 Strategickhaos Listener - Quick Start Guide

This guide helps you quickly set up and run the Strategickhaos Listener system after a clean rebuild.

## 📦 What You Need

- Python 3.8 or higher
- Port 58563 available
- Network access (check firewall settings)

## ⚡ Quick Setup (Windows PowerShell)

```powershell
# 1. Navigate to brain directory
cd brain

# 2. Run automated setup
.\setup-listener.ps1

# 3. Start the listener
.\jarvis_venv\Scripts\python.exe .\plugins\listener_bind_58563.py

# Or with logging:
.\jarvis_venv\Scripts\python.exe .\plugins\listener_bind_58563.py | Tee-Object -FilePath .\logs\listener_output.log
```

## ⚡ Quick Setup (Unix/Linux/macOS)

```bash
# 1. Navigate to brain directory
cd brain

# 2. Make setup script executable
chmod +x setup-listener.sh

# 3. Run automated setup
./setup-listener.sh

# 4. Start the listener
source jarvis_venv/bin/activate
python3 plugins/listener_bind_58563.py

# Or with logging:
python3 plugins/listener_bind_58563.py | tee logs/listener_output.log
```

## ✅ Verify It's Working

In another terminal, test the connection:

```bash
# Using netcat
echo "Hello Strategickhaos" | nc localhost 58563

# Expected response:
# [ACK] Hello Strategickhaos
```

## 🎯 What Happens During Setup

The setup script automatically:
1. ✅ Verifies Python 3 is installed
2. ✅ Creates `jarvis_venv/` virtual environment
3. ✅ Upgrades pip to latest version
4. ✅ Installs Flask and Requests libraries
5. ✅ Creates `logs/` directory for output

## 📊 Expected Output

When the listener starts, you should see:

```
[2025-11-19 16:22:28] 🔊 Strategickhaos Listener active on 0.0.0.0:58563
[2025-11-19 16:22:28] ✅ Socket bound and listening for connections...
```

When a connection is made:

```
[2025-11-19 16:23:11] 🧠 Connection established with: ('127.0.0.1', 52958)
[2025-11-19 16:23:11] 📥 Received: Hello Strategickhaos
[2025-11-19 16:23:11] 📤 Sent: [ACK] Hello Strategickhaos
```

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Check what's using port 58563
# Linux/macOS:
lsof -i :58563

# Windows:
netstat -ano | findstr :58563
```

### Python Not Found

**Windows**: Install from [python.org](https://www.python.org/downloads/) and ensure "Add to PATH" is checked

**Linux/macOS**: 
```bash
# Ubuntu/Debian
sudo apt install python3 python3-venv

# macOS
brew install python3
```

### Virtual Environment Already Exists

If you need to recreate the environment:

**Windows**:
```powershell
Remove-Item -Recurse -Force jarvis_venv
.\setup-listener.ps1
```

**Unix/Linux**:
```bash
rm -rf jarvis_venv
./setup-listener.sh
```

## 🔒 Security Notes

⚠️ **The listener binds to all network interfaces (0.0.0.0) by default.** This is for development and integration with external systems.

For production or local-only use, edit `plugins/listener_bind_58563.py`:
```python
HOST = '127.0.0.1'  # Change from '0.0.0.0' to '127.0.0.1'
```

## 🎮 Next Phase

Once your listener is running successfully, you're ready for:

**Phase 2: glyph_controller_bindings.cpp**

This will enable streaming glyph inputs to your listener!

## 📚 Full Documentation

For complete documentation, see: `brain/README.md`

---

**Strategickhaos Sovereignty Architecture** | Built for the future 🚀
