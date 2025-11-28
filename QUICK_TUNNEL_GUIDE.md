# ⚡ Quick Tunnel Reference Card

## The 12-Second Path to Global Visibility

### Problem
`ERR_NGROK_4018` - ngrok now requires account verification + authtoken for free tier.

### Solution
**Cloudflare Tunnel** - No account, no token, no limits, instant HTTPS.

---

## 🏃 Fastest Path (Choose Your OS)

### Windows (PowerShell)
```powershell
# Install (one time)
winget install cloudflare.cloudflared

# Start tunnel
cloudflared tunnel --url http://localhost:3000

# Or use our script
./setup-tunnel.ps1
```

### Linux/Mac (Bash)
```bash
# Install (one time)
# macOS:
brew install cloudflare/cloudflare/cloudflared

# Debian/Ubuntu:
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb
sudo dpkg -i cloudflared.deb

# Start tunnel
cloudflared tunnel --url http://localhost:3000

# Or use our script
./setup-tunnel.sh
```

---

## 📦 What You Get

```
Input:  http://localhost:3000
Output: https://transcendental-rotation-authority-a1b2.trycloudflare.com

✅ HTTPS by default
✅ Works through firewalls
✅ No port forwarding needed
✅ Unlimited bandwidth
✅ Stays up as long as process runs
```

---

## 🎯 Common Use Cases

### Tunnel Different Ports
```bash
# Port 8080
cloudflared tunnel --url http://localhost:8080

# Custom host
cloudflared tunnel --url http://127.0.0.1:3000

# Using scripts
./setup-tunnel.sh 8080              # Linux/Mac
./setup-tunnel.ps1 -Port 8080       # Windows
```

### Multiple Tunnels
```bash
# Terminal 1: Frontend
cloudflared tunnel --url http://localhost:3000

# Terminal 2: Backend API
cloudflared tunnel --url http://localhost:8000

# Terminal 3: WebSocket Server
cloudflared tunnel --url http://localhost:9000
```

### Tunnel Docker Services
```bash
# Start your Docker service
docker compose up -d

# Tunnel it
cloudflared tunnel --url http://localhost:3000
```

---

## 🔧 Troubleshooting

### "cloudflared: command not found"
**Windows:**
```powershell
# Reinstall
winget install cloudflare.cloudflared

# Or restart PowerShell
```

**Linux/Mac:**
```bash
# Check installation
which cloudflared

# If not found, reinstall using method above
```

### "Connection refused"
```bash
# Check if your service is running
curl http://localhost:3000

# Check what's listening on the port
# Windows:
netstat -ano | findstr :3000

# Linux/Mac:
lsof -i :3000
```

### "URL not loading"
- Wait 10-15 seconds for DNS propagation
- Try from different device/network
- Check cloudflared terminal for errors

---

## 🎭 Alternative: ngrok (If You Need Static Domain)

```bash
# 1. Sign up: https://dashboard.ngrok.com/signup
# 2. Get token: https://dashboard.ngrok.com/get-started/your-authtoken
# 3. Configure
ngrok config add-authtoken YOUR_TOKEN

# 4. Start with reserved domain
ngrok http 3000 --domain=your-domain.ngrok.app
```

Free tier gives you **one permanent reserved domain** + HTTPS.

---

## 📚 More Info

- **Full Guide**: [TUNNEL_SETUP.md](./TUNNEL_SETUP.md)
- **Cloudflare Docs**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- **ngrok Docs**: https://ngrok.com/docs

---

## 🚀 Pro Tips

1. **Keep Terminal Open**: Tunnel stops when terminal closes
2. **Use tmux/screen**: For persistent tunnels on Linux
3. **Check Logs**: cloudflared shows all requests in terminal
4. **Share URL**: Copy the .trycloudflare.com URL and share away
5. **Production?**: Use DigitalOcean droplet ($6/mo) for permanent hosting

---

**No signup. No token. No bill. No 4018.**

The bamboo approves. 🎋

---

*Built with 🔥 by the Strategickhaos Swarm Intelligence collective*
