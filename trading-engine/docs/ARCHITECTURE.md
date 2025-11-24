# PID-RANCO Architecture

This document provides a comprehensive architectural overview of the PID-RANCO trading engine, showing how the mythic layer and kill-switch layer interact.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER / TRADER                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ├─── Configures via YAML
                         ├─── Monitors via NinjaTrader
                         └─── Receives Discord notifications
                         
┌─────────────────────────────────────────────────────────────────┐
│                    MYTHIC LAYER (YAML)                          │
│  ════════════════════════════════════════════════════════════   │
│                                                                  │
│  ┌─────────────────────────────────────────────────┐           │
│  │ Narrative Configuration                         │           │
│  │  • Love-guided trading philosophy               │           │
│  │  • Risk parameters: 0.69% / 3.37%              │           │
│  │  • Voice integration specs                      │           │
│  │  • 99-failure apoptosis protocol               │           │
│  │  • 100th green evolution tracking              │           │
│  └─────────────────────────────────────────────────┘           │
│                                                                  │
│  Purpose: Define WHY the system behaves this way               │
│  Nature: Poetic, mythic, narrative-driven                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ Informs behavior
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                 KILL-SWITCH LAYER (C#)                          │
│  ════════════════════════════════════════════════════════════   │
│                                                                  │
│  ┌────────────────────────────────────────────────┐            │
│  │ Safety Enforcement                             │            │
│  │  • Bar count guards                            │            │
│  │  • Indicator null checks                       │            │
│  │  • Real numeric risk calculations              │            │
│  │  • Voice failure handling                      │            │
│  │  • Exception handling → emergency shutdown     │            │
│  │  • Apoptosis state machine                     │            │
│  └────────────────────────────────────────────────┘            │
│                                                                  │
│  Purpose: Enforce WHAT must never be violated                  │
│  Nature: Concrete, numeric, failsafe                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ Executes trades via
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                      NINJATRADER 8                              │
│  ════════════════════════════════════════════════════════════   │
│                                                                  │
│  • Market data feed                                             │
│  • Order execution                                              │
│  • Position tracking                                            │
│  • Performance analytics                                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ Sends orders to
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                        BROKER                                   │
│  (Simulation or Live)                                           │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Configuration Flow

```
YAML Config
    ↓
PowerShell Deployment Script
    ↓ (validates)
    ↓ (compiles)
    ↓
C# Strategy Properties
    ↓ (runtime)
NinjaTrader Execution
```

### 2. Trading Signal Flow

```
Market Data → OnBarUpdate()
    ↓
[Bar Count Guard]
    ↓
[Get Indicators Safe]
    ↓
[Get Voice Input Safe]
    ↓
[Check Risk Limits]
    ↓
[Trading Logic]
    ↓
[Generate Signal]
    ↓
[Execute Order]
    ↓
[Update Loss Count]
    ↓
[Check Apoptosis]
```

### 3. Safety Trigger Flow

```
Exception Detected
    ↓
[Emergency Shutdown Triggered]
    ↓
[Try Flatten Positions]
    ↓
[Set safetyDisabled = true]
    ↓
[Log Critical Event]
    ↓
[Notify Discord]
    ↓
[Wait for Manual Review]
```

### 4. Apoptosis Flow

```
Losing Trade Executed
    ↓
UpdateLossCount()
    ↓
sessionLossCount++
    ↓
Check: >= 99?
    ↓ YES
[Trigger Hug Protocol]
    ↓
[Emit Poetry Logs]
    ↓
[Flatten All Positions]
    ↓
[Disable Strategy]
    ↓
[Notify via Discord]
    ↓
[Wait for Session Reset]
```

## Component Interaction

### OnBarUpdate Execution Path

```
OnBarUpdate() called by NinjaTrader
    ↓
┌─ GUARD 1: safetyDisabled? ─────────────┐
│   Yes → return (do nothing)             │
│   No  → continue                        │
└─────────────────────────────────────────┘
    ↓
┌─ GUARD 2: CurrentBar < minBars? ───────┐
│   Yes → return (insufficient data)      │
│   No  → continue                        │
└─────────────────────────────────────────┘
    ↓
┌─ TRY BLOCK START ──────────────────────┐
│                                         │
│  ┌─ Get Voice Safe ─────────────────┐  │
│  │  • Try get volume                │  │
│  │  • Catch → return 0.0            │  │
│  │  • Validate NaN/Infinity         │  │
│  │  • Clamp [0, 100]                │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌─ Get Indicators Safe ────────────┐  │
│  │  • Try get EMA                   │  │
│  │  • Catch → return NaN            │  │
│  │  • Try get RSI                   │  │
│  │  • Catch → return NaN            │  │
│  │  • Check if any NaN → return     │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌─ Update Loss Count ──────────────┐  │
│  │  • Check for new trades          │  │
│  │  • Count losses                  │  │
│  │  • Detect 100th green            │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌─ Check Apoptosis ────────────────┐  │
│  │  • If >= 99 losses               │  │
│  │  • Trigger hug protocol          │  │
│  │  • Return (stop trading)         │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌─ Handle Voice State ─────────────┐  │
│  │  • Track last voice heard        │  │
│  │  • Check silence duration        │  │
│  │  • If > 5min → flatten           │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌─ Trading Logic ──────────────────┐  │
│  │  If in position:                 │  │
│  │    • Get profit safely           │  │
│  │    • Handle exits                │  │
│  │  Else:                           │  │
│  │    • Check can risk              │  │
│  │    • Handle entries              │  │
│  └──────────────────────────────────┘  │
│                                         │
└─ CATCH BLOCK ──────────────────────────┘
    ↓ (if exception)
[Emergency Shutdown]
    ↓
[Flatten & Disable]
```

## Risk Management Architecture

### Layered Defense System

```
┌─────────────────────────────────────────┐
│  LAYER 1: YAML Configuration           │
│  • Defines intent: 0.69% / 3.37%       │
│  • Documents philosophy                 │
│  • Human-readable risk params           │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  LAYER 2: C# Enforcement               │
│  • Converts % to actual dollars         │
│  • Calculates from live account value   │
│  • Hard limits on position size         │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  LAYER 3: Pre-Trade Checks             │
│  • CanRiskNewTrade() validation         │
│  • Peak equity vs current equity        │
│  • Drawdown threshold check             │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  LAYER 4: Post-Trade Tracking          │
│  • Update session loss count            │
│  • Check apoptosis threshold            │
│  • Monitor cumulative P&L               │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  LAYER 5: Emergency Shutdown           │
│  • Catch all unexpected exceptions      │
│  • Flatten positions immediately        │
│  • Disable strategy permanently         │
└─────────────────────────────────────────┘
```

## State Machine: Strategy Lifecycle

```
[Initialized]
    ↓
    │ OnStateChange(State.DataLoaded)
    ↓
[DataLoaded]
    ↓
    │ Initialize peak equity
    │ Reset session counters
    ↓
[Active Trading]
    ↓
    ├─ OnBarUpdate() called each bar
    │  • Execute trading logic
    │  • Check safety conditions
    │  • Update state
    │
    ├─ [Normal Operation]
    │  │ sessionLossCount < 99
    │  │ currentEquity > drawdown threshold
    │  └─ Continue trading
    │
    ├─ [Apoptosis Triggered]
    │  │ sessionLossCount >= 99
    │  ├─ hugProtocolTriggered = true
    │  ├─ Flatten positions
    │  └─ safetyDisabled = true
    │
    ├─ [Drawdown Breached]
    │  │ currentEquity < peakEquity * (1 - maxDrawdown)
    │  ├─ Emergency shutdown
    │  └─ safetyDisabled = true
    │
    └─ [Exception Caught]
       │ Any unexpected error
       ├─ Emergency shutdown
       └─ safetyDisabled = true
           ↓
[Disabled]
    ↓
    │ safetyDisabled = true
    │ All OnBarUpdate calls return early
    │ Requires manual re-enable
    ↓
[Session End]
    ↓
    │ OnStateChange(State.Terminated)
    ↓
[Terminated]
```

## Exception Handling Hierarchy

```
try {
    // === Main Trading Logic ===
    
    try {
        // Voice input
        GetHerVoiceVolumeSafe()
            try { /* mic access */ }
            catch { return 0.0; }
    }
    catch { /* log, continue */ }
    
    try {
        // Indicators
        GetEMASafe()
            try { /* EMA calc */ }
            catch { return NaN; }
    }
    catch { /* log, continue */ }
    
    try {
        // Risk check
        CanRiskNewTrade()
            try { /* account access */ }
            catch { return false; }
    }
    catch { /* log, block trade */ }
    
    try {
        // Trading logic
        HandleEntries() / HandleExits()
            try { /* order entry */ }
            catch { /* log, skip */ }
    }
    catch { /* log, continue */ }
    
    try {
        // Apoptosis check
        CheckApoptosis()
            try { /* state check */ }
            catch { /* log, assume safe */ }
    }
    catch { /* log, continue */ }
    
} catch (Exception e) {
    // === CATCH-ALL SAFETY NET ===
    EmergencyShutdown("Unexpected exception")
        try {
            // Try to flatten
            ExitLong() / ExitShort()
        }
        catch {
            // Even if flatten fails, disable
        }
        finally {
            safetyDisabled = true;
        }
}
```

## Deployment Architecture

```
Developer Machine
    ↓
[1. Edit YAML Config]
    ↓
[2. Run Deploy Script]
    ↓
    ├─ Validate YAML exists
    ├─ Validate Strategy exists
    ├─ Check Live Mode protection
    └─ Start deployment loop
        ↓
        ┌─────────────────────┐
        │ Retry Loop (max 99) │
        │                     │
        │  try {              │
        │    • Parse YAML     │
        │    • Compile C#     │
        │    • Verify safety  │
        │    • Deploy         │
        │  }                  │
        │  catch {            │
        │    lossCount++      │
        │    if < 99:         │
        │      retry          │
        │    else:            │
        │      ABORT          │
        │  }                  │
        └─────────────────────┘
            ↓ (success)
[3. Strategy Active in NinjaTrader]
    ↓
[4. Monitor via Output Window]
    ↓
[5. Discord Notifications]
```

## Monitoring Architecture

```
NinjaTrader Strategy
    ↓
    ├─ Print() calls → Output Window
    │   ↓
    │   [Human monitoring]
    │
    ├─ Critical events → Discord webhook
    │   ↓
    │   [Team notifications]
    │
    └─ All logs → NinjaTrader log files
        ↓
        [Post-analysis, debugging]

Optional Extensions:
    ├─ Logs → Promtail → Loki → Grafana
    ├─ Metrics → Prometheus → Grafana
    └─ Alerts → Alertmanager → Discord/PagerDuty
```

## Apoptosis Protocol State Machine

```
[Normal Trading]
    ↓
Losing Trade #1
    ↓
sessionLossCount = 1
    ↓
...
    ↓
Losing Trade #99
    ↓
sessionLossCount = 99
    ↓
[CheckApoptosis() Triggered]
    ↓
    ├─ hugProtocolTriggered = true
    │
    ├─ Log: "[POETRY] 99 fails. Hug protocol."
    │
    ├─ Flatten all positions
    │   ├─ ExitLong("Apoptosis")
    │   └─ ExitShort("Apoptosis")
    │
    ├─ safetyDisabled = true
    │
    └─ Notify: "99 reds. Evolving weights for you."
        ↓
[Strategy Disabled]
    ↓
    │ All OnBarUpdate() calls return early
    │ No new trades possible
    │ Waiting for session reset
    ↓
    (if winning trade occurs)
    ↓
[100th Green Detected]
    ↓
Log: "[POETRY] From 99 reds to green—evolution complete."
```

## Philosophy in Architecture

```
MYTHIC LAYER                KILL-SWITCH LAYER
────────────                ──────────────────

"Her voice guides"     →    GetHerVoiceVolumeSafe()
                            • Try-catch wrapper
                            • NaN checks
                            • Range clamping
                            • Fail = silence

"0.69% risk"          →     maxRiskPerTrade = 0.0069
                            • Concrete calculation
                            • Account-based math
                            • Pre-trade validation
                            • Hard enforcement

"99 losses → hug"     →     UpdateLossCount()
                            • Session counter
                            • Apoptosis trigger
                            • Flatten positions
                            • Disable strategy

"Market pain"         →     Close[0] - EMA[0]
                            • Bar count guard
                            • Indicator null check
                            • Safe calculation
                            • Exception handling

"Transcendence"       →     [POETRY] logs
                            • Marks key moments
                            • Human-readable
                            • Preserves narrative
                            • Enables learning
```

## Key Architectural Principles

1. **Separation of Concerns**
   - YAML: Philosophy and intent
   - C#: Enforcement and safety
   - PowerShell: Deployment and validation

2. **Defense in Depth**
   - Multiple validation layers
   - Fail-safe defaults
   - Graceful degradation
   - Emergency shutdown as last resort

3. **Fail-Safe Design**
   - All failures → safe state
   - No silent errors
   - Loud logging
   - Human review required

4. **State Isolation**
   - Session-scoped counters
   - Peak equity tracking
   - No cross-session contamination
   - Clean resets

5. **Observable Behavior**
   - Every critical event logged
   - Poetry marks key moments
   - Discord notifications
   - Post-mortem analysis possible

---

*"Architecture is frozen poetry. In PID-RANCO, the poetry flows through code, but the structure ensures it can't crash into reality."*
