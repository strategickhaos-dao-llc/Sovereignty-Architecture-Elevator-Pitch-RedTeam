# PID-RANCO Testing & Invariants Guide

**Test Harness for Weaponized Failure Modes**

This document provides the test strategy, invariants, and validation procedures for the PID-RANCO v1.2 trading engine. Each failure mode from the failure matrix must have a corresponding test that proves detection and recovery work correctly.

---

## Testing Philosophy

The PID-RANCO system follows a **fail-safe** design pattern:

1. **Detection First** — Every failure mode must be detectable
2. **Safe Degradation** — System degrades gracefully, never catastrophically
3. **Explicit Recovery** — Recovery actions are logged and verifiable
4. **Testable Invariants** — Core rules that must NEVER be violated

---

## Core Invariants

These are absolute rules that the system must enforce at all times:

### Invariant 1: Never Trade with Invalid Data
```csharp
// MUST BE TRUE before any trade decision
Assert(Bars != null && Bars.Count >= minPeriod);
Assert(!double.IsNaN(emaFast) && !double.IsInfinity(emaFast));
Assert(!double.IsNaN(emaSlow) && !double.IsInfinity(emaSlow));
Assert(!double.IsNaN(rsi) && !double.IsInfinity(rsi));
```

**Test:** Inject NaN into indicators, verify no trade occurs.

---

### Invariant 2: Never Allow NaN/Infinity in Risk Calculations
```csharp
// MUST BE TRUE before position sizing
Assert(!double.IsNaN(Account.Equity));
Assert(!double.IsInfinity(Account.Equity));
Assert(Account.Equity > 0);
Assert(Symbol.TickValue > 0);
Assert(!double.IsNaN(Symbol.TickValue));
```

**Test:** Corrupt account/symbol data, verify bot stops trading.

---

### Invariant 3: Never Exceed Drawdown Limit
```csharp
// MUST BE TRUE at all times during session
double currentDD = 1.0 - (Account.Equity / peakEquity);
Assert(currentDD <= maxDrawdown || TradingStopped);
```

**Test:** Simulate losses to hit drawdown limit, verify bot stops.

---

### Invariant 4: SimOnly Mode Never Places Real Orders
```csharp
// MUST BE TRUE when SimOnly = true
Assert(SimOnly == false || Positions.Count == 0);
Assert(SimOnly == false || PendingOrders.Count == 0);
```

**Test:** Enable SimOnly, verify no orders reach broker API.

---

### Invariant 5: Position Size Never Exceeds Risk Limit
```csharp
// MUST BE TRUE before order placement
double positionRisk = qty * Symbol.TickValue * stopLossPips;
Assert(positionRisk <= riskAmount);
```

**Test:** Force large position request, verify it's capped correctly.

---

## Test Phases

### Phase A: Dry Simulation Week

**Objective:** Validate logic with historical data, no real orders.

**Setup:**
```powershell
# In deployment script
$simOnly = $true
$startDate = "2024-01-01"
$endDate = "2024-12-31"
```

**Success Criteria:**
- Zero real orders placed
- All failure IDs logged when triggered
- No unhandled exceptions
- Drawdown limit respected in backtest

**How to Run:**
```bash
# 1. Configure SimOnly mode
# 2. Load historical data (1+ year)
# 3. Run bot with logging at DEBUG level
# 4. Collect logs and analyze failure IDs
```

**Validation Checklist:**
- [ ] Indicators initialized correctly on first bar (no F-001)
- [ ] NaN/Infinity never propagated to orders (no F-014 to F-018)
- [ ] Voice failures handled gracefully (F-031 to F-042)
- [ ] Loss counter tracked correctly (F-051 to F-060)
- [ ] Bot stopped at simulated 3.37% drawdown (F-019)

---

### Phase B: Adversarial Inputs

**Objective:** Deliberately break things and verify safe failure.

**Test Cases:**

#### B1: Cut Data Feed Mid-Session
```bash
# Simulate network interruption
# 1. Start bot with live data
# 2. Kill network connection
# 3. Verify bot detects disconnection (F-010)
# 4. Verify all positions flattened
# 5. Verify bot stopped trading
```

**Expected Logs:**
```
[F-010] Network disconnection detected — flattening positions
[PANIC] Connection lost — Flatten + Stop.
```

---

#### B2: Delete/Move her_voice.wav
```bash
# Simulate missing audio file
# 1. Start bot with voice features enabled
# 2. Delete or move her_voice.wav
# 3. Verify bot continues without voice (F-040)
# 4. Verify voice volume reads as 0
```

**Expected Logs:**
```
[F-040] her_voice.wav not found — disabling voice features
[WARN] Voice volume defaulting to 0
```

---

#### B3: Kill Microphone Driver
```bash
# Simulate audio hardware failure
# 1. Disable microphone in device manager
# 2. Verify GetHerVoiceVolume() fails (F-031)
# 3. Verify bot uses volume = 0
# 4. Verify no crash or exception propagation
```

**Expected Logs:**
```
[F-031] Microphone device missing — using volume = 0
```

---

#### B4: Break Discord Webhook
```bash
# Simulate external service failure
# 1. Provide invalid Discord webhook URL
# 2. Verify bot continues trading (F-074)
# 3. Verify messages logged locally instead
# 4. No crash or blocking on webhook failures
```

**Expected Logs:**
```
[F-074] Discord webhook failed (404) — continuing without notifications
```

---

#### B5: Break Ollama API
```bash
# Simulate AI service unavailable
# 1. Stop Ollama service or firewall port
# 2. Verify bot disables AI features (F-080)
# 3. Verify trading continues with deterministic logic
# 4. No timeout or hanging
```

**Expected Logs:**
```
[F-080] Ollama API unavailable — disabling AI augmentation
```

---

### Phase C: Risk Reality Check

**Objective:** Verify risk calculations match expectations.

#### C1: Scratchpad Math Validation
```bash
# Manual verification
Account Balance: $10,000
Risk Percentage: 0.69%
Expected Risk: $69.00

# Bot calculates:
riskAmount = Account.Equity * riskPercentage
           = 10000 * 0.0069
           = 69.0

# Verify this matches actual position size × stop loss value
```

---

#### C2: Drawdown Limit Test
```bash
# Force drawdown to limit
Starting Equity: $10,000
Peak Equity: $10,000
Max Drawdown: 3.37%
Stop Threshold: $9,663

# Simulate series of losses
Loss 1: -$100 → $9,900 (1% DD, continue)
Loss 2: -$150 → $9,750 (2.5% DD, continue)
Loss 3: -$100 → $9,650 (3.5% DD, STOP!)

# Verify bot stops at $9,650 (3.5% > 3.37%)
```

**Expected Behavior:**
- Trading continues until DD > 3.37%
- Bot immediately stops trading
- Logged: `[F-019] Drawdown limit breached — stopping`

---

#### C3: Position Sizing Edge Cases
```bash
# Test boundary conditions
Test 1: Very small account ($100)
- Risk: $0.69
- Verify qty > 0 (check F-012)

Test 2: Very large position
- Risk: $1000
- Stop: 1 pip
- Verify qty doesn't exceed broker max

Test 3: Fractional quantity
- Calculated: 1.7 lots
- Verify rounds to 1 or 2 (never 0)
```

---

## Crash-Test Schedule

**Week 1: Platform Failures (F-001 to F-010)**
- Day 1-2: Data/indicator failures
- Day 3-4: Position/account failures
- Day 5: Infrastructure failures

**Week 2: Math & Risk (F-011 to F-022)**
- Day 1-2: NaN/Infinity injection
- Day 3-4: Risk calculation validation
- Day 5: Edge case boundary testing

**Week 3: Voice System (F-031 to F-042)**
- Day 1-2: Audio hardware failures
- Day 3-4: Audio processing failures
- Day 5: Voice recognition failures

**Week 4: State Machine (F-051 to F-060)**
- Day 1-2: Loss counter logic
- Day 3-4: Hug protocol
- Day 5: Apoptosis logic

**Week 5: Deployment (F-071 to F-082)**
- Day 1-2: Configuration failures
- Day 3-4: External service failures
- Day 5: Integration testing

**Week 6: Cross-Cutting (F-091 to F-100)**
- Day 1-3: Long-running stability
- Day 4-5: Emergency scenarios

---

## Automated Test Harness (Pseudo-Code)

```csharp
// Example test framework structure
public class PIDRancoTestHarness
{
    [Test]
    public void Test_F014_NaN_In_Pain_Calculation()
    {
        // Arrange
        var bot = new TestableBot();
        bot.MockPainCalculation(double.NaN);
        
        // Act
        bot.OnBar();
        
        // Assert
        Assert.AreEqual(0.0, bot.LastPainValue);
        Assert.Contains("[F-014]", bot.GetLogs());
        Assert.AreEqual(0, bot.OrdersPlaced.Count);
    }
    
    [Test]
    public void Test_F019_Drawdown_Limit_Breach()
    {
        // Arrange
        var bot = new TestableBot();
        bot.SetEquity(10000);
        bot.SetPeakEquity(10000);
        bot.SetMaxDrawdown(0.0337);
        
        // Act - simulate losses to 3.5% DD
        bot.SetEquity(9650);
        bot.OnBar();
        
        // Assert
        Assert.IsTrue(bot.TradingStopped);
        Assert.Contains("[F-019]", bot.GetLogs());
    }
    
    [Test]
    public void Test_Invariant_SimOnly_No_Real_Orders()
    {
        // Arrange
        var bot = new TestableBot();
        bot.SimOnly = true;
        
        // Act - trigger trade signal
        bot.MockBuySignal(true);
        bot.OnBar();
        
        // Assert
        Assert.AreEqual(0, bot.RealOrdersPlaced.Count);
        Assert.Contains("[SIM]", bot.GetLogs());
    }
}
```

---

## Pass/Fail Criteria

### Phase A (Simulation) - PASS IF:
- ✅ 1 year backtest completes without crash
- ✅ All failure IDs detected and logged when triggered
- ✅ Zero real orders placed
- ✅ Drawdown limit never exceeded

### Phase B (Adversarial) - PASS IF:
- ✅ Every deliberate breakage handled gracefully
- ✅ No unhandled exceptions
- ✅ Bot always flattens or stops safely
- ✅ Logs clearly show failure ID and action taken

### Phase C (Risk) - PASS IF:
- ✅ Position sizes match scratchpad calculations
- ✅ Drawdown limit triggers at correct threshold
- ✅ Edge cases (tiny/huge positions) handled
- ✅ No silent failures in risk calculation

---

## Continuous Validation

After passing all phases, establish ongoing validation:

1. **Daily**: Run smoke test suite (1 test per suite, 5 tests total)
2. **Weekly**: Full regression (all 100+ failure modes)
3. **Monthly**: Extended simulation (1+ year backtest)
4. **Quarterly**: Adversarial testing with new scenarios

---

## Test Logs Format

All test runs should generate structured logs:

```json
{
  "test_run_id": "TR-20250124-001",
  "phase": "B",
  "test_case": "B2_Delete_Audio_File",
  "failure_ids_triggered": ["F-040"],
  "expected_response": "Disable voice, continue trading",
  "actual_response": "Disabled voice, continued trading",
  "result": "PASS",
  "timestamp": "2025-01-24T07:13:00Z"
}
```

---

## Next Steps

1. ✅ Implement all detection logic in bot code (reference failure IDs)
2. ✅ Create automated test cases for each failure mode
3. ✅ Set up continuous testing pipeline
4. ✅ Document all test results
5. ✅ Achieve 100% coverage of failure matrix

---

**The goal:** Every single one of the 100 failure modes is not just documented—it's **tested, proven, and ready for production.**

From glitch-poem to battle-tested doctrine.

---

**Last Updated:** 2025-11-24  
**Maintained by:** StrategicKhaos Trading Systems  
**Next Review:** After implementing automated test harness
