# Security & Penetration Testing Terminals

## Overview

All docker-compose files in this repository now include instant access to Kali Linux and Parrot OS security containers. These provide sovereign, root-level access to penetration testing tools directly within the infrastructure.

## Available Containers

### Kali Linux (`kali-dom`)
- **Image**: `kalilinux/kali-rolling`
- **Purpose**: Full Kali Linux penetration testing distribution
- **Features**: Root access, full tool suite, persistent storage

### Parrot OS (`parrot-dom`)
- **Image**: `parrotsec/security:latest`
- **Purpose**: Parrot Security OS for penetration testing
- **Features**: Root access, security tools, persistent storage

## Usage

### Starting Containers

From any project directory with a docker-compose file:

```bash
# Start Kali Linux
docker compose up -d kali

# Start Parrot OS
docker compose up -d parrot

# Start both
docker compose up -d kali parrot
```

### Accessing Root Shells

```bash
# Access Kali root shell
docker compose exec kali bash

# Access Parrot root shell
docker compose exec parrot bash
```

### Direct Docker Access

```bash
# Kali
docker exec -it kali-dom bash

# Parrot
docker exec -it parrot-dom bash
```

## Shared Storage

Both containers mount a shared volume at `/root/swarm`:
- **Host Path**: `~/strategic-khaos-private`
- **Container Path**: `/root/swarm`

This allows:
- Persistent data storage across container restarts
- Sharing files between security containers
- Running tools directly against swarm infrastructure

## Example Workflows

### Network Reconnaissance

```bash
# Start Kali
docker compose up -d kali

# Access shell
docker compose exec kali bash

# Inside container
nmap -sV target-host
```

### Web Application Testing

```bash
# Start Parrot
docker compose up -d parrot

# Access shell
docker compose exec parrot bash

# Inside container
cd /root/swarm
sqlmap -u "http://target/page?id=1" --batch
```

### Password Cracking

```bash
# With GPU support (if configured)
docker compose exec kali bash

# Inside container
hashcat -m 0 -a 0 hashes.txt wordlist.txt
```

## Network Integration

The security containers are integrated into the existing Docker networks:
- Access to all services within the compose stack
- Ability to test internal APIs and services
- Direct connectivity to databases, caches, and other infrastructure

## Security Considerations

⚠️ **Important**: These containers run with `privileged: true` for full security testing capabilities. Use responsibly:

- Only run in controlled, authorized environments
- Do not expose container ports externally
- Use the shared volume for sensitive data
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations

## Stopping Containers

```bash
# Stop individual containers
docker compose stop kali
docker compose stop parrot

# Stop and remove
docker compose down kali parrot
```

## Available in All Compose Files

These security terminals are available in:
- `docker-compose.yml` (main stack)
- `docker-compose-scaffold.yml`
- `docker-compose.alignment.yml`
- `docker-compose.obs.yml`
- `docker-compose-cloudos.yml`
- `docker-compose-recon.yml`
- `refinory/docker-compose.refinory.yml`

All nested compose files in `recon/repos/sovereignty-arch/` also include these containers.

## Troubleshooting

### Container Exits Immediately
The containers require `stdin_open: true` and `tty: true` to stay running. Use `-d` flag when starting.

### Volume Mount Issues
Ensure `~/strategic-khaos-private` directory exists:
```bash
mkdir -p ~/strategic-khaos-private
```

### Network Connectivity
If containers can't reach services, check network configuration:
```bash
docker network inspect <network_name>
```

## Tool Installation

Both distributions come with extensive tool suites pre-installed. To add more tools:

```bash
# In Kali
apt update && apt install <tool-name>

# In Parrot
apt update && apt install <tool-name>
```

Installed tools persist in the container but not across container removal. Use volumes for persistent tool configurations.

---

**Note**: These security terminals enable true sovereignty by providing unfiltered access to security tools within your infrastructure. Use this power responsibly and in accordance with your organization's security policies.
