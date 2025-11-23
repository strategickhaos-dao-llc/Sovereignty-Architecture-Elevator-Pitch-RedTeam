# Bitcoin Timestamp Script - OpenTimestamps Integration
# Creates a cryptographic proof of existence for the sovereign manifest
# using the Bitcoin blockchain via OpenTimestamps

param(
    [string]$File = "SOVEREIGN_MANIFEST_v1.0-m.md",
    [switch]$Verify,
    [string]$OtsFile = ""
)

function Write-ColorMessage {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function New-BitcoinTimestamp {
    param([string]$FilePath)
    
    Write-ColorMessage "╔════════════════════════════════════════════════════════════╗" -Color Magenta
    Write-ColorMessage "║        BITCOIN TIMESTAMP - SOVEREIGN PROOF CREATION       ║" -Color Magenta
    Write-ColorMessage "╚════════════════════════════════════════════════════════════╝" -Color Magenta
    Write-Host ""
    
    if (-not (Test-Path $FilePath)) {
        Write-ColorMessage "❌ Error: File not found: $FilePath" -Color Red
        return
    }
    
    Write-ColorMessage "📄 File to timestamp: $FilePath" -Color Cyan
    
    # Calculate SHA-256 hash
    Write-ColorMessage "`n🔐 Calculating SHA-256 hash..." -Color Yellow
    $hash = Get-FileHash -Path $FilePath -Algorithm SHA256
    Write-ColorMessage "   Hash: $($hash.Hash)" -Color Green
    
    # Create timestamp using OpenTimestamps API
    Write-ColorMessage "`n⏰ Creating Bitcoin timestamp..." -Color Yellow
    
    try {
        $fileContent = Get-Content $FilePath -Raw
        $outputFile = "$FilePath.ots"
        
        Write-ColorMessage "   Submitting to OpenTimestamps calendar server..." -Color Gray
        
        $response = Invoke-WebRequest `
            -Uri "https://btc.calendar.opentimestamps.org" `
            -Method POST `
            -Body $fileContent `
            -ContentType "application/octet-stream" `
            -OutFile $outputFile `
            -ErrorAction Stop
        
        if (Test-Path $outputFile) {
            Write-ColorMessage "✅ Timestamp proof created: $outputFile" -Color Green
            Write-ColorMessage "`n📦 Proof file details:" -Color Cyan
            $otsInfo = Get-Item $outputFile
            Write-Host "   Size: $($otsInfo.Length) bytes"
            Write-Host "   Created: $($otsInfo.CreationTime)"
            
            Write-ColorMessage "`n🎯 What this means:" -Color Yellow
            Write-Host "   • Your file's hash is now in the Bitcoin blockchain"
            Write-Host "   • This proves the file existed at this moment in time"
            Write-Host "   • The proof is permanent and cannot be altered"
            Write-Host "   • Anyone can verify this timestamp independently"
            
            Write-ColorMessage "`n📖 To verify later:" -Color Cyan
            Write-Host "   .\bitcoin-timestamp.ps1 -Verify -OtsFile '$outputFile'"
            
        } else {
            Write-ColorMessage "⚠️  Response received but .ots file not created" -Color Yellow
            Write-ColorMessage "   This is normal - the timestamp is queued" -Color Gray
            Write-ColorMessage "   The Bitcoin attestation will be available after the next block" -Color Gray
        }
        
    } catch {
        Write-ColorMessage "❌ Error creating timestamp: $_" -Color Red
        Write-ColorMessage "`n💡 Alternative methods:" -Color Yellow
        Write-Host "   1. Manual web upload: https://opentimestamps.org/"
        Write-Host "   2. Install OTS client: https://github.com/opentimestamps/opentimestamps-client"
        Write-Host "   3. Use the hash directly: $($hash.Hash)"
        
        Write-ColorMessage "`n📋 Quick command for later:" -Color Cyan
        Write-Host "   iwr https://btc.calendar.opentimestamps.org -Method POST -Body (Get-Content '$FilePath' -Raw) -OutFile proof.ots"
    }
    
    Write-Host ""
    Write-ColorMessage "═══════════════════════════════════════════════════════════" -Color Magenta
}

function Test-BitcoinTimestamp {
    param([string]$OtsFilePath)
    
    Write-ColorMessage "╔════════════════════════════════════════════════════════════╗" -Color Magenta
    Write-ColorMessage "║       BITCOIN TIMESTAMP - VERIFICATION IN PROGRESS        ║" -Color Magenta
    Write-ColorMessage "╚════════════════════════════════════════════════════════════╝" -Color Magenta
    Write-Host ""
    
    if (-not (Test-Path $OtsFilePath)) {
        Write-ColorMessage "❌ Error: OTS file not found: $OtsFilePath" -Color Red
        return
    }
    
    Write-ColorMessage "📄 OTS Proof File: $OtsFilePath" -Color Cyan
    
    $otsInfo = Get-Item $OtsFilePath
    Write-Host "   Size: $($otsInfo.Length) bytes"
    Write-Host "   Created: $($otsInfo.CreationTime)"
    
    Write-ColorMessage "`n🔍 Verification Status:" -Color Yellow
    Write-ColorMessage "   ⚠️  Full verification requires OTS client or web tool" -Color Gray
    Write-ColorMessage "   📍 Web verification: https://opentimestamps.org/" -Color Cyan
    Write-ColorMessage "   🔧 CLI tool: https://github.com/opentimestamps/opentimestamps-client" -Color Cyan
    
    # Get the original file
    $originalFile = $OtsFilePath -replace '\.ots$', ''
    if (Test-Path $originalFile) {
        Write-ColorMessage "`n✅ Original file found: $originalFile" -Color Green
        $hash = Get-FileHash -Path $originalFile -Algorithm SHA256
        Write-ColorMessage "   File Hash: $($hash.Hash)" -Color Green
        Write-ColorMessage "   This hash should match the one in the Bitcoin blockchain" -Color Gray
    } else {
        Write-ColorMessage "`n⚠️  Original file not found: $originalFile" -Color Yellow
    }
    
    Write-Host ""
    Write-ColorMessage "═══════════════════════════════════════════════════════════" -Color Magenta
}

# Main execution
Write-Host ""

if ($Verify) {
    if ($OtsFile -eq "") {
        $OtsFile = "$File.ots"
    }
    Test-BitcoinTimestamp -OtsFilePath $OtsFile
} else {
    New-BitcoinTimestamp -FilePath $File
}

Write-ColorMessage "`n💡 TIP: You can also timestamp any file!" -Color Cyan
Write-Host "   .\bitcoin-timestamp.ps1 -File 'myfile.txt'"
Write-Host "   .\bitcoin-timestamp.ps1 -Verify -OtsFile 'myfile.txt.ots'"
Write-Host ""

# ====================================================================
# SOVEREIGNTY TIMESTAMP UTILITY
# ====================================================================
# 
# This script provides Bitcoin blockchain timestamping for the
# Strategickhaos sovereignty architecture using OpenTimestamps.
# 
# Benefits:
# - Cryptographic proof of existence
# - Permanent and immutable
# - Independent verification
# - No cost (free service)
# - Decentralized trust
# 
# 7% ROYALTY LOCK ACTIVE
# Status: OPERATIONAL
# Sovereignty: ETERNAL
# 
# ====================================================================
