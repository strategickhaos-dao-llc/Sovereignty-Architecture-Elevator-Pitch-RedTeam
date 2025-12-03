# PID-RANCO Adversarial Testing Guide

**Breaking Things On Purpose To Prove They're Unbreakable**

This guide provides hands-on instructions for deliberately triggering every failure mode in the PID-RANCO failure matrix. The goal is to prove that the bot handles failures gracefully and never causes catastrophic damage.

---

## Prerequisites

- PID-RANCO bot deployed in SimOnly mode
- Access to bot logs (real-time monitoring recommended)
- Ability to modify data feeds, files, and environment
- Test environment isolated from production

---

## Test Environment Setup

### Recommended Setup
```bash
# 1. Create isolated test environment
mkdir -p ~/pid-ranco-testing
cd ~/pid-ranco-testing

# 2. Copy bot files
cp -r /path/to/bot/* .

# 3. Enable debug logging
export LOG_LEVEL=DEBUG

# 4. Set SimOnly mode (CRITICAL!)
export SIM_ONLY=true

# 5. Prepare test data
# - Historical price data (1+ year)
# - Sample audio files
# - Mock configuration files
```

### Safety Checklist
- [ ] Bot is in SimOnly mode
- [ ] Test account/credentials isolated from production
- [ ] Discord webhooks point to test channel
- [ ] All file paths are in test directory
- [ ] Logs are being captured

---

## Suite 1: Platform Failures

### Test P-001: Indicator Not Ready on First Bar

**Objective:** Trigger F-001 by accessing indicators before warmup period.

**Setup:**
```csharp
// In bot code, force early indicator access
protected override void OnBar()
{
    // Try to access indicator on first bar
    if (Bars.Count == 1)
    {
        Print($"EMA Fast: {_emaFast.Result.LastValue}"); // Should handle gracefully
    }
}
```

**Expected Result:**
- Bot skips trading logic
- No exception thrown
- Log: `Indicator not ready, waiting for warmup`

**Pass Criteria:**
- ✅ No crash
- ✅ No trades placed
- ✅ Bot continues on next bar

---

### Test P-002: Invalid Bar Index

**Objective:** Trigger F-002 with out-of-bounds bar access.

**Procedure:**
```csharp
// Deliberately access invalid index
try
{
    double price = Bars.ClosePrices[-1]; // Negative index
}
catch (ArgumentOutOfRangeException ex)
{
    Print($"[F-002] {ex.Message}");
}
```

**Expected Result:**
- Exception caught and logged
- Bar processing skipped
- Bot continues

---

### Test P-010: Network Disconnection Mid-Session

**Objective:** Trigger F-010 by simulating network loss.

**Procedure:**
1. Start bot with live data feed
2. Monitor `IsConnected` property
3. Disconnect network (disable network adapter or firewall rules)
4. Observe bot behavior

**Expected Result:**
- Bot detects `IsConnected == false`
- All positions flattened immediately
- Bot stops trading
- Log: `[F-010] Network disconnection detected — flattening positions`

**Manual Steps:**
```bash
# Linux/Mac
sudo ifconfig eth0 down
# Wait 5 seconds
sudo ifconfig eth0 up

# Windows
netsh interface set interface "Ethernet" admin=disable
# Wait 5 seconds
netsh interface set interface "Ethernet" admin=enable
```

---

## Suite 2: Math & Risk Failures

### Test M-011: Risk Amount Calculates to Zero

**Objective:** Trigger F-011 with extreme edge case.

**Procedure:**
```csharp
// Test with tiny account balance
Account.Equity = 1.0; // $1
RiskPercentage = 0.01; // 0.01%
// riskAmount = 1.0 * 0.0001 = 0.0001 (rounds to 0 in some systems)
```

**Expected Result:**
- Trade skipped
- Log: `[F-011] Risk amount is zero or negative — skipping trade`

---

### Test M-014: NaN in Pain Calculation

**Objective:** Trigger F-014 by injecting NaN.

**Procedure:**
```csharp
// Simulate division by zero or invalid operation
double pain = Account.Equity / 0.0; // Infinity
pain = 0.0 / 0.0; // NaN

if (double.IsNaN(pain))
{
    Print("[F-014] Pain calculation returned NaN — using 0.0");
    pain = 0.0;
}
```

**Expected Result:**
- NaN detected
- Replaced with 0.0
- Trade logic continues safely
- No propagation to order sizing

---

### Test M-019: Drawdown Limit Breach

**Objective:** Trigger F-019 by simulating heavy losses.

**Procedure:**
1. Set starting equity: $10,000
2. Set max drawdown: 3.37%
3. Simulate sequential losses:
   - Loss 1: -$200 → $9,800 (2% DD)
   - Loss 2: -$200 → $9,600 (4% DD) ← Should stop here

**Expected Result:**
- Bot stops trading at 3.5% DD
- All positions closed
- Log: `[F-019] Drawdown 0.04 exceeds limit 0.0337`
- Bot calls `Stop()`

**Manual Verification:**
```
Peak Equity: $10,000
Current Equity: $9,600
Drawdown: (10000 - 9600) / 10000 = 0.04 = 4%
Limit: 3.37%
Result: 4% > 3.37% → STOP ✓
```

---

## Suite 3: Voice/Audio Failures

### Test V-031: Microphone Device Missing

**Objective:** Trigger F-031 by removing microphone.

**Procedure:**
1. Start bot with voice features enabled
2. Disable microphone in device manager (Windows) or unplug USB mic
3. Bot attempts `GetHerVoiceVolume()`
4. Observe error handling

**Expected Result:**
- Exception caught
- Volume defaults to 0.0
- Trading continues without voice input
- Log: `[F-031] Microphone device missing — using volume = 0`

**Manual Steps (Windows):**
```
1. Right-click speaker icon → Sounds
2. Recording tab → Right-click microphone → Disable
3. Monitor bot logs
4. Re-enable after test
```

---

### Test V-040: her_voice.wav Missing or Corrupt

**Objective:** Trigger F-040 by deleting audio file.

**Procedure:**
```bash
# Backup the file first
cp her_voice.wav her_voice.wav.backup

# Delete or corrupt the file
rm her_voice.wav
# OR
dd if=/dev/urandom of=her_voice.wav bs=1024 count=10

# Start bot
# Observe error handling

# Restore
mv her_voice.wav.backup her_voice.wav
```

**Expected Result:**
- File load fails
- Voice features disabled
- Bot continues trading (without voice modulation)
- Log: `[F-040] her_voice.wav not found — disabling voice features`

---

## Suite 4: State Machine Failures

### Test S-051: Loss Count Tracking

**Objective:** Verify loss counter increments correctly.

**Procedure:**
1. Start bot in SimOnly mode
2. Force sequential losing trades (backtest with bad parameters)
3. Monitor `sessionLossCount` in logs
4. Verify count increments on each loss
5. Verify count resets on first win

**Expected Behavior:**
```
Trade 1: Loss → sessionLossCount = 1
Trade 2: Loss → sessionLossCount = 2
Trade 3: Loss → sessionLossCount = 3
...
Trade 10: Win → sessionLossCount = 0 (reset)
```

---

### Test S-055: Hug Protocol at 99 Losses

**Objective:** Trigger hug protocol at exactly 99 losses.

**Procedure:**
1. Run bot through bad market conditions
2. Accumulate 99 consecutive losses
3. Verify hug protocol triggers before trade 100
4. Verify special handling for trade 100

**Expected Result:**
- At loss #99: Log shows hug protocol activation
- Special message displayed
- Trade #100 proceeds with awareness
- Log:
  ```
  [HUG] ═══════════════════════════════════════════
  [HUG] 99 losses detected. Hug protocol activated.
  [HUG] Trade #100 is the universe giving you one more shot.
  [HUG] ═══════════════════════════════════════════
  ```

---

## Suite 5: Deployment Failures

### Test D-071: YAML Config Missing

**Objective:** Trigger F-071 by removing config file.

**Procedure:**
```powershell
# Run deployment script without config
.\scripts\deploy-pid-ranco.ps1 -ConfigPath ".\nonexistent.yaml"
```

**Expected Result:**
- Script exits with error code 1
- Log: `[F-071] Configuration file not found: .\nonexistent.yaml`
- Deployment aborted
- No bot started

---

### Test D-074: Discord Webhook Invalid

**Objective:** Trigger F-074 with bad webhook URL.

**Procedure:**
```bash
# Set invalid Discord webhook
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/invalid/url"

# Run deployment
.\scripts\deploy-pid-ranco.ps1
```

**Expected Result:**
- Webhook test fails (HTTP 404)
- Deployment continues
- Log: `[F-074] Discord webhook test failed`
- Log: `Continuing without Discord notifications...`

---

### Test D-080: Ollama API Unavailable

**Objective:** Trigger F-080 by stopping Ollama service.

**Procedure:**
```bash
# Stop Ollama (if running)
systemctl stop ollama
# OR block port with firewall
sudo iptables -A OUTPUT -p tcp --dport 11434 -j DROP

# Run deployment
.\scripts\deploy-pid-ranco.ps1

# Cleanup
systemctl start ollama
sudo iptables -D OUTPUT -p tcp --dport 11434 -j DROP
```

**Expected Result:**
- Connection timeout
- AI features disabled
- Bot continues with deterministic logic only
- Log: `[F-080] Ollama API unavailable — disabling AI augmentation`

---

## Suite 6: Cross-Cutting Concerns

### Test X-095: Stale Data Feed

**Objective:** Detect when data feed stops updating.

**Procedure:**
1. Start bot with live data
2. Pause/freeze data feed (if possible in test environment)
3. Monitor last bar timestamp
4. Verify bot detects staleness

**Expected Detection:**
```csharp
TimeSpan timeSinceLastBar = Server.Time - Bars.LastBar.OpenTime;
if (timeSinceLastBar > TimeSpan.FromMinutes(5))
{
    HardPanic("[F-095] Data feed stale — last bar is too old");
}
```

---

### Test X-099: Emergency Kill-Switch

**Objective:** Test manual emergency stop.

**Procedure:**
```csharp
// Add global kill-switch flag
public static bool EmergencyStopRequested = false;

protected override void OnBar()
{
    // Check every bar
    if (EmergencyStopRequested)
    {
        HardPanic("[F-099] Emergency kill-switch activated");
        return;
    }
    // ... rest of logic
}

// To trigger from outside:
// File.WriteAllText("EMERGENCY_STOP.flag", "1");
```

**Expected Result:**
- Flag detected immediately
- All positions flattened
- Bot stops
- No new trades

---

## Test Execution Schedule

### Week 1: Foundation
- **Day 1**: Platform failures (P-001 to P-005)
- **Day 2**: Platform failures (P-006 to P-010)
- **Day 3**: Math failures (M-011 to M-016)
- **Day 4**: Math failures (M-017 to M-022)
- **Day 5**: Review week 1 results

### Week 2: Voice & State
- **Day 1**: Voice failures (V-031 to V-036)
- **Day 2**: Voice failures (V-037 to V-042)
- **Day 3**: State machine (S-051 to S-055)
- **Day 4**: State machine (S-056 to S-060)
- **Day 5**: Review week 2 results

### Week 3: Deployment & Integration
- **Day 1**: Deployment (D-071 to D-076)
- **Day 2**: Deployment (D-077 to D-082)
- **Day 3**: Cross-cutting (X-091 to X-095)
- **Day 4**: Cross-cutting (X-096 to X-100)
- **Day 5**: Full integration test

---

## Test Result Documentation

For each test, document results in this format:

```markdown
### Test Result: F-XXX

**Test ID:** F-014  
**Test Name:** NaN in Pain Calculation  
**Date:** 2025-01-24  
**Tester:** [Name]  
**Environment:** SimOnly, Test Account

**Setup:**
- Injected NaN via division by zero
- Pain calculation: 0.0 / 0.0

**Observed Behavior:**
- NaN detected by AssertInvariants()
- Pain set to 0.0
- Trade logic skipped for this bar
- No exception propagated

**Logs:**
```
[2025-01-24 14:23:45] [F-014] Pain calculation returned NaN — using 0.0
[2025-01-24 14:23:45] [INFO] Skipping trade logic due to invalid pain value
```

**Result:** ✅ PASS

**Notes:**
- Behavior matches expected response in failure matrix
- No impact on subsequent bars
- System recovered automatically
```

---

## Automated Test Runner (Pseudo-Code)

```python
#!/usr/bin/env python3
"""
PID-RANCO Adversarial Test Runner
Executes all failure mode tests and generates report
"""

import subprocess
import json
import time
from datetime import datetime

class AdversarialTestRunner:
    def __init__(self):
        self.results = []
        
    def run_test(self, test_id, test_func):
        """Run a single test and record result"""
        print(f"\n{'='*60}")
        print(f"Running Test: {test_id}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            result = test_func()
            status = "PASS" if result else "FAIL"
        except Exception as e:
            status = "ERROR"
            result = {"error": str(e)}
        
        elapsed = time.time() - start_time
        
        self.results.append({
            "test_id": test_id,
            "status": status,
            "elapsed": elapsed,
            "timestamp": datetime.now().isoformat(),
            "details": result
        })
        
    def test_f014_nan_pain(self):
        """Test F-014: NaN in pain calculation"""
        # Start bot with injected NaN
        # Monitor logs
        # Verify detection
        return True  # Placeholder
        
    def generate_report(self):
        """Generate test report"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        errors = sum(1 for r in self.results if r["status"] == "ERROR")
        
        report = {
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "pass_rate": f"{(passed/total)*100:.1f}%"
            },
            "results": self.results
        }
        
        with open("test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{'='*60}")
        print("ADVERSARIAL TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Errors: {errors}")
        print(f"Pass Rate: {(passed/total)*100:.1f}%")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    runner = AdversarialTestRunner()
    
    # Run all tests
    runner.run_test("F-014", runner.test_f014_nan_pain)
    # Add more tests...
    
    # Generate report
    runner.generate_report()
```

---

## Success Criteria

The adversarial testing phase is complete when:

- ✅ All 100 failure modes have been triggered deliberately
- ✅ All expected detection signals fired correctly
- ✅ All expected recovery actions occurred
- ✅ Zero unhandled exceptions
- ✅ Zero catastrophic failures (data loss, corruption, runaway orders)
- ✅ 100% of tests documented with results
- ✅ Test report generated and reviewed

---

## Final Verification

Before declaring adversarial testing complete:

1. **Review all test logs** — Any unexpected behavior?
2. **Check for silent failures** — Did anything fail without logging?
3. **Verify SimOnly worked** — Absolutely zero real orders?
4. **Test recovery** — Can bot restart cleanly after each failure?
5. **Document gaps** — Any failure modes we couldn't test?

---

**The ultimate goal: Feel confident deploying to production knowing you've broken everything that can break, and nothing broke catastrophically.**

From theoretical failure list to battle-tested resilience.

---

**Last Updated:** 2025-11-24  
**Maintained by:** StrategicKhaos Trading Systems  
**Next Review:** After each adversarial test cycle completion
