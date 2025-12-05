#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Cloud Inventory Discovery - Discovers live cloud terminals across AWS, GCP, and Azure.
.DESCRIPTION
    This script discovers cloud terminals from AWS, GCP, and Azure and emits a normalized
    Ansible inventory file (cloud_hosts.ini) for use with cloud_swarm_playbook.yaml.
.PARAMETER Burst
    Number of target nodes to provision (for burst scaling).
.PARAMETER Output
    Output file path for the inventory (default: cloud_hosts.ini).
.EXAMPLE
    ./cloud_inventory.ps1
    ./cloud_inventory.ps1 --burst 100
#>

param(
    [int]$Burst = 0,
    [string]$Output = "cloud_hosts.ini"
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
}

function Discover-AWS {
    Write-Log "Discovering AWS instances..."
    $instances = @()
    try {
        $awsOutput = aws ec2 describe-instances `
            --filters "Name=instance-state-name,Values=running" `
            --query "Reservations[].Instances[].{IP:PublicIpAddress,ID:InstanceId,Name:Tags[?Key=='Name'].Value|[0]}" `
            --output json 2>$null | ConvertFrom-Json
        
        foreach ($instance in $awsOutput) {
            if ($instance.IP) {
                $instances += @{
                    IP = $instance.IP
                    ID = $instance.ID
                    Name = if ($instance.Name) { $instance.Name } else { $instance.ID }
                    Provider = "aws"
                }
            }
        }
        Write-Log "Found $($instances.Count) AWS instances"
    }
    catch {
        Write-Log "AWS discovery failed: $_" "WARN"
    }
    return $instances
}

function Discover-GCP {
    Write-Log "Discovering GCP instances..."
    $instances = @()
    try {
        $gcpOutput = gcloud compute instances list `
            --filter="status=RUNNING" `
            --format="json(name,networkInterfaces[0].accessConfigs[0].natIP,zone)" 2>$null | ConvertFrom-Json
        
        foreach ($instance in $gcpOutput) {
            $ip = $instance.networkInterfaces[0].accessConfigs[0].natIP
            if ($ip) {
                $instances += @{
                    IP = $ip
                    ID = $instance.name
                    Name = $instance.name
                    Provider = "gcp"
                }
            }
        }
        Write-Log "Found $($instances.Count) GCP instances"
    }
    catch {
        Write-Log "GCP discovery failed: $_" "WARN"
    }
    return $instances
}

function Discover-Azure {
    Write-Log "Discovering Azure instances..."
    $instances = @()
    try {
        $azOutput = az vm list-ip-addresses `
            --query "[].{Name:virtualMachine.name, IP:virtualMachine.network.publicIpAddresses[0].ipAddress}" `
            --output json 2>$null | ConvertFrom-Json
        
        foreach ($instance in $azOutput) {
            if ($instance.IP) {
                $instances += @{
                    IP = $instance.IP
                    ID = $instance.Name
                    Name = $instance.Name
                    Provider = "azure"
                }
            }
        }
        Write-Log "Found $($instances.Count) Azure instances"
    }
    catch {
        Write-Log "Azure discovery failed: $_" "WARN"
    }
    return $instances
}

function Provision-BurstNodes {
    param([int]$Count, [array]$CurrentNodes)
    
    $toAdd = $Count - $CurrentNodes.Count
    if ($toAdd -le 0) {
        Write-Log "Already have $($CurrentNodes.Count) nodes, no burst needed"
        return @()
    }
    
    Write-Log "Provisioning $toAdd burst nodes (splitting across providers)..."
    $newNodes = @()
    $perProvider = [math]::Ceiling($toAdd / 3)
    
    # AWS burst (t3.micro spot instances)
    # NOTE: AMI ID should be updated for your region. Get latest Ubuntu AMI:
    # aws ec2 describe-images --owners 099720109477 --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-*-22.04-amd64-server-*" --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId'
    $awsCount = [math]::Min($perProvider, $toAdd - $newNodes.Count)
    for ($i = 1; $i -le $awsCount; $i++) {
        try {
            Write-Log "Provisioning AWS burst node $i/$awsCount..."
            # Get latest Ubuntu 22.04 AMI dynamically
            $ami = aws ec2 describe-images `
                --owners 099720109477 `
                --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-*-22.04-amd64-server-*" `
                --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' `
                --output text 2>$null
            
            if (-not $ami) {
                $ami = "ami-0c55b159cbfafe1f0"  # Fallback AMI
                Write-Log "Using fallback AMI: $ami" "WARN"
            }
            
            $result = aws ec2 run-instances `
                --image-id $ami `
                --instance-type t3.micro `
                --instance-market-options "MarketType=spot" `
                --count 1 `
                --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=swarm-burst-$i},{Key=Purpose,Value=cloud-swarm}]" `
                --output json 2>$null | ConvertFrom-Json
            
            if ($result.Instances[0].PublicIpAddress) {
                $newNodes += @{
                    IP = $result.Instances[0].PublicIpAddress
                    ID = $result.Instances[0].InstanceId
                    Name = "swarm-burst-aws-$i"
                    Provider = "aws"
                }
            }
        }
        catch {
            Write-Log "Failed to provision AWS burst node: $_" "WARN"
        }
    }
    
    # GCP burst
    $gcpCount = [math]::Min($perProvider, $toAdd - $newNodes.Count)
    for ($i = 1; $i -le $gcpCount; $i++) {
        try {
            Write-Log "Provisioning GCP burst node $i/$gcpCount..."
            $name = "swarm-burst-gcp-$i"
            gcloud compute instances create $name `
                --machine-type=e2-micro `
                --preemptible `
                --zone=us-central1-a 2>$null
            
            $ip = gcloud compute instances describe $name `
                --zone=us-central1-a `
                --format="value(networkInterfaces[0].accessConfigs[0].natIP)" 2>$null
            
            if ($ip) {
                $newNodes += @{
                    IP = $ip
                    ID = $name
                    Name = $name
                    Provider = "gcp"
                }
            }
        }
        catch {
            Write-Log "Failed to provision GCP burst node: $_" "WARN"
        }
    }
    
    # Azure burst
    $azureCount = [math]::Min($perProvider, $toAdd - $newNodes.Count)
    for ($i = 1; $i -le $azureCount; $i++) {
        try {
            Write-Log "Provisioning Azure burst node $i/$azureCount..."
            $name = "swarm-burst-azure-$i"
            az vm create `
                --resource-group strategickhaos-swarm `
                --name $name `
                --image Ubuntu2204 `
                --size Standard_B1s `
                --priority Spot `
                --output json 2>$null | Out-Null
            
            $ip = az vm list-ip-addresses `
                --name $name `
                --query "[0].virtualMachine.network.publicIpAddresses[0].ipAddress" `
                --output tsv 2>$null
            
            if ($ip) {
                $newNodes += @{
                    IP = $ip
                    ID = $name
                    Name = $name
                    Provider = "azure"
                }
            }
        }
        catch {
            Write-Log "Failed to provision Azure burst node: $_" "WARN"
        }
    }
    
    Write-Log "Provisioned $($newNodes.Count) new burst nodes"
    return $newNodes
}

function Write-Inventory {
    param([array]$Nodes, [string]$Path)
    
    $content = @"
# Cloud Swarm Inventory - Generated $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# Total nodes: $($Nodes.Count)

[all_cloud_terminals]
"@

    foreach ($node in $Nodes) {
        $content += "`n$($node.IP) ansible_host=$($node.IP) node_name=$($node.Name) cloud_provider=$($node.Provider)"
    }
    
    # Group by provider
    $content += "`n`n[aws_nodes]"
    foreach ($node in ($Nodes | Where-Object { $_.Provider -eq "aws" })) {
        $content += "`n$($node.IP)"
    }
    
    $content += "`n`n[gcp_nodes]"
    foreach ($node in ($Nodes | Where-Object { $_.Provider -eq "gcp" })) {
        $content += "`n$($node.IP)"
    }
    
    $content += "`n`n[azure_nodes]"
    foreach ($node in ($Nodes | Where-Object { $_.Provider -eq "azure" })) {
        $content += "`n$($node.IP)"
    }
    
    $content += @"

[all_cloud_terminals:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/strategickhaos_swarm_key
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
"@

    Set-Content -Path $Path -Value $content
    Write-Log "Wrote inventory to $Path"
}

# Main execution
Write-Log "=== Cloud Inventory Discovery ==="
Write-Log "Starting discovery across AWS, GCP, and Azure..."

$allNodes = @()
$allNodes += Discover-AWS
$allNodes += Discover-GCP
$allNodes += Discover-Azure

Write-Log "Total discovered nodes: $($allNodes.Count)"

if ($Burst -gt 0) {
    Write-Log "Burst mode enabled, target: $Burst nodes"
    $burstNodes = Provision-BurstNodes -Count $Burst -CurrentNodes $allNodes
    $allNodes += $burstNodes
}

Write-Inventory -Nodes $allNodes -Path $Output

Write-Log "=== Discovery Complete ==="
Write-Log "Nodes available: $($allNodes.Count)"
Write-Log "Inventory file: $Output"
Write-Log ""
Write-Log "Next steps:"
Write-Log "  1. Bootstrap nodes: ansible-playbook -i $Output cloud_swarm_playbook.yaml"
Write-Log "  2. Fire shards: ./shard_launcher.sh $Output"
