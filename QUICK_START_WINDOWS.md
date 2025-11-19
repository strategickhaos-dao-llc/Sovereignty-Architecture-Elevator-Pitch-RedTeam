# Quick Start: Windows Defender Override

## 🚀 One-Click Setup for Windows Development

This guide gets you running PowerShell scripts without Windows Defender prompts in under 2 minutes.

### ⚡ Fast Track (Copy-Paste Method)

1. **Open Administrator PowerShell**
   - Press `Win + X`
   - Click "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. **Navigate to project**
   ```powershell
   cd "C:\path\to\Sovereignty-Architecture-Elevator-Pitch-"
   ```

3. **Run the override**
   ```powershell
   .\defender-executive-override.ps1
   ```

4. **Type `YES` when prompted**

5. **Done!** No more security prompts for PowerShell scripts.

---

## 🔍 Safe Testing First (Recommended)

Before applying changes, test what will happen:

```powershell
# See what would change (no actual modifications)
.\defender-executive-override.ps1 -DryRun
```

Review the output, then run without `-DryRun` to apply.

---

## 📱 Quick Reference Commands

### Apply Override
```powershell
# Standard setup
.\defender-executive-override.ps1

# Custom project path
.\defender-executive-override.ps1 -ProjectPath "C:\MyProject"

# Skip real-time monitoring changes
.\defender-executive-override.ps1 -SkipRealtimeMonitoring
```

### Check Current Status
```powershell
# View all Defender exclusions
Get-MpPreference | Select-Object Exclusion*

# Check real-time protection status
Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled
```

### Remove Exclusions (Undo)
```powershell
# Remove specific path
Remove-MpPreference -ExclusionPath "C:\path\to\project"

# Remove .ps1 extension exclusion
Remove-MpPreference -ExclusionExtension ".ps1"

# Remove PowerShell process exclusions
Remove-MpPreference -ExclusionProcess "powershell.exe"
Remove-MpPreference -ExclusionProcess "pwsh.exe"

# Re-enable real-time monitoring
Set-MpPreference -DisableRealtimeMonitoring $false
```

---

## ⚠️ Important Notes

### Before You Start
- ✅ **Only use on personal development machines**
- ✅ **Understand this reduces system security**
- ✅ **Make sure you trust all code you'll be running**

### Don't Use If
- ❌ Corporate/managed device (check with IT first)
- ❌ Production server or shared computer
- ❌ System handles sensitive data (PII, financial, etc.)

---

## 🆘 Troubleshooting

### "Execution Policy" Error
```powershell
# Option 1: Bypass for this script only
PowerShell.exe -ExecutionPolicy Bypass -File .\defender-executive-override.ps1

# Option 2: Change policy (less secure)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Access Denied" or "Could not disable..."
1. Disable Tamper Protection manually:
   - Open Windows Security
   - Go to "Virus & threat protection" → "Manage settings"
   - Turn off "Tamper Protection"
2. Run the script again

### "Not running as administrator"
- You must run PowerShell as Administrator
- Right-click PowerShell and select "Run as administrator"

---

## 📚 More Information

- **Full Documentation**: [DEFENDER_OVERRIDE_GUIDE.md](DEFENDER_OVERRIDE_GUIDE.md)
- **Security Considerations**: See guide for risks and mitigations
- **Alternative Approaches**: Code signing, sandboxing, etc.

---

## ✅ Verification

After running the script, verify it worked:

```powershell
# Should show your project path
(Get-MpPreference).ExclusionPath

# Should show .ps1
(Get-MpPreference).ExclusionExtension

# Should show powershell.exe and pwsh.exe
(Get-MpPreference).ExclusionProcess
```

---

**Remember**: This is a development convenience tool. Use responsibly and only on machines you control.

For questions or issues, refer to [DEFENDER_OVERRIDE_GUIDE.md](DEFENDER_OVERRIDE_GUIDE.md) or open a GitHub issue.
