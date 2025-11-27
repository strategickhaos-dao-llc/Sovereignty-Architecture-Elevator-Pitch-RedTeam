# compute-blake3-hash.ps1 - BLAKE3 Hash Computation and Provenance Update Script
# Downloads the official b3sum executable and computes hashes for artifacts
#
# Usage:
#   .\scripts\compute-blake3-hash.ps1 -ArtifactPath "path\to\artifact.tar.gz"
#   .\scripts\compute-blake3-hash.ps1 -ArtifactPath "swarmgate_v1.0.tar.gz" -UpdateProvenance

param(
    [Parameter(Mandatory = $true)]
    [string]$ArtifactPath,
    
    [switch]$UpdateProvenance,
    
    [string]$B3SumExePath = "",
    
    [string]$ProvenanceFile = "PROVENANCE.md"
)

$ErrorActionPreference = "Stop"

function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-ColorText "[$timestamp] $Message" -Color Cyan
}

function Error {
    param([string]$Message)
    Write-ColorText "[ERROR] $Message" -Color Red
}

function Success {
    param([string]$Message)
    Write-ColorText "[SUCCESS] $Message" -Color Green
}

# Download b3sum executable if not provided
function Get-B3SumExecutable {
    if ($B3SumExePath -and (Test-Path $B3SumExePath)) {
        Log "Using provided b3sum executable: $B3SumExePath"
        return $B3SumExePath
    }
    
    # Check if b3sum is already in current directory
    $localB3Sum = Join-Path $PWD "b3sum.exe"
    if (Test-Path $localB3Sum) {
        Log "Using existing b3sum executable: $localB3Sum"
        return $localB3Sum
    }
    
    # Download the official b3sum executable
    # Note: The official release provides a standalone .exe, not a .zip
    $b3Url = "https://github.com/BLAKE3-team/BLAKE3/releases/latest/download/b3sum_windows_x64_bin.exe"
    $b3Exe = Join-Path $PWD "b3sum.exe"
    
    Log "Downloading b3sum from official BLAKE3 releases..."
    Log "URL: $b3Url"
    
    try {
        Invoke-WebRequest -Uri $b3Url -OutFile $b3Exe -UseBasicParsing
        Success "Downloaded b3sum executable to: $b3Exe"
        return $b3Exe
    }
    catch {
        Error "Failed to download b3sum: $_"
        throw
    }
}

# Compute BLAKE3 hash
function Get-Blake3Hash {
    param(
        [string]$B3SumPath,
        [string]$FilePath
    )
    
    if (-not (Test-Path $FilePath)) {
        Error "Artifact file not found: $FilePath"
        throw "File not found: $FilePath"
    }
    
    Log "Computing BLAKE3 hash for: $FilePath"
    
    try {
        $output = & $B3SumPath $FilePath 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            Error "b3sum failed with exit code: $LASTEXITCODE"
            Error "Output: $output"
            throw "b3sum execution failed"
        }
        
        # Parse the hash from output (format: "hash  filename")
        $hash = ($output -split '\s+')[0]
        
        if ($hash.Length -ne 64) {
            Error "Invalid hash length: $($hash.Length) (expected 64)"
            throw "Invalid BLAKE3 hash"
        }
        
        Success "Computed BLAKE3 hash: $hash"
        return $hash
    }
    catch {
        Error "Failed to compute hash: $_"
        throw
    }
}

# Update PROVENANCE.md with the hash
function Update-ProvenanceFile {
    param(
        [string]$Hash,
        [string]$FileName,
        [string]$ProvenancePath
    )
    
    if (-not (Test-Path $ProvenancePath)) {
        Error "Provenance file not found: $ProvenancePath"
        throw "Provenance file not found"
    }
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $hostname = $env:COMPUTERNAME
    
    $entry = @"

**Canonical BLAKE3 (Verified on $hostname at $timestamp):**
```
$hash  $FileName
```
"@
    
    Log "Updating provenance file: $ProvenancePath"
    
    try {
        Add-Content -Path $ProvenancePath -Value $entry -Encoding UTF8
        Success "Provenance updated with hash for: $FileName"
    }
    catch {
        Error "Failed to update provenance: $_"
        throw
    }
}

# Main execution
function Main {
    Write-ColorText "🔐 BLAKE3 Hash Computation Tool" -Color Magenta
    Write-Host ""
    
    try {
        # Get b3sum executable
        $b3sum = Get-B3SumExecutable
        
        # Compute hash
        $fileName = Split-Path $ArtifactPath -Leaf
        $hash = Get-Blake3Hash -B3SumPath $b3sum -FilePath $ArtifactPath
        
        # Update provenance if requested
        if ($UpdateProvenance) {
            Update-ProvenanceFile -Hash $hash -FileName $fileName -ProvenancePath $ProvenanceFile
        }
        
        Write-Host ""
        Success "🎉 Hash computation complete!"
        Write-Host ""
        Write-ColorText "BLAKE3 Hash: $hash" -Color Yellow
        Write-ColorText "File: $fileName" -Color Yellow
        
        # Return the hash for pipeline use
        return $hash
    }
    catch {
        Error "Hash computation failed: $_"
        exit 1
    }
}

# Execute main function
Main
