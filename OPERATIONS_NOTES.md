# Operations Notes — Post‑Swarm Aggregation & Cost-Guard

## 1) Aggregation & Verification

- **Run**: `./collect_and_verify.sh cloud_hosts.ini collected`
- **Checks**: Verifies blake3 hashes exist in node provenance logs, produces `collected/aggregated_results.json`, produces detached GPG signature `aggregated_results.json.asc`.
- **Recommended**: GPG-sign with an org key and run OpenTimestamps (`ots stamp aggregated_results.json.asc`) to anchor.

## 2) Auto-Shutdown / Cost Guard

- Deploy `auto_shutdown_idle.yml` to control schedule or run via cron/GitHub Actions on a schedule (e.g., every 15m).
- It examines last PID-RANCO output timestamp and schedules node shutdown when idle >= `idle_minutes`.
- Use control-level cloud API shutdowns for stricter cost control (e.g., AWS stop-instances by tag) — provider playbooks can be added if desired.

## 3) Daily Pulse & Monitoring

- Run `cluster_pulse.sh` on a schedule (cron or GitHub Actions) to append node health to `cluster_pulse.txt` (UAM ingestable).
- Consider Prometheus + Pushgateway on control plane for richer telemetry later.

## 4) Safety

- Do not add cloud API keys to inventory. Use vault references or ephemeral token retrieval.
- Test auto-shutdown with a small threshold and a single host (localhost) first.

## 5) Next Steps (Available on Request)

- Add provider stop/start playbooks (AWS/GCP/Azure) that use instance IDs from `cloud_terminals.json` and safely stop/hibernate by tag.
- Create a scheduled GitHub Actions workflow that runs `cluster_pulse.sh` and runs the auto-shutdown playbook from a self-hosted runner or control host via remote execution.
- Add a central cost dashboard (small script that queries cloud provider billing APIs) and threshold alerting (email/Slack).

## Quick Run Suggestions

### Immediately After Your Current Run Finishes

1. `./collect_and_verify.sh cloud_hosts.ini collected`
2. Inspect `collected/provenance_verified.log` and `aggregated_results.json`
3. `gpg --verify collected/aggregated_results.json.asc aggregated_results.json` (or just open)
4. `ots stamp collected/aggregated_results.json.asc` (if you run OpenTimestamps client)

### Enable Cost-Guard

- Add a cron on the control host:
  ```bash
  */15 * * * * /path/to/control_cost_guard.sh /path/to/cloud_hosts.ini 30
  ```
- Or schedule a GitHub Actions workflow that calls a self-hosted runner which has access to ansible and the inventory.
