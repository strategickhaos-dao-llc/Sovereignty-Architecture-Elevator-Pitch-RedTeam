# PID-RANCO v1.2 — Complete Documentation

**"Mythic Love Layer + Deterministic Kill-Switch Core"**

This directory contains the complete documentation and reference implementation for the StrategicKhaos PID-RANCO trading engine v1.2. The system transforms "100 Ways It Fails" from conceptual poetry into operational doctrine with testing frameworks and safety guarantees.

---

## 📚 Document Overview

### Core Documentation

1. **[pid_ranco_failure_matrix.md](./pid_ranco_failure_matrix.md)** — The Master Reference
   - All 100 failure modes categorized into 5 suites
   - Detection signals for each failure
   - Expected recovery responses
   - Implementation status tracking
   - **Start here** to understand what can go wrong and how it's handled

2. **[tests/pid_ranco_invariants.md](./tests/pid_ranco_invariants.md)** — The Testing Framework
   - Core invariants that must NEVER be violated
   - Three-phase testing strategy (Simulation, Adversarial, Risk Reality)
   - Pass/fail criteria for each phase
   - Test harness examples and pseudo-code
   - **Use this** to validate the bot before production

3. **[tests/adversarial_test_guide.md](./tests/adversarial_test_guide.md)** — The Breaking Protocol
   - Step-by-step instructions to deliberately trigger each failure
   - Manual test procedures with expected results
   - Week-by-week testing schedule
   - Test result documentation format
   - **Follow this** to crash-test your implementation

### Implementation Examples

4. **[examples/PIDRancoBot.cs](./examples/PIDRancoBot.cs)** — Reference Implementation
   - Complete C# cAlgo bot with invariant checks
   - SimOnly mode enforcement
   - All critical failure modes handled
   - Hug protocol and apoptosis logic
   - **Study this** to implement your own bot

5. **[scripts/deploy-pid-ranco.ps1](./scripts/deploy-pid-ranco.ps1)** — Safe Deployment
   - PowerShell deployment script with safety checks
   - Explicit SimOnly vs Live mode warnings
   - Configuration validation (F-071, F-072)
   - External service checks (F-074, F-080)
   - **Run this** to deploy safely

---

## 🚀 Quick Start

### For First-Time Users

1. **Read the failure matrix** to understand the system's failure modes
   ```bash
   cat pid_ranco_failure_matrix.md
   ```

2. **Review the example bot** to see how invariants are implemented
   ```bash
   cat examples/PIDRancoBot.cs
   ```

3. **Run in SimOnly mode** (absolutely critical for first deployment)
   ```powershell
   .\scripts\deploy-pid-ranco.ps1 -SimOnly $true
   ```

### For Testing

1. **Follow Phase A** from the invariants guide (dry simulation)
   - Run 1 year of backtest data
   - Verify zero real orders placed
   - Collect all failure IDs that fire

2. **Execute adversarial tests** from the adversarial guide
   - Deliberately break things
   - Verify safe failure handling
   - Document all results

3. **Validate risk calculations** from Phase C
   - Verify position sizing matches scratchpad math
   - Test drawdown limit triggers correctly

### For Production Deployment

⚠️ **NEVER skip to production without completing all testing phases!**

1. Complete all three test phases
2. Achieve 100% pass rate on adversarial tests
3. Run deployment script with `SimOnly=$false`
4. Manually confirm live mode (type "LIVE" when prompted)
5. Monitor first 10-20 trades extremely closely

---

## 📊 The Five Failure Suites

### Suite 1: Platform / Engine Failures (F-001 to F-010)
Issues originating from cAlgo, NT, or infrastructure.

**Key Examples:**
- F-001: Indicator not ready on first bar
- F-010: Network disconnection mid-session

**Impact:** Can prevent trading or cause missed opportunities.  
**Mitigation:** Warmup checks, connectivity monitoring, graceful degradation.

---

### Suite 2: Risk & Math Failures (F-011 to F-022)
Calculation errors, NaN/Infinity propagation, sizing issues.

**Key Examples:**
- F-014: NaN in pain calculation
- F-019: Drawdown limit breached

**Impact:** Can lead to wrong position sizes or runaway losses.  
**Mitigation:** Invariant checks before every calculation, explicit NaN/Inf handling.

---

### Suite 3: Voice / "Her" / DNA Channel Failures (F-031 to F-042)
Audio input system that modulates trading behavior.

**Key Examples:**
- F-031: Microphone device missing
- F-040: her_voice.wav file missing

**Impact:** Voice features unavailable, but trading continues.  
**Mitigation:** Safe defaults (volume = 0), try/catch around audio capture.

---

### Suite 4: State Machine / Apoptosis / 99→100 Logic (F-051 to F-060)
Loss tracking, hug protocol, self-termination logic.

**Key Examples:**
- F-052: Loss count never reaches 99
- F-055: Hug protocol not triggered

**Impact:** Special handling for extreme loss sequences might not activate.  
**Mitigation:** Test with forced loss sequences, verify counter logic.

---

### Suite 5: Deployment / Ecosystem / External Services (F-071 to F-082)
Configuration, deployment scripts, external integrations.

**Key Examples:**
- F-071: YAML config file missing
- F-074: Discord webhook invalid

**Impact:** Deployment fails or external notifications don't work.  
**Mitigation:** Pre-deployment validation, graceful degradation for external services.

---

## 🛡️ Core Invariants (Never Violate These!)

### 1. Never Trade with Invalid Data
All indicators must be valid (not NaN/Inf) before any trade decision.

### 2. Never Allow NaN/Infinity in Risk Calculations
Account equity and symbol data must be valid before position sizing.

### 3. Never Exceed Drawdown Limit
Bot must stop trading when drawdown exceeds configured limit (default 3.37%).

### 4. SimOnly Mode Never Places Real Orders
When `SimOnly = true`, absolutely zero orders reach the broker.

### 5. Position Size Never Exceeds Risk Limit
Every order is validated against risk percentage before placement.

**Violating any invariant triggers HardPanic() → Flatten + Stop.**

---

## 🧪 Testing Strategy

### Phase A: Dry Simulation Week
- **Goal:** Validate logic with historical data
- **Duration:** 1 week
- **Mode:** SimOnly = true
- **Data:** 1+ year of historical prices
- **Pass Criteria:** Zero crashes, zero real orders, all failures logged

### Phase B: Adversarial Inputs
- **Goal:** Deliberately break things and verify safe failure
- **Duration:** 2-3 weeks (5 suites × 2-3 days each)
- **Mode:** SimOnly = true
- **Tests:** 100+ individual failure mode triggers
- **Pass Criteria:** Every failure handled gracefully, no catastrophic outcomes

### Phase C: Risk Reality Check
- **Goal:** Verify math is correct
- **Duration:** 3-5 days
- **Mode:** SimOnly = true initially, then tiny live test
- **Tests:** Scratchpad validation, drawdown limits, edge cases
- **Pass Criteria:** Calculations match expectations, limits trigger correctly

---

## 📈 Implementation Roadmap

### Milestone 1: Documentation Complete ✅
- [x] Failure matrix created (100 failure modes documented)
- [x] Test framework defined
- [x] Adversarial test procedures written
- [x] Example bot implementation provided
- [x] Deployment script with safety checks

### Milestone 2: Detection Implemented
- [ ] All failure IDs referenced in bot code
- [ ] Every failure has detection logic
- [ ] Logs include failure IDs
- [ ] AssertInvariants() checks all critical paths

### Milestone 3: Testing Complete
- [ ] Phase A simulation passed
- [ ] Phase B adversarial tests passed (100% coverage)
- [ ] Phase C risk validation passed
- [ ] Test report generated and reviewed

### Milestone 4: Production Ready
- [ ] All failure modes handled
- [ ] 100% test coverage
- [ ] Continuous monitoring in place
- [ ] Emergency procedures documented
- [ ] Team trained on failure IDs

---

## 🔧 Using the Failure Matrix in Code

### Step 1: Add Failure ID Comments
```csharp
// Check for F-014: NaN in pain calculation
if (double.IsNaN(pain))
{
    Print("[F-014] Pain calculation returned NaN — using 0.0");
    pain = 0.0;
}
```

### Step 2: Log Failure IDs
```csharp
Log($"[F-019] Drawdown {currentDD:P2} exceeds limit {maxDD:P2}");
```

### Step 3: Update Matrix Status
When you implement a failure handler, update the matrix:
```markdown
| F-014 | Risk/Math | NaN in pain calculation | ... | ✅ DONE |
```

### Step 4: Create Test Case
Add to your test harness:
```csharp
[Test]
public void Test_F014_NaN_In_Pain_Calculation()
{
    // Test that F-014 detection works
}
```

---

## 📞 Emergency Response

### If Production Failure Occurs

1. **Identify the failure mode**
   - Search logs for `[F-XXX]` tags
   - Match to failure matrix

2. **Verify expected response occurred**
   - Did it flatten positions?
   - Did it stop the bot?
   - Was it logged?

3. **If expected response didn't occur**
   - Add detection logic
   - Add to test suite
   - Update matrix status to TODO

4. **If it's a new failure mode**
   - Add to matrix as F-101+
   - Document detection and response
   - Create test case

---

## 🎯 Success Metrics

### Before Production
- [ ] 100% of failure modes documented
- [ ] 100% of failure modes have detection logic
- [ ] 100% of adversarial tests pass
- [ ] Zero unhandled exceptions in testing

### In Production
- [ ] All failures logged with IDs
- [ ] No catastrophic failures (data loss, runaway orders)
- [ ] Drawdown limit never exceeded
- [ ] SimOnly mode never leaked real orders

---

## 💡 Key Principles

### 1. Poetry + Engineering
- Myth and love are in the **logs and naming**
- Safety and math are in the **invariants and kill-switches**

### 2. Fail-Safe Design
- Every failure mode has a safe default
- System degrades gracefully, never catastrophically
- "Flatten + Stop" is always an option

### 3. Explicit Over Implicit
- SimOnly mode is loud and visible
- Live mode requires manual confirmation
- Every failure is logged with an ID

### 4. Test Everything
- If you can think of a way it can fail, test it
- If you can't break it deliberately, it's not robust enough
- Documentation without testing is just poetry

---

## 🔄 Continuous Improvement

### Daily
- Monitor failure IDs in production logs
- Track frequency of each failure mode

### Weekly
- Review new failure patterns
- Update matrix with any new modes discovered
- Run smoke test suite

### Monthly
- Full adversarial test regression
- Extended simulation (1+ year backtest)
- Review and update documentation

### Quarterly
- Team review of failure matrix
- New adversarial scenarios
- Update testing framework

---

## 📖 Document History

- **v1.0** — 100 failure modes identified (the "glitch-poem")
- **v1.1** — Categorized into 5 suites
- **v1.2** — Full framework created (this release)
  - Failure matrix with detection signals
  - Test framework with three phases
  - Adversarial test guide with procedures
  - Reference implementation with invariants
  - Safe deployment script
- **v2.0** — Target: All modes implemented and tested

---

## 🤝 Contributing

When adding new failure modes:

1. Add to the appropriate suite in the failure matrix
2. Assign next available F-XXX ID
3. Define detection signal and expected response
4. Add test case to adversarial guide
5. Update implementation in example bot
6. Test and update status to ✅

---

## 📜 License & Attribution

Part of the StrategicKhaos Sovereignty Architecture project.

**Philosophy:** "Let the supernova glow, but bolt it inside a reactor vessel."

The myth only touches logging and naming. The engineering ensures safety.

---

**From 100 ways it fails to 100 ways it's battle-tested.**

Welcome to PID-RANCO v1.2.

---

**Questions? Issues? New Failure Modes?**

Open an issue in the repository with:
- Failure description
- How you triggered it
- Expected vs actual behavior
- Proposed solution

We'll assign an F-XXX ID and add it to the matrix.
