// Application state
const state = {
    user: null,
    currentView: 'chat',
    conversationId: null
};

// API helper
async function api(endpoint, options = {}) {
    const response = await fetch(`/api${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        credentials: 'include'
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || 'Request failed');
    }

    return data;
}

// Show error message
function showError(message, elementId = 'auth-error') {
    const errorEl = document.getElementById(elementId);
    errorEl.textContent = message;
    errorEl.style.display = 'block';
    setTimeout(() => {
        errorEl.style.display = 'none';
    }, 5000);
}

// Initialize app
async function init() {
    try {
        const data = await api('/auth/me');
        state.user = data.user;
        showDashboard();
    } catch (error) {
        showLogin();
    }

    setupEventListeners();
}

// Show login view
function showLogin() {
    document.getElementById('login-view').style.display = 'block';
    document.getElementById('dashboard-view').style.display = 'none';
}

// Show dashboard
function showDashboard() {
    document.getElementById('login-view').style.display = 'none';
    document.getElementById('dashboard-view').style.display = 'block';
    document.getElementById('user-info').textContent = `${state.user.username} (${state.user.role})`;
    
    // Show admin panels if admin
    if (state.user.role === 'admin') {
        document.getElementById('admin-invite-panel').style.display = 'block';
        loadAllInvites();
    }
    
    loadMyInvites();
    loadProfile();
}

// Setup event listeners
function setupEventListeners() {
    // Auth forms
    document.getElementById('login-form-element').addEventListener('submit', handleLogin);
    document.getElementById('register-form-element').addEventListener('submit', handleRegister);
    document.getElementById('logout-btn').addEventListener('click', handleLogout);
    
    // Form switchers
    document.getElementById('show-register').addEventListener('click', (e) => {
        e.preventDefault();
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('register-form').style.display = 'block';
    });
    
    document.getElementById('show-login').addEventListener('click', (e) => {
        e.preventDefault();
        document.getElementById('register-form').style.display = 'none';
        document.getElementById('login-form').style.display = 'block';
    });
    
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const view = e.target.dataset.view;
            switchView(view);
        });
    });
    
    // Chat
    document.getElementById('send-btn').addEventListener('click', sendMessage);
    document.getElementById('chat-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Invite generation
    const inviteForm = document.getElementById('generate-invite-form');
    if (inviteForm) {
        inviteForm.addEventListener('submit', handleGenerateInvite);
    }
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const data = await api('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        state.user = data.user;
        showDashboard();
    } catch (error) {
        showError(error.message);
    }
}

// Handle registration
async function handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const inviteCode = document.getElementById('register-invite').value;
    
    try {
        const data = await api('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password, inviteCode })
        });
        
        state.user = data.user;
        showDashboard();
    } catch (error) {
        showError(error.message);
    }
}

// Handle logout
async function handleLogout() {
    try {
        await api('/auth/logout', { method: 'POST' });
        state.user = null;
        state.conversationId = null;
        document.getElementById('chat-messages').innerHTML = '';
        showLogin();
    } catch (error) {
        showError(error.message);
    }
}

// Switch dashboard view
function switchView(view) {
    state.currentView = view;
    
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.view === view) {
            link.classList.add('active');
        }
    });
    
    // Show/hide sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });
    
    document.getElementById(`${view}-section`).style.display = 'block';
}

// Send chat message
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    const model = document.getElementById('model-select').value;
    
    // Add user message to UI
    addMessageToUI('user', message);
    input.value = '';
    
    // Disable send button
    const sendBtn = document.getElementById('send-btn');
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<span class="loading"></span>';
    
    try {
        const data = await api('/llm/chat', {
            method: 'POST',
            body: JSON.stringify({
                message,
                conversationId: state.conversationId,
                model
            })
        });
        
        state.conversationId = data.conversationId;
        addMessageToUI('assistant', data.message);
    } catch (error) {
        addMessageToUI('assistant', `Error: ${error.message}`);
    } finally {
        sendBtn.disabled = false;
        sendBtn.textContent = 'Send';
    }
}

// Add message to UI
function addMessageToUI(role, content) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    
    const roleEl = document.createElement('div');
    roleEl.className = 'message-role';
    roleEl.textContent = role === 'user' ? 'You' : 'AI Assistant';
    
    const contentEl = document.createElement('div');
    contentEl.textContent = content;
    
    messageEl.appendChild(roleEl);
    messageEl.appendChild(contentEl);
    messagesDiv.appendChild(messageEl);
    
    // Scroll to bottom
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Generate invite
async function handleGenerateInvite(e) {
    e.preventDefault();
    const email = document.getElementById('invite-email').value;
    const days = parseInt(document.getElementById('invite-days').value);
    
    try {
        const data = await api('/invites/generate', {
            method: 'POST',
            body: JSON.stringify({ email, expiresInDays: days })
        });
        
        // Show result
        const resultDiv = document.getElementById('invite-result');
        resultDiv.innerHTML = `
            <div class="success-message">
                <strong>Invite generated successfully!</strong><br>
                Email: ${data.email}<br>
                Code: <span class="invite-code">${data.inviteCode}</span><br>
                Invite URL: <a href="${data.inviteUrl}" target="_blank">${data.inviteUrl}</a><br>
                Expires: ${new Date(data.expiresAt).toLocaleDateString()}
            </div>
        `;
        resultDiv.style.display = 'block';
        
        // Reset form
        e.target.reset();
        
        // Reload invites
        loadAllInvites();
    } catch (error) {
        const resultDiv = document.getElementById('invite-result');
        resultDiv.innerHTML = `<div class="error-message">${error.message}</div>`;
        resultDiv.style.display = 'block';
    }
}

// Load all invites (admin)
async function loadAllInvites() {
    try {
        const data = await api('/invites/list');
        const tbody = document.getElementById('invites-tbody');
        tbody.innerHTML = '';
        
        data.invitations.forEach(invite => {
            const tr = document.createElement('tr');
            const status = invite.used ? 'used' : 
                          new Date(invite.expires_at) < new Date() ? 'expired' : 'active';
            
            tr.innerHTML = `
                <td>${invite.email}</td>
                <td><code>${invite.invite_code.substring(0, 16)}...</code></td>
                <td><span class="status-badge status-${status}">${status}</span></td>
                <td>${new Date(invite.expires_at).toLocaleDateString()}</td>
                <td>
                    ${!invite.used ? `<button class="btn btn-small btn-danger" onclick="deleteInvite(${invite.id})">Revoke</button>` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Failed to load invites:', error);
    }
}

// Load my invites
async function loadMyInvites() {
    try {
        const data = await api('/invites/mine');
        const tbody = document.getElementById('my-invites-tbody');
        tbody.innerHTML = '';
        
        data.invitations.forEach(invite => {
            const tr = document.createElement('tr');
            const status = invite.used ? 'used' : 
                          new Date(invite.expires_at) < new Date() ? 'expired' : 'active';
            
            tr.innerHTML = `
                <td>${invite.email}</td>
                <td><code>${invite.invite_code.substring(0, 16)}...</code></td>
                <td><span class="status-badge status-${status}">${status}</span></td>
                <td>${new Date(invite.expires_at).toLocaleDateString()}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Failed to load my invites:', error);
    }
}

// Delete invite
async function deleteInvite(inviteId) {
    if (!confirm('Are you sure you want to revoke this invitation?')) {
        return;
    }
    
    try {
        await api(`/invites/${inviteId}`, { method: 'DELETE' });
        loadAllInvites();
    } catch (error) {
        alert('Failed to revoke invitation: ' + error.message);
    }
}

// Load profile
function loadProfile() {
    const profileDiv = document.getElementById('profile-details');
    profileDiv.innerHTML = `
        <div class="profile-card">
            <h3>Account Information</h3>
            <div class="profile-item">
                <div class="profile-label">Username</div>
                <div class="profile-value">${state.user.username}</div>
            </div>
            <div class="profile-item">
                <div class="profile-label">Email</div>
                <div class="profile-value">${state.user.email}</div>
            </div>
            <div class="profile-item">
                <div class="profile-label">Role</div>
                <div class="profile-value">${state.user.role}</div>
            </div>
        </div>
        <div class="profile-card">
            <h3>Security</h3>
            <div class="profile-item">
                <div class="profile-label">Account Status</div>
                <div class="profile-value">✅ Active</div>
            </div>
            <div class="profile-item">
                <div class="profile-label">Authentication</div>
                <div class="profile-value">Session-based</div>
            </div>
        </div>
    `;
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
