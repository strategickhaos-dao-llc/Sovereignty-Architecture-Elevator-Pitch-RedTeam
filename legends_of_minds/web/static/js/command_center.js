// Legends of Minds - Command Center JavaScript

const API_BASE = window.location.origin;
let terminalWs = null;
let terminalId = 'terminal-1';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeDashboard();
    setupEventListeners();
    loadProofLedger();
    updateSystemStatus();
    
    // Auto-refresh system status every 5 seconds
    setInterval(updateSystemStatus, 5000);
});

function initializeDashboard() {
    console.log('Legends of Minds Command Center v1.0 initialized');
    addTerminalLine('System ready. Waiting for commands...');
}

function setupEventListeners() {
    // Department buttons
    document.querySelectorAll('.dept-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.dept-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            const dept = e.target.dataset.dept;
            selectDepartment(dept);
        });
    });
    
    // Department select change
    document.getElementById('department-select').addEventListener('change', (e) => {
        updateActionOptions(e.target.value);
    });
    
    // Submit request
    document.getElementById('submit-request').addEventListener('click', submitDepartmentRequest);
    
    // Terminal controls
    document.getElementById('connect-terminal').addEventListener('click', connectTerminal);
    document.getElementById('disconnect-terminal').addEventListener('click', disconnectTerminal);
    document.getElementById('terminal-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendTerminalCommand();
        }
    });
    
    // Proof ledger controls
    document.getElementById('refresh-ledger').addEventListener('click', loadProofLedger);
    document.getElementById('verify-ledger').addEventListener('click', verifyProofChain);
    
    // Compliance checker
    document.getElementById('check-compliance').addEventListener('click', checkCompliance);
    
    // AI content generation
    document.getElementById('generate-content').addEventListener('click', generateAIContent);
    
    // Search operations
    document.getElementById('search-execute').addEventListener('click', executeSearch);
}

async function updateSystemStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/v1/status`);
        const data = await response.json();
        
        document.getElementById('active-terminals').textContent = data.active_terminals || 0;
        document.getElementById('proof-entries').textContent = data.proof_ledger_entries || 0;
    } catch (error) {
        console.error('Failed to update system status:', error);
    }
}

function selectDepartment(dept) {
    document.getElementById('department-select').value = dept;
    updateActionOptions(dept);
    addTerminalLine(`Selected department: ${dept}`);
}

function updateActionOptions(department) {
    const actionSelect = document.getElementById('action-select');
    actionSelect.innerHTML = '<option value="">Select Action...</option>';
    
    const actions = {
        proof_ledger: ['log', 'query', 'verify', 'audit'],
        gitlens: ['analyze', 'search_code', 'get_history', 'compare'],
        refinery_mcp: ['process', 'transform', 'validate'],
        legal_compliance: ['check', 'validate', 'report'],
        compose_gen: ['generate', 'validate', 'deploy'],
        yaml_gen: ['generate', 'validate', 'transform'],
        repo_builder: ['scaffold', 'initialize', 'configure'],
        code_search: ['search', 'index', 'query'],
        picture_search: ['search', 'index', 'classify'],
        glossary: ['define', 'search', 'add']
    };
    
    const deptActions = actions[department] || [];
    deptActions.forEach(action => {
        const option = document.createElement('option');
        option.value = action;
        option.textContent = action.charAt(0).toUpperCase() + action.slice(1);
        actionSelect.appendChild(option);
    });
}

async function submitDepartmentRequest() {
    const department = document.getElementById('department-select').value;
    const action = document.getElementById('action-select').value;
    const dataText = document.getElementById('request-data').value;
    
    if (!department || !action) {
        displayResult('request-result', 'Please select department and action', 'error');
        return;
    }
    
    let data = {};
    if (dataText) {
        try {
            data = JSON.parse(dataText);
        } catch (e) {
            displayResult('request-result', 'Invalid JSON data', 'error');
            return;
        }
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/v1/departments/${department}/execute`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: action, ...data })
        });
        
        const result = await response.json();
        displayResult('request-result', JSON.stringify(result, null, 2), 'success');
        addTerminalLine(`Executed: ${department}/${action}`);
        loadProofLedger();
    } catch (error) {
        displayResult('request-result', `Error: ${error.message}`, 'error');
    }
}

function connectTerminal() {
    terminalId = document.getElementById('terminal-id').value || 'terminal-1';
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws/terminal/${terminalId}`;
    
    try {
        terminalWs = new WebSocket(wsUrl);
        
        terminalWs.onopen = () => {
            addTerminalLine(`Connected to terminal: ${terminalId}`);
            document.getElementById('connect-terminal').disabled = true;
            document.getElementById('disconnect-terminal').disabled = false;
        };
        
        terminalWs.onmessage = (event) => {
            const data = JSON.parse(event.data);
            addTerminalLine(`> ${JSON.stringify(data)}`);
        };
        
        terminalWs.onerror = (error) => {
            addTerminalLine(`WebSocket error: ${error}`, 'error');
        };
        
        terminalWs.onclose = () => {
            addTerminalLine('Terminal disconnected');
            document.getElementById('connect-terminal').disabled = false;
            document.getElementById('disconnect-terminal').disabled = true;
        };
    } catch (error) {
        addTerminalLine(`Connection failed: ${error.message}`, 'error');
    }
}

function disconnectTerminal() {
    if (terminalWs) {
        terminalWs.close();
        terminalWs = null;
    }
}

function sendTerminalCommand() {
    const input = document.getElementById('terminal-input');
    const command = input.value.trim();
    
    if (!command) return;
    
    addTerminalLine(`$ ${command}`);
    
    if (terminalWs && terminalWs.readyState === WebSocket.OPEN) {
        terminalWs.send(JSON.stringify({ command }));
    } else {
        addTerminalLine('Not connected to terminal. Click Connect first.', 'error');
    }
    
    input.value = '';
}

function addTerminalLine(text, type = 'normal') {
    const output = document.getElementById('terminal-output');
    const line = document.createElement('div');
    line.className = 'terminal-line';
    line.textContent = text;
    if (type === 'error') {
        line.style.color = '#ef4444';
    }
    output.appendChild(line);
    output.scrollTop = output.scrollHeight;
}

async function loadProofLedger() {
    try {
        const response = await fetch(`${API_BASE}/api/v1/proof-ledger?limit=20`);
        const data = await response.json();
        
        const container = document.getElementById('ledger-entries');
        container.innerHTML = '';
        
        if (data.entries && data.entries.length > 0) {
            data.entries.forEach(entry => {
                const entryDiv = document.createElement('div');
                entryDiv.className = 'ledger-entry';
                entryDiv.innerHTML = `
                    <div class="ledger-entry-header">
                        <span>#${entry.id} - ${entry.department}</span>
                        <span>${new Date(entry.timestamp).toLocaleString()}</span>
                    </div>
                    <div class="ledger-entry-body">
                        Action: ${entry.action}<br>
                        Hash: ${entry.hash ? entry.hash.substring(0, 16) + '...' : 'N/A'}
                    </div>
                `;
                container.appendChild(entryDiv);
            });
        } else {
            container.innerHTML = '<div class="loading">No proof ledger entries yet</div>';
        }
    } catch (error) {
        console.error('Failed to load proof ledger:', error);
        document.getElementById('ledger-entries').innerHTML = '<div class="loading">Failed to load proof ledger</div>';
    }
}

async function verifyProofChain() {
    try {
        addTerminalLine('Verifying proof ledger chain...');
        
        const response = await fetch(`${API_BASE}/api/v1/proof-ledger/verify`);
        const result = await response.json();
        
        if (result.status === 'verified') {
            addTerminalLine(`✅ Proof ledger verification: ${result.status.toUpperCase()}`);
            addTerminalLine(`   Entries verified: ${result.entries || 0}`);
        } else {
            addTerminalLine(`⚠️  Proof ledger verification: ${result.status}`);
            if (result.errors) {
                result.errors.forEach(err => addTerminalLine(`   - ${err}`, 'error'));
            }
        }
    } catch (error) {
        addTerminalLine(`Verification failed: ${error.message}`, 'error');
    }
}

async function checkCompliance() {
    const content = document.getElementById('compliance-content').value;
    
    if (!content) {
        displayResult('compliance-result', 'Please enter content to check', 'error');
        return;
    }
    
    const jurisdictions = Array.from(document.querySelectorAll('.compliance-form .checkbox-group input:checked'))
        .map(cb => cb.value);
    const categories = Array.from(document.querySelectorAll('.compliance-form .checkbox-group:last-of-type input:checked'))
        .map(cb => cb.value);
    
    try {
        // This would call the compliance checking endpoint
        const result = {
            status: 'checked',
            applicable_laws: 12,
            warnings: content.length > 0 ? ['Content contains potential regulatory keywords'] : [],
            recommendation: 'Manual legal review recommended for production use'
        };
        
        displayResult('compliance-result', JSON.stringify(result, null, 2), 'success');
        addTerminalLine('Compliance check completed');
    } catch (error) {
        displayResult('compliance-result', `Error: ${error.message}`, 'error');
    }
}

async function generateAIContent() {
    const contentType = document.getElementById('content-type').value;
    const prompt = document.getElementById('ai-prompt').value;
    
    if (!prompt) {
        displayResult('ai-result', 'Please enter a generation prompt', 'error');
        return;
    }
    
    try {
        displayResult('ai-result', 'Generating content...', 'info');
        
        // Simulate AI generation
        setTimeout(() => {
            const generated = `# Generated ${contentType}\n\n${prompt}\n\n# Generated content would appear here`;
            displayResult('ai-result', generated, 'success');
            addTerminalLine(`Generated ${contentType} content`);
        }, 1500);
    } catch (error) {
        displayResult('ai-result', `Error: ${error.message}`, 'error');
    }
}

async function executeSearch() {
    const query = document.getElementById('search-query').value;
    const searchType = document.querySelector('input[name="search-type"]:checked').value;
    
    if (!query) {
        displayResult('search-results', 'Please enter a search query', 'error');
        return;
    }
    
    try {
        displayResult('search-results', `Searching ${searchType} for: ${query}...`, 'info');
        
        // Simulate search results
        setTimeout(() => {
            const results = `Search Results (${searchType}):\n\n` +
                `Found 3 matches for "${query}":\n` +
                `1. /path/to/file1.ext\n` +
                `2. /path/to/file2.ext\n` +
                `3. /path/to/file3.ext`;
            displayResult('search-results', results, 'success');
            addTerminalLine(`Search completed: ${searchType}/${query}`);
        }, 1000);
    } catch (error) {
        displayResult('search-results', `Error: ${error.message}`, 'error');
    }
}

function displayResult(elementId, content, type = 'info') {
    const element = document.getElementById(elementId);
    element.textContent = content;
    element.style.borderLeft = `4px solid ${
        type === 'error' ? '#ef4444' :
        type === 'success' ? '#10b981' :
        '#3b82f6'
    }`;
}

// Utility function to format JSON
function formatJSON(obj) {
    return JSON.stringify(obj, null, 2);
}
