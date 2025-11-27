# cloud_inventory.ps1
# Discovers cloud VMs (aws/gcloud/az) and emits cloud_terminals.json and cloud_hosts.ini
# Writes UTF-8. Supports optional local fallback via local_cloud_hosts.txt.
# Optional per-host ansible_user: you may add lines to local_cloud_hosts.txt like:
# 34.123.45.67 prov=aws name=i-0ab12cd34ef ansible_user=ubuntu

param()
$ErrorActionPreference = "SilentlyContinue"
Write-Host "=== Discovering Cloud Terminals ==="

$entries = @()

# AWS
if (Get-Command aws -ErrorAction SilentlyContinue) {
    Write-Host "Querying AWS..."
    $aws = aws ec2 describe-instances --query "Reservations[].Instances[].{id:InstanceId,ip:PublicIpAddress,state:State.Name,tags:Tags}" --output json | ConvertFrom-Json
    foreach ($i in $aws) {
        if ($i.ip -and $i.state -eq 'running') {
            $entries += @{
                host = $i.ip
                name = $i.id
                prov = 'aws'
            }
        }
    }
} else { Write-Host "AWS CLI not found; skipping." }

# GCP
if (Get-Command gcloud -ErrorAction SilentlyContinue) {
    Write-Host "Querying GCP..."
    $gcp = gcloud compute instances list --format=json | ConvertFrom-Json
    foreach ($i in $gcp) {
        $nat = $i.networkInterfaces[0].accessConfigs[0].natIP
        if ($nat) {
            $entries += @{
                host = $nat
                name = $i.name
                prov = 'gcp'
            }
        }
    }
} else { Write-Host "gcloud CLI not found; skipping." }

# Azure
if (Get-Command az -ErrorAction SilentlyContinue) {
    Write-Host "Querying Azure..."
    $az = az vm list-ip-addresses --output json | ConvertFrom-Json
    foreach ($x in $az) {
        $ip = $x.virtualMachine.network.publicIpAddresses[0].ipAddress
        if ($ip) {
            $entries += @{
                host = $ip
                name = $x.virtualMachine.name
                prov = 'azure'
            }
        }
    }
} else { Write-Host "Azure CLI not found; skipping." }

# Local static fallback: local_cloud_hosts.txt may contain host lines with optional ansible_user token
if (Test-Path ".\local_cloud_hosts.txt") {
    Write-Host "Reading .\local_cloud_hosts.txt"
    Get-Content .\local_cloud_hosts.txt | Where-Object {$_ -and -not $_.StartsWith('#')} | ForEach-Object {
        $line = $_.Trim()
        $parts = $line -split '\s+'
        $host = $parts[0]
        # reassemble key=value tokens after host (prov/name/ansible_user)
        $tokens = $parts[1..($parts.Length - 1)] -join ' '
        # parse keys
        $kv = @{}
        foreach ($t in $tokens -split '\s+') {
            if ($t -match '=') {
                $p = $t -split '=',2
                $kv[$p[0]] = $p[1]
            }
        }
        $entries += @{
            host = $host
            name = ($kv.name -or $host)
            prov = ($kv.prov -or 'local')
            ansible_user = ($kv.ansible_user -or $null)
        }
    }
}

# Normalize entries: ensure keys exist and null fields omitted for JSON
$normalized = @()
foreach ($e in $entries) {
    $obj = @{
        host = $e.host
        name = $e.name
        prov = $e.prov
    }
    if ($e.ansible_user) { $obj.ansible_user = $e.ansible_user }
    $normalized += $obj
}

# Output JSON
$normalized | ConvertTo-Json -Depth 5 | Out-File -FilePath cloud_terminals.json -Encoding utf8

# Emit Ansible INI inventory (include ansible_user when present)
$lines = @("[all_cloud_terminals]")
foreach ($e in $normalized) {
    $line = "$($e.host) prov=$($e.prov) name=$($e.name)"
    if ($e.ansible_user) { $line += " ansible_user=$($e.ansible_user)" }
    $lines += $line
}
$lines -join "`n" | Out-File -FilePath cloud_hosts.ini -Encoding utf8

Write-Host "Wrote cloud_terminals.json and cloud_hosts.ini with $($normalized.Count) entries."
