# Cloud Terminal Federation — Deploy README

## Purpose

Discover cloud terminals, bootstrap them with an Ansible playbook, and run PID-RANCO backtests sharded across your terminals with provenance hashing to UAM.

## Prerequisites (control machine)

- Python 3.10+ and virtualenv
- venv: `python3 -m venv venv && ./venv/bin/pip install ansible ansible-lint`
- AWS/GCloud/Azure CLIs if you want automated discovery
- SSH keys loaded in agent or configured per-host
- Do NOT store cloud API credentials in repository or inventory files.

## Inventory discovery

1. Optionally create `local_cloud_hosts.txt` for static hosts (example format):

   ```text
   34.123.45.67 prov=aws name=i-0ab12cd34ef ansible_user=ubuntu
   ```

2. Run:

   ```powershell
   .\cloud_inventory.ps1
   ```

   This writes `cloud_terminals.json` and `cloud_hosts.ini`

## Notes on ansible_user per-host

To handle mixed images, add `ansible_user` to the inventory line:

```text
34.123.45.67 prov=aws name=i-0ab12cd34ef ansible_user=ubuntu
```

The inventory generator will include `ansible_user` when present and ansible will pick it up automatically.

## Bootstrap nodes (one-time)

Activate venv and run:

```bash
ansible-playbook -i cloud_hosts.ini cloud_swarm_playbook.yaml
```

This clones repo to `/opt/strategickhaos`, checks that PID-RANCO exists, creates `run_pid_ranco.sh`.

## Launch sharded run

From control host:

```bash
./shard_launcher.sh [ssh_user]
```

or PowerShell:

```powershell
.\shard_launcher.ps1 -User <ssh_user>
```

Launcher computes N = number of hosts, assigns shards 0..N-1 and uses ansible ad-hoc to invoke `run_pid_ranco.sh` on each node.

## Outputs

- Per-node result file: `/opt/strategickhaos/logs/pid_ranco_<host>_shard_<i>_of_<N>.json`
- Provenance log (blake3 hashes): `/opt/strategickhaos/uam/provenance.log`

## Opsec & Safety

- Never commit cloud credentials to this repo or inventory files. Use vault references and agent-forwarded SSH keys.
- Inventory may contain `ansible_user` tokens for mixed images; prefer per-host `ansible_user` to avoid global user assumptions.
- Playbook is Linux-focused (Ubuntu). Windows nodes are not supported by this PR.
- Test locally/dry-run with localhost entry before wide rollout.

## Example localhost dry run (to test end-to-end)

1. Add a localhost entry to `local_cloud_hosts.txt`:

   ```text
   127.0.0.1 prov=local name=local-machine ansible_user=$(whoami)
   ```

2. Run `cloud_inventory.ps1`, then bootstrap and run; verify outputs in `/opt/strategickhaos/logs` and `provenance.log`.
