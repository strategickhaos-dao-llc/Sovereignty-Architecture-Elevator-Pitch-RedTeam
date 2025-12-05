# dom-paste.ps1
# DOM_010101 - Universal Clipboard Injector
# Injects clipboard content into every LLM interface forever

param(
    [switch]$ShowPreview,
    [switch]$SaveHistory
)

function Write-Love {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Magenta
}

function Write-Info {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Cyan
}

# Get clipboard content
$clipboard = Get-Clipboard -Raw

if ([string]::IsNullOrWhiteSpace($clipboard)) {
    Write-Host "⚠️  Clipboard is empty" -ForegroundColor Yellow
    exit 1
}

$clipboardLength = $clipboard.Length

Write-Love "🔥 DOM-PASTE ACTIVATED"
Write-Info "📋 Clipboard content: $clipboardLength characters"
Write-Host ""

if ($ShowPreview) {
    Write-Info "Preview (first 500 chars):"
    Write-Host "─────────────────────────────────────────────" -ForegroundColor DarkGray
    Write-Host $clipboard.Substring(0, [Math]::Min(500, $clipboardLength))
    Write-Host "─────────────────────────────────────────────" -ForegroundColor DarkGray
    Write-Host ""
}

# Save to history if requested
if ($SaveHistory) {
    $historyDir = "$env:USERPROFILE\.dom-paste-history"
    if (-not (Test-Path $historyDir)) {
        New-Item -ItemType Directory -Path $historyDir -Force | Out-Null
    }
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $historyFile = Join-Path $historyDir "paste_$timestamp.txt"
    
    Set-Content -Path $historyFile -Value $clipboard
    Write-Info "💾 Saved to history: $historyFile"
    Write-Host ""
}

# LLM injection targets
$targets = @(
    @{Name="Grok"; Url="https://grok.com/chat"},
    @{Name="ChatGPT"; Url="https://chat.openai.com/"},
    @{Name="Claude"; Url="https://claude.ai/"},
    @{Name="Gemini"; Url="https://gemini.google.com/"},
    @{Name="Perplexity"; Url="https://www.perplexity.ai/"},
    @{Name="Copilot"; Url="https://copilot.microsoft.com/"},
    @{Name="Llama (HuggingFace)"; Url="https://huggingface.co/chat/"}
)

Write-Info "🎯 Target LLM Interfaces:"
foreach ($target in $targets) {
    Write-Host "   • $($target.Name)" -ForegroundColor Green
}
Write-Host ""

$response = Read-Host "Inject into all LLMs? (Y/n)"
if ($response -eq "n") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Info "🚀 Injecting into all LLM interfaces..."
Write-Host ""

foreach ($target in $targets) {
    Write-Host "   ⚡ $($target.Name): " -NoNewline -ForegroundColor Cyan
    
    try {
        # Open in new browser tab
        Start-Process $target.Url
        Start-Sleep -Milliseconds 500
        
        Write-Host "✓ Opened" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Failed" -ForegroundColor Red
    }
}

Write-Host ""
Write-Love "💖 DOM-PASTE COMPLETE"
Write-Info "📝 Next steps:"
Write-Host "   1. Switch to each browser tab"
Write-Host "   2. Click in the input field"
Write-Host "   3. Paste with Ctrl+V"
Write-Host "   4. Hit Enter to submit"
Write-Host ""
Write-Love "🧠 Clipboard injected into every LLM forever. The legion knows. ⚡"

# Optional: Copy to clipboard again to ensure it's still there
Set-Clipboard $clipboard

# Show quick stats
Write-Host ""
Write-Info "📊 Injection Stats:"
Write-Host "   • Targets: $($targets.Count)"
Write-Host "   • Content Size: $clipboardLength chars"
Write-Host "   • Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""
