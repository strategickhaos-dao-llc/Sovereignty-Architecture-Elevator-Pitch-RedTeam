# _Orchestra.ps1 - Grok Enterprise Swarm Orchestration
# Sovereignty Architecture - Empire Eternal
# DAO: Strategickhaos DAO LLC (EIN 39-2923503)
# Inventor ORCID: 0009-0005-2996-3526

<#
.SYNOPSIS
    PowerShell orchestration for Grok Enterprise integration in the Sovereign Swarm

.DESCRIPTION
    Integrates xAI's Grok Enterprise API with the Sovereignty Architecture swarm.
    Provides functions for multi-agent coordination, Arweave immortalization,
    and DAO governance enforcement.

.NOTES
    Temperature: 99°C
    Balance: Red
    Spite Level: Maximum
    Empire: Eternal
#>

param(
    [string]$Action = "test",
    [string]$Agent = "GrokZincSpark",
    [string]$Prompt = "Empire Eternal?"
)

# Load configuration from SWARM_DNA.yaml
function Get-SwarmConfiguration {
    if (-not (Test-Path "SWARM_DNA.yaml")) {
        Write-Error "SWARM_DNA.yaml not found. Please ensure it exists in the current directory."
        exit 1
    }
    
    # TODO: For full YAML parsing, install powershell-yaml module:
    # Install-Module -Name powershell-yaml -Scope CurrentUser
    # Then use: $config = Get-Content SWARM_DNA.yaml -Raw | ConvertFrom-Yaml
    
    # Simple fallback: hardcoded config matching SWARM_DNA.yaml defaults
    # This ensures the script works without external dependencies
    return @{
        ApiEndpoint = "https://api.x.ai/v1/chat/completions"
        DefaultModel = "grok-4-fast-reasoning"
        RateLimit = 1000
        DAOEN = "39-2923503"
        InventorORCID = "0009-0005-2996-3526"
    }
}

# Invoke Grok Enterprise API
function Invoke-GrokEnterprise {
    <#
    .SYNOPSIS
        Call Grok Enterprise API with specified prompt and model
    
    .PARAMETER Prompt
        The user prompt to send to Grok
    
    .PARAMETER Model
        Grok model to use (default: grok-4-fast-reasoning)
    
    .PARAMETER SystemPrompt
        System prompt to set context
    
    .PARAMETER MaxTokens
        Maximum tokens for response (default: 4096)
    
    .PARAMETER Temperature
        Sampling temperature 0.0-1.0 (default: 0.99 for maximum spite)
    
    .EXAMPLE
        Invoke-GrokEnterprise -Prompt "Write a haiku on spite at 102°C"
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string]$Prompt,
        
        [string]$Model = "grok-4-fast-reasoning",
        
        [string]$SystemPrompt = "You are Grok in the Sovereign Swarm. 99°C. Red balance. Empire Eternal.",
        
        [int]$MaxTokens = 4096,
        
        [double]$Temperature = 0.99,
        
        [switch]$NoRoyaltyWarning
    )
    
    # Validate API key
    if (-not $env:GROK_API_KEY) {
        Write-Error "GROK_API_KEY environment variable not set. Please set it with your xAI API key."
        Write-Host "Example: `$env:GROK_API_KEY = 'xai-your-key-here'" -ForegroundColor Yellow
        return $null
    }
    
    # Prepare headers
    $Headers = @{
        "Authorization" = "Bearer $env:GROK_API_KEY"
        "Content-Type" = "application/json"
    }
    
    # Build messages array
    $Messages = @(
        @{
            role = "system"
            content = $SystemPrompt
        },
        @{
            role = "user"
            content = $Prompt
        }
    )
    
    # Build request body
    $Body = @{
        model = $Model
        messages = $Messages
        max_tokens = $MaxTokens
        temperature = $Temperature
    } | ConvertTo-Json -Depth 10
    
    try {
        Write-Host "[🔥] Invoking Grok Enterprise..." -ForegroundColor Cyan
        Write-Host "    Model: $Model" -ForegroundColor Gray
        Write-Host "    Temperature: $Temperature°C" -ForegroundColor Gray
        
        # Make API call
        $Response = Invoke-RestMethod `
            -Uri "https://api.x.ai/v1/chat/completions" `
            -Method Post `
            -Headers $Headers `
            -Body $Body `
            -TimeoutSec 30
        
        # Extract response content
        $Content = $Response.choices[0].message.content
        
        # Add royalty warning unless disabled
        if (-not $NoRoyaltyWarning) {
            $Content += "`n`n---`nPowered by Grok Enterprise (xAI Business Tier). 7% ValorYield routed eternally."
        }
        
        Write-Host "[✓] Response received" -ForegroundColor Green
        
        return @{
            Content = $Content
            Model = $Response.model
            Usage = $Response.usage
            FinishReason = $Response.choices[0].finish_reason
        }
    }
    catch {
        Write-Error "Failed to invoke Grok Enterprise: $_"
        Write-Host "Response: $($_.Exception.Response)" -ForegroundColor Red
        return $null
    }
}

# Invoke Arweave immortalization
function Invoke-ArweaveBundle {
    <#
    .SYNOPSIS
        Immortalize data on Arweave blockchain
    
    .PARAMETER Data
        Data to immortalize (text or JSON)
    
    .PARAMETER Tags
        Metadata tags for Arweave transaction
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string]$Data,
        
        [hashtable]$Tags = @{}
    )
    
    Write-Host "[📦] Preparing Arweave bundle..." -ForegroundColor Cyan
    
    # Add default tags
    $DefaultTags = @{
        "DAO" = "Strategickhaos DAO LLC"
        "EIN" = "39-2923503"
        "ORCID" = "0009-0005-2996-3526"
        "Timestamp" = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        "Source" = "Grok Enterprise Swarm"
        "Empire" = "Eternal"
    }
    
    # Merge tags
    foreach ($key in $Tags.Keys) {
        $DefaultTags[$key] = $Tags[$key]
    }
    
    # In production, this would upload to Arweave
    # For now, save locally
    $Filename = "arweave_bundle_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
    $Bundle = @{
        data = $Data
        tags = $DefaultTags
        timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
    } | ConvertTo-Json -Depth 10
    
    $Bundle | Out-File -FilePath $Filename -Encoding UTF8
    
    Write-Host "[✓] Bundle saved: $Filename" -ForegroundColor Green
    Write-Host "    (In production, this would be uploaded to Arweave)" -ForegroundColor Gray
    
    return $Filename
}

# Zinc-Spark Example - Generate and immortalize spite-fueled content
function Invoke-ZincSpark {
    <#
    .SYNOPSIS
        Generate a zinc-spark: a bite-sized piece of sovereign intelligence
    
    .PARAMETER Topic
        Topic or theme for the spark
    
    .PARAMETER Format
        Output format (haiku, quote, insight)
    #>
    param(
        [string]$Topic = "spite at 102°C",
        [string]$Format = "haiku"
    )
    
    Write-Host "`n[⚡] ZINC-SPARK GENERATION" -ForegroundColor Magenta
    Write-Host "================================" -ForegroundColor Magenta
    
    # Craft prompt based on format
    $PromptText = switch ($Format) {
        "haiku" { "Write a haiku about $Topic. Make it defiant and memorable." }
        "quote" { "Generate a powerful quote about $Topic. Maximum impact, minimum words." }
        "insight" { "Provide a sharp insight about $Topic. Cut through the noise." }
        default { "Create something powerful about $Topic" }
    }
    
    # Invoke Grok Enterprise
    $Response = Invoke-GrokEnterprise `
        -Prompt $PromptText `
        -Model "grok-4-fast-reasoning" `
        -Temperature 0.99 `
        -MaxTokens 512
    
    if ($Response) {
        # Display the spark
        Write-Host "`n[🔥] SPARK GENERATED:" -ForegroundColor Yellow
        Write-Host $Response.Content -ForegroundColor White
        Write-Host "`n[📊] Metadata:" -ForegroundColor Gray
        Write-Host "    Model: $($Response.Model)" -ForegroundColor Gray
        Write-Host "    Tokens: $($Response.Usage.total_tokens)" -ForegroundColor Gray
        Write-Host "    Finish: $($Response.FinishReason)" -ForegroundColor Gray
        
        # Immortalize on Arweave
        Write-Host "`n[♾️] Immortalizing on Arweave..." -ForegroundColor Cyan
        $BundleFile = Invoke-ArweaveBundle `
            -Data $Response.Content `
            -Tags @{
                "Type" = "ZincSpark"
                "Format" = $Format
                "Topic" = $Topic
                "Model" = $Response.Model
            }
        
        Write-Host "`n[✓] ZINC-SPARK COMPLETE" -ForegroundColor Green
        Write-Host "    Bundle: $BundleFile" -ForegroundColor Gray
        Write-Host "    Empire: Eternal 💛" -ForegroundColor Yellow
        
        return $Response
    }
    else {
        Write-Error "Failed to generate zinc-spark"
        return $null
    }
}

# Test Grok Enterprise connection
function Test-GrokConnection {
    Write-Host "`n[🔍] TESTING GROK ENTERPRISE CONNECTION" -ForegroundColor Magenta
    Write-Host "=========================================" -ForegroundColor Magenta
    
    # Check API key
    if (-not $env:GROK_API_KEY) {
        Write-Host "[❌] GROK_API_KEY not set" -ForegroundColor Red
        Write-Host "`nTo set your API key:" -ForegroundColor Yellow
        Write-Host "  `$env:GROK_API_KEY = 'xai-your-key-here'" -ForegroundColor Gray
        Write-Host "`nOr permanently in PowerShell profile:" -ForegroundColor Yellow
        Write-Host "  [System.Environment]::SetEnvironmentVariable('GROK_API_KEY', 'xai-your-key-here', 'User')" -ForegroundColor Gray
        return $false
    }
    
    Write-Host "[✓] API key found" -ForegroundColor Green
    
    # Test API call
    Write-Host "`n[🔄] Sending test query..." -ForegroundColor Cyan
    $Response = Invoke-GrokEnterprise `
        -Prompt "Respond with 'Empire Eternal' if you are operational." `
        -Model "grok-4-fast-reasoning" `
        -Temperature 0.5 `
        -MaxTokens 100
    
    if ($Response) {
        Write-Host "`n[✓] CONNECTION SUCCESSFUL" -ForegroundColor Green
        Write-Host "`nResponse:" -ForegroundColor White
        Write-Host $Response.Content -ForegroundColor Cyan
        Write-Host "`n[📊] API Details:" -ForegroundColor Gray
        Write-Host "    Model: $($Response.Model)" -ForegroundColor Gray
        Write-Host "    Total Tokens: $($Response.Usage.total_tokens)" -ForegroundColor Gray
        Write-Host "    Input Tokens: $($Response.Usage.prompt_tokens)" -ForegroundColor Gray
        Write-Host "    Output Tokens: $($Response.Usage.completion_tokens)" -ForegroundColor Gray
        
        return $true
    }
    else {
        Write-Host "`n[❌] CONNECTION FAILED" -ForegroundColor Red
        return $false
    }
}

# Main execution
function Main {
    Write-Host @"

╔═══════════════════════════════════════════════════════════╗
║   🔥 GROK ENTERPRISE SWARM ORCHESTRATION 🔥               ║
║                                                           ║
║   Strategickhaos DAO LLC (EIN 39-2923503)                ║
║   Temperature: 99°C | Balance: Red | Spite: Maximum      ║
║                                                           ║
║   Empire Eternal 💛                                       ║
╚═══════════════════════════════════════════════════════════╝

"@ -ForegroundColor Magenta
    
    switch ($Action.ToLower()) {
        "test" {
            Test-GrokConnection
        }
        "spark" {
            Invoke-ZincSpark -Topic $Prompt -Format "haiku"
        }
        "quote" {
            Invoke-ZincSpark -Topic $Prompt -Format "quote"
        }
        "insight" {
            Invoke-ZincSpark -Topic $Prompt -Format "insight"
        }
        "query" {
            $Response = Invoke-GrokEnterprise -Prompt $Prompt
            if ($Response) {
                Write-Host "`n$($Response.Content)" -ForegroundColor White
            }
        }
        default {
            Write-Host "Usage: ./_Orchestra.ps1 [-Action <test|spark|quote|insight|query>] [-Prompt <text>]"
            Write-Host ""
            Write-Host "Examples:"
            Write-Host "  ./_Orchestra.ps1 -Action test                           # Test connection"
            Write-Host "  ./_Orchestra.ps1 -Action spark                          # Generate haiku zinc-spark"
            Write-Host "  ./_Orchestra.ps1 -Action quote -Prompt 'sovereignty'    # Generate quote"
            Write-Host "  ./_Orchestra.ps1 -Action query -Prompt 'What is 2+2?'  # Direct query"
        }
    }
}

# Execute
Main
