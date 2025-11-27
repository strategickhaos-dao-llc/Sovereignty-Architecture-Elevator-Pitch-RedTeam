# shard_launcher.ps1 - PowerShell launcher
param(
  [string]$User = "ubuntu",
  [string]$Inventory = "cloud_hosts.ini"
)
if (-not (Test-Path $Inventory)) {
  Write-Error "Inventory $Inventory not found."
  exit 1
}
$hosts = Get-Content $Inventory | Where-Object { $_ -and -not $_.StartsWith('[') -and -not $_.StartsWith('#') } | ForEach-Object { ($_ -split '\s+')[0] }
$hosts = $hosts | Where-Object { $_ }
$N = $hosts.Count
if ($N -eq 0) { Write-Error "No hosts found in $Inventory"; exit 1 }

Write-Host "Found $N hosts. Launching shards..."
$i = 0
foreach ($h in $hosts) {
  $shard = $i
  Write-Host "Launching shard $shard on $h"
  Start-Process -FilePath ansible -ArgumentList "-i $Inventory $h -m shell -a `/opt/strategickhaos/run_pid_ranco.sh $shard $N`" -NoNewWindow
  $i++
}
Write-Host "Jobs started."
