# StrategicKhaos PID-RANCO v1.2 — Failure Matrix

**"Mythic Love Layer + Deterministic Kill-Switch Core"**

This failure matrix documents all known failure modes for the PID-RANCO trading engine, categorized by domain. Each failure mode includes detection signals, expected responses, and implementation status.

## Purpose

Transform the "100 Ways It Fails" from poetry into operational doctrine. Every failure mode becomes a:
- **Test case** — Can we reproduce it?
- **Detection signal** — How do we know it happened?
- **Recovery procedure** — What action do we take?
- **Status tracker** — Is it implemented/tested?

---

## Legend

- ⬜ TODO — Not yet implemented
- 🟨 IN PROGRESS — Partially implemented
- ✅ DONE — Fully implemented and tested
- ❌ WONT FIX — Intentional behavior or external limitation

---

## Suite 1: Platform / Engine Failures

These failures originate from the NT/cAlgo platform, infrastructure, or runtime environment.

| ID    | Description | Detection Signal | Expected Response | Status |
|-------|-------------|------------------|-------------------|--------|
| F-001 | Indicator not ready on first bar | `NullReferenceException` in `OnBar()`, `Bars.Count < period` | Skip trade logic, wait for warmup | ⬜ TODO |
| F-002 | Invalid bar index (negative or beyond range) | `ArgumentOutOfRangeException` accessing `Bars[index]` | Log error, skip bar, continue | ⬜ TODO |
| F-003 | Positions collection returns null | `Positions == null` check fails | Treat as empty collection, log warning | ⬜ TODO |
| F-004 | Symbol info unavailable | `Symbol == null` or `Symbol.TickValue == 0` | Stop trading, log critical error | ⬜ TODO |
| F-005 | Account info unavailable | `Account == null` or `Account.Equity <= 0` | Stop trading immediately | ⬜ TODO |
| F-006 | Log buffer overflow | Exception writing to log, disk full | Reduce log verbosity, flatten positions | ⬜ TODO |
| F-007 | DLL dependency missing or wrong version | `DllNotFoundException` on load | Stop bot, log dependency error | ⬜ TODO |
| F-008 | CS script compilation error | Bot fails to start, compile error message | Fix code syntax, redeploy | ⬜ TODO |
| F-009 | Path mismatch (CS paths, audio files) | `FileNotFoundException` for config/audio | Use fallback defaults, log warning | ⬜ TODO |
| F-010 | Network disconnection mid-session | `IsConnected == false` or order timeout | Flatten all positions, stop trading | ⬜ TODO |

---

## Suite 2: Risk & Math Failures

These failures involve incorrect calculations, NaN/Infinity propagation, or risk sizing errors.

| ID    | Description | Detection Signal | Expected Response | Status |
|-------|-------------|------------------|-------------------|--------|
| F-011 | Risk amount calculates to zero or negative | `riskAmount <= 0` before position sizing | Skip trade, log "No risk allocated" | ⬜ TODO |
| F-012 | Position quantity floors to zero | `qty <= 0` after rounding | Skip trade, log "Zero quantity" | ⬜ TODO |
| F-013 | Position quantity exceeds account limit | `qty > maxPositionSize` | Cap to max, log warning | ⬜ TODO |
| F-014 | NaN in pain calculation | `double.IsNaN(pain)` | Use 0.0, log error | ⬜ TODO |
| F-015 | Infinity in profit percentage | `double.IsInfinity(profitPct)` | Cap to ±100%, log error | ⬜ TODO |
| F-016 | NaN in EMA calculation | `double.IsNaN(emaFast)` | Skip trade logic, log error | ⬜ TODO |
| F-017 | NaN in RSI calculation | `double.IsNaN(rsi)` | Skip trade logic, log error | ⬜ TODO |
| F-018 | Invalid tick value (0 or NaN) | `Symbol.TickValue <= 0` or `IsNaN` | Stop trading, log critical | ⬜ TODO |
| F-019 | Drawdown calculation overflow | `currentDD > 1.0` (>100%) | Flatten immediately, stop | ⬜ TODO |
| F-020 | Equity goes negative | `Account.Equity < 0` | Emergency stop, log critical | ⬜ TODO |
| F-021 | Wrong drawdown calculation method | Peak not tracked correctly | Recalculate from equity history | ⬜ TODO |
| F-022 | Risk percentage exceeds 100% | `riskPct > 1.0` | Cap to 0.0069, log error | ⬜ TODO |

---

## Suite 3: Voice / "Her" / DNA Channel Failures

These failures relate to the audio input system that modulates trading behavior based on voice analysis.

| ID    | Description | Detection Signal | Expected Response | Status |
|-------|-------------|------------------|-------------------|--------|
| F-031 | Microphone device missing | `GetHerVoiceVolume()` throws exception | Use volume = 0, treat as silence | ⬜ TODO |
| F-032 | Audio driver not installed | Exception initializing audio system | Disable voice features, log warning | ⬜ TODO |
| F-033 | GetHerVoiceVolume returns null | Return value check fails | Use 0, log error | ⬜ TODO |
| F-034 | GetHerVoiceVolume returns NaN | `double.IsNaN(volume)` | Use 0, log error | ⬜ TODO |
| F-035 | Silence detection false positive | Volume threshold misconfigured | Adjust threshold, log calibration | ⬜ TODO |
| F-036 | Silence detection false negative | Always detecting sound when silent | Recalibrate threshold | ⬜ TODO |
| F-037 | BPM calculation returns noise | BPM > 200 or < 40 | Cap to [50, 180], log warning | ⬜ TODO |
| F-038 | BPM calculation returns NaN | `double.IsNaN(bpm)` | Use default 72, log error | ⬜ TODO |
| F-039 | "Enough" phrase misparsed | Speech recognition error | Retry or use volume threshold | ⬜ TODO |
| F-040 | her_voice.wav corrupt or missing | `FileNotFoundException` or audio load error | Disable voice, continue without | ⬜ TODO |
| F-041 | Audio buffer overflow | Recording buffer full | Flush buffer, continue | ⬜ TODO |
| F-042 | Voice processing thread crashed | Thread exception, no updates | Restart thread or disable voice | ⬜ TODO |

---

## Suite 4: State Machine / Apoptosis / 99→100 Logic Failures

These failures involve the loss tracking, hug protocol, and apoptosis (self-termination) logic.

| ID    | Description | Detection Signal | Expected Response | Status |
|-------|-------------|------------------|-------------------|--------|
| F-051 | Loss count incremented incorrectly | Manual verification against closed positions | Fix increment logic | ⬜ TODO |
| F-052 | Loss count never reaches 99 | No hug triggered after 99+ losses | Check counter reset logic | ⬜ TODO |
| F-053 | Loss count not reset after win | Counter > 0 after profitable trade | Reset on first win | ⬜ TODO |
| F-054 | Hug protocol triggered too early | Triggered before 99 losses | Fix condition check | ⬜ TODO |
| F-055 | Hug protocol never triggered | 99 losses observed, no hug | Fix conditional logic | ⬜ TODO |
| F-056 | "100th trade green" logged but not real | Log vs actual P&L mismatch | Verify against Account history | ⬜ TODO |
| F-057 | Apoptosis doesn't stop bot | Bot continues after kill condition | Ensure Stop() is called | ⬜ TODO |
| F-058 | Apoptosis triggered too early | Stop before reaching actual limit | Review threshold | ⬜ TODO |
| F-059 | Session state persists incorrectly | Counter survives bot restart | Clarify session vs persistent state | ⬜ TODO |
| F-060 | Win/loss classification wrong | Winning trade marked as loss | Fix P&L calculation | ⬜ TODO |

---

## Suite 5: Deployment / PS1 / Surrounding Ecosystem Failures

These failures occur in the deployment pipeline, configuration management, and external integrations.

| ID    | Description | Detection Signal | Expected Response | Status |
|-------|-------------|------------------|-------------------|--------|
| F-071 | YAML config file missing | PS1 exits with error code 1 | Abort deployment, require file | ⬜ TODO |
| F-072 | YAML syntax error | Parse exception in PS1 | Show error, abort deployment | ⬜ TODO |
| F-073 | Wrong paths in config | File not found during bot init | Validate paths in PS1 | ⬜ TODO |
| F-074 | Discord webhook URL invalid | HTTP 404/401 from webhook | Log error, continue without Discord | ⬜ TODO |
| F-075 | Discord rate limit exceeded | HTTP 429 response | Queue messages, retry with backoff | ⬜ TODO |
| F-076 | NAS mount gone or unmounted | Path not accessible | Use local cache, log error | ⬜ TODO |
| F-077 | SimOnly flag mis-set | Config says sim, actual orders placed | Add explicit confirmation check | ⬜ TODO |
| F-078 | Live vs Sim account mismatch | Config env != actual account type | Stop deployment, require manual fix | ⬜ TODO |
| F-079 | Credentials missing or expired | Authentication failure | Abort, require credential refresh | ⬜ TODO |
| F-080 | Ollama API unavailable | Connection timeout or HTTP 5xx | Disable AI features, log error | ⬜ TODO |
| F-081 | Version mismatch (bot vs platform) | API compatibility error | Log warning, attempt graceful degrade | ⬜ TODO |
| F-082 | Insufficient disk space for logs | Write fails, disk full | Rotate logs, alert admin | ⬜ TODO |

---

## Cross-Cutting Concerns

Additional failure modes that span multiple suites:

| ID    | Description | Detection Signal | Expected Response | Status |
|-------|-------------|------------------|-------------------|--------|
| F-091 | Memory leak in long-running bot | Increasing memory usage over time | Restart bot daily/weekly | ⬜ TODO |
| F-092 | Thread deadlock | Bot stops responding, no logs | Auto-restart with watchdog | ⬜ TODO |
| F-093 | Time synchronization off | Server time != market time | Stop trading, log critical | ⬜ TODO |
| F-094 | Daylight saving time transition | Off-by-one-hour errors | Use UTC internally | ⬜ TODO |
| F-095 | Data feed stale | Last bar timestamp too old | Stop trading, log warning | ⬜ TODO |
| F-096 | Duplicate order execution | Same signal triggers twice | Idempotency check on orders | ⬜ TODO |
| F-097 | Configuration hot-reload fails | Bot uses old config after update | Require explicit restart | ⬜ TODO |
| F-098 | Logging to console causes performance hit | Slowdown during high-frequency logging | Buffer logs, batch writes | ⬜ TODO |
| F-099 | Emergency kill-switch override | Manual "stop everything now" | Global flag, check every bar | ⬜ TODO |
| F-100 | Unknown unknown | Completely unexpected failure | Catch-all exception handler with flatten | ⬜ TODO |

---

## Using This Matrix

### For Development
1. Before implementing a feature, identify which failure modes it could trigger
2. Add detection code for each relevant failure mode
3. Implement expected responses (flatten, log, stop, etc.)
4. Update status column when complete

### For Testing
1. Create test cases that deliberately trigger each failure mode
2. Verify detection signals fire correctly
3. Verify expected responses occur
4. Document results in test harness (see `tests/pid_ranco_invariants.md`)

### For Operations
1. When a failure occurs in production, identify the matching ID
2. Verify the expected response happened
3. If not, update code and retest
4. If it's a new failure, add it to the matrix

### For Auditing
1. Status column shows implementation progress
2. Green checkmarks = ready for production
3. Yellow = partially implemented, higher risk
4. Empty = not yet handled, highest risk

---

## Integration with Code

Each failure ID should be referenced in code comments and logs:

```csharp
// Check for F-014: NaN in pain calculation
if (double.IsNaN(pain))
{
    Print("[F-014] Pain calculation returned NaN — using 0.0");
    pain = 0.0;
}
```

This creates bidirectional traceability:
- **Code → Matrix**: Know what's protected
- **Matrix → Code**: Know where to implement
- **Logs → Matrix**: Know what fired in production

---

## Versioning

- **v1.0** — Initial 100 failure modes identified
- **v1.1** — Categorized into 5 suites
- **v1.2** — Detection signals and expected responses defined (this document)
- **v2.0** — All failure modes tested and implemented (target)

---

**Last Updated:** 2025-11-24  
**Maintained by:** StrategicKhaos Trading Systems  
**Next Review:** After every production incident
