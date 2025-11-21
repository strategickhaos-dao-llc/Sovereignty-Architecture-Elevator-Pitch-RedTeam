# SRE Practices

**Canon References: #51-55**

## Core Principles

Site Reliability Engineering (SRE) is what happens when you ask a software engineer to design operations.

```
Traditional Ops          SRE
Manual processes    →    Automation
Reactive            →    Proactive  
Blame culture       →    Blameless
100% uptime goal    →    Error budgets
Hero culture        →    Sustainable practices
```

## SLIs, SLOs, SLAs (#51)

### Service Level Indicators (SLIs)

Quantitative measures of service quality.

**Common SLIs:**
```typescript
// Availability: % of successful requests
const availability = successfulRequests / totalRequests;

// Latency: % of requests faster than threshold
const latencyCompliance = requestsUnder100ms / totalRequests;

// Throughput: Requests per second
const throughput = totalRequests / timeWindowSeconds;

// Error rate: % of failed requests
const errorRate = failedRequests / totalRequests;
```

**Good SLI Properties:**
- Measurable
- Meaningful to users
- Simple to understand
- Aggregatable

### Service Level Objectives (SLOs)

Target values for SLIs.

**Example SLOs:**
```yaml
availability:
  sli: "successful_requests / total_requests"
  target: 99.9%
  window: 30 days

latency:
  sli: "requests_under_100ms / total_requests"
  target: 95%
  window: 7 days
  
error_rate:
  sli: "failed_requests / total_requests"
  target: < 0.1%
  window: 24 hours
```

**Setting SLOs:**
1. Start with user expectations
2. Consider technical feasibility
3. Include error budget (room for failure)
4. Iterate based on data

```typescript
// SLO Calculation
interface SLO {
  target: number;      // e.g., 99.9%
  window: number;      // e.g., 30 days in seconds
  
  calculateCompliance(sliValue: number): {
    compliant: boolean;
    remaining: number;
  } {
    const compliant = sliValue >= this.target;
    const remaining = this.target - sliValue;
    return { compliant, remaining };
  }
}

const availabilitySLO = new SLO({ target: 0.999, window: 30 * 24 * 3600 });
const currentAvailability = 0.9985;
const result = availabilitySLO.calculateCompliance(currentAvailability);
// { compliant: false, remaining: 0.0005 }
```

### Service Level Agreements (SLAs)

Business contracts with consequences.

**SLA = SLO + Consequences**

```yaml
sla:
  objective: 99.9% availability
  window: monthly
  consequences:
    - threshold: 99.9%
      penalty: none
    - threshold: 99.5%
      penalty: 10% credit
    - threshold: 99.0%
      penalty: 25% credit
    - threshold: < 99.0%
      penalty: 50% credit + option to terminate
```

**Golden Rule:** SLO should be stricter than SLA
```
Internal SLO: 99.95%  (gives buffer)
External SLA: 99.9%   (contractual commitment)
```

## Error Budgets (#52)

**Error Budget = 100% - SLO**

If SLO is 99.9%, error budget is 0.1% (43 minutes of downtime per month).

### Using Error Budgets

```typescript
class ErrorBudget {
  constructor(
    private slo: number,        // e.g., 0.999
    private windowSeconds: number // e.g., 30 days
  ) {}
  
  calculate(successfulRequests: number, totalRequests: number) {
    const actualAvailability = successfulRequests / totalRequests;
    const targetAvailability = this.slo;
    
    // How much error budget have we used?
    const budgetUsed = (1 - actualAvailability) / (1 - targetAvailability);
    
    // How much downtime can we still afford?
    const allowedDowntime = this.windowSeconds * (1 - targetAvailability);
    const actualDowntime = this.windowSeconds * (1 - actualAvailability);
    const remainingDowntime = allowedDowntime - actualDowntime;
    
    return {
      budgetUsed,           // 0.0 to 1.0 (0% to 100%)
      remainingDowntime,    // seconds
      state: budgetUsed < 0.5 ? 'healthy' : 
             budgetUsed < 0.8 ? 'warning' : 
             budgetUsed < 1.0 ? 'critical' : 'exhausted'
    };
  }
}

// 99.9% SLO over 30 days
const budget = new ErrorBudget(0.999, 30 * 24 * 3600);
const result = budget.calculate(9990000, 10000000);
// { budgetUsed: 1.0, remainingDowntime: 0, state: 'exhausted' }
```

### Error Budget Policy

**When budget is healthy (< 50% used):**
- Deploy frequently
- Experiment with new features
- Take calculated risks

**When budget is depleted (> 100% used):**
- Freeze all changes except bug fixes
- Focus on reliability improvements
- Cancel non-critical work
- Increase monitoring

**Example Policy:**
```yaml
error_budget_policy:
  healthy: # < 50% used
    - deploy_frequency: multiple_per_day
    - change_approval: engineer_approval
    - allowed_experiments: yes
    
  warning: # 50-80% used
    - deploy_frequency: once_per_day
    - change_approval: team_lead_approval
    - allowed_experiments: yes_with_caution
    
  critical: # 80-100% used
    - deploy_frequency: emergency_only
    - change_approval: director_approval
    - allowed_experiments: no
    
  exhausted: # > 100% used
    - deploy_freeze: yes
    - focus: reliability_only
    - postmortem: required
```

## Toil Reduction (#53)

**Toil:** Work that is manual, repetitive, automatable, tactical, grows with scale, and has no lasting value.

### Identifying Toil

```
Is it manual?           YES ─┐
Is it repetitive?       YES ─┤
Is it automatable?      YES ─┼─→ It's toil, automate it!
Is it tactical?         YES ─┤
Grows with scale?       YES ─┘

Any NO? → Might not be toil
```

**Toil Examples:**
- Manually deploying every release
- Running scripts to clean up disk space
- Responding to the same alert manually
- Copying data between environments
- Provisioning user accounts one by one

### Toil Budget

Target: **< 50% of engineer time on toil**

```typescript
interface ToilTracking {
  week: string;
  engineerHours: number;
  toil: {
    manual_deployments: number;
    alert_response: number;
    data_cleanup: number;
    user_requests: number;
  };
  
  calculateToilPercentage(): number {
    const totalToil = Object.values(this.toil).reduce((a, b) => a + b, 0);
    return (totalToil / this.engineerHours) * 100;
  }
}

const weekData = {
  week: '2024-W01',
  engineerHours: 40,
  toil: {
    manual_deployments: 8,
    alert_response: 6,
    data_cleanup: 4,
    user_requests: 2
  }
};

const toilPercentage = weekData.calculateToilPercentage(); // 50%
// At threshold! Time to automate something.
```

### Automation Strategy

```typescript
// Before: Manual toil
async function deployManually() {
  // 1. SSH to server
  // 2. Pull code
  // 3. Run migrations
  // 4. Restart service
  // 5. Check logs
  // Takes 30 minutes, error-prone
}

// After: Automated
async function deployAutomated() {
  await cicd.deploy({
    service: 'api',
    version: 'v1.2.3',
    environment: 'production',
    strategy: 'canary'
  });
  // Takes 2 minutes, reliable
}
```

## Blameless Postmortems (#54)

**Goal:** Learn from failures, not blame people.

### Postmortem Template

```markdown
# Incident Postmortem: [Title]

**Date:** 2024-01-15
**Duration:** 2 hours 15 minutes
**Severity:** SEV-2 (Partial outage)
**Author:** Jane Doe

## Summary
API latency increased to 10s causing timeouts for 30% of users.

## Impact
- 30% of users experienced timeouts
- Revenue loss: ~$50,000
- Customer support tickets: 234

## Timeline (All times UTC)
- 14:00 - Deployment of v2.5.0 to production (canary 5%)
- 14:15 - Alerts fire: High latency on /api/orders
- 14:20 - On-call engineer investigates
- 14:30 - Database connection pool exhaustion identified
- 14:45 - Rollback initiated
- 15:00 - Rollback complete
- 16:15 - Full service restored after connection pool cleanup

## Root Cause
New code in v2.5.0 leaked database connections. Each request opened 
connection but didn't close it on error path. Connection pool (max 100)
exhausted after ~100 requests.

## What Went Well
- Alerts fired promptly
- Rollback was fast (15 minutes)
- Team coordinated effectively

## What Went Wrong
- Connection leak not caught in testing
- Canary metrics didn't catch issue before full rollout
- No automated rollback on error threshold

## Action Items
- [ ] Add connection leak detection to tests (Owner: John, Due: 2024-01-20)
- [ ] Improve canary metrics to include connection pool (Owner: Sarah, Due: 2024-01-22)
- [ ] Implement auto-rollback when error rate > 5% (Owner: Mike, Due: 2024-02-01)
- [ ] Add connection pool exhaustion alert (Owner: Jane, Due: 2024-01-18)

## Lessons Learned
- Error paths need as much testing as happy paths
- Connection management is critical at scale
- Canary deployments need comprehensive metrics
```

### Blameless Culture

**Bad:**
> "John caused an outage by deploying buggy code."

**Good:**
> "Our deployment process allowed buggy code to reach production. We need better automated testing and canary validation."

**Key Principles:**
- Systems fail, not people
- Human error is a symptom, not a cause
- Focus on process improvements
- Psychological safety enables learning

## Runbooks (#55)

Documented procedures for common operations.

### Runbook Template

```markdown
# Runbook: High Database Latency

## Symptoms
- Database queries taking > 1s
- Alert: `database_query_duration_p95 > 1s`
- Users reporting slow page loads

## Impact
- Degraded user experience
- Possible timeouts
- Cascading failures to dependent services

## Diagnosis

### Step 1: Check Database Metrics
```sql
-- Check slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 1000
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Step 2: Check Connection Pool
```bash
# Check active connections
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';

# Should be < 80% of max_connections
```

### Step 3: Check for Lock Contention
```sql
SELECT * FROM pg_locks WHERE NOT granted;
```

## Resolution

### Option A: Kill Long-Running Query (Safe)
```sql
-- Find long-running queries
SELECT pid, now() - query_start as duration, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - query_start > interval '5 minutes';

-- Kill specific query
SELECT pg_terminate_backend(pid);
```

### Option B: Scale Database (Safe, slow)
```bash
# Increase instance size
aws rds modify-db-instance --db-instance-identifier mydb \
  --db-instance-class db.r5.2xlarge --apply-immediately
```

### Option C: Restart Database (RISKY - last resort)
```bash
# Coordinate with team first!
# Brief outage expected
aws rds reboot-db-instance --db-instance-identifier mydb
```

## Prevention
- Add index to frequently queried columns
- Set statement_timeout to prevent runaway queries
- Implement connection pooling
- Regular VACUUM and ANALYZE

## Escalation
If not resolved in 30 minutes, escalate to:
- Database Team: @db-oncall
- SRE Manager: @sre-manager
```

## Measuring Reliability

### Key Metrics

```typescript
interface ReliabilityMetrics {
  // Four Golden Signals
  latency: {
    p50: number;
    p95: number;
    p99: number;
  };
  traffic: {
    requestsPerSecond: number;
  };
  errors: {
    errorRate: number;
    errorBudget: number;
  };
  saturation: {
    cpuUsage: number;
    memoryUsage: number;
    diskUsage: number;
  };
  
  // Reliability
  availability: number;
  mtbf: number; // Mean Time Between Failures
  mttr: number; // Mean Time To Recovery
  
  // Toil
  toilPercentage: number;
  automationCoverage: number;
}
```

## Related Concepts

- [[Observability]] - Foundation for measuring SLIs
- [[Error_Budgets]] - Balancing velocity and reliability
- [[Chaos_Engineering]] - Testing reliability proactively
- [[Incident_Response]] - Handling outages

## Further Reading

- "Site Reliability Engineering" by Google
- "The Site Reliability Workbook" by Google
- "Implementing Service Level Objectives" by Alex Hidalgo

---

**Key Takeaway:** SRE is about sustainable reliability through automation, measurement (SLOs), learning (blameless postmortems), and balancing innovation with stability (error budgets).
