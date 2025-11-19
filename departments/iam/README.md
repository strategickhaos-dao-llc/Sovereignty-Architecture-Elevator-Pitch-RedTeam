# Identity & Access Management (IAM) Department

**Department for handling names, logins, and user identity links across the Sovereignty Architecture ecosystem.**

## 🎯 Purpose

The IAM Department manages:
- **User Registration & Onboarding** - Streamlined joining process for new team members
- **Authentication & Login Management** - Secure credential handling and session management
- **Identity Linking** - Connect GitHub, GitLens, Discord, and other platform identities
- **Access Control** - Role-based permissions and authorization
- **User Profiles** - Centralized user information and preferences

## 🏗️ Architecture

```
departments/iam/
├── README.md                    # This file
├── config.yaml                  # IAM configuration
├── user-registry.ts             # User registration and management
├── auth-service.ts              # Authentication service
├── identity-linker.ts           # Cross-platform identity linking
├── onboarding-flow.ts           # New user onboarding automation
└── schemas/
    ├── user.schema.json         # User data schema
    └── credentials.schema.json  # Credentials schema
```

## 🚀 Features

### 1. User Registration
- Self-service registration interface
- Email verification
- Initial role assignment
- Discord/GitHub account linking

### 2. Authentication
- Multi-factor authentication (MFA) support
- OAuth2/OIDC integration
- Token-based sessions
- Password policy enforcement

### 3. Identity Linking
- **GitHub Integration** - Link GitHub accounts for PR/commit tracking
- **GitLens Integration** - Associate VS Code/GitLens users
- **Discord Integration** - Connect Discord users for notifications
- **Platform Unification** - Single identity across all services

### 4. Access Control
- Role-based access control (RBAC)
- Permission inheritance
- Team and group management
- Audit logging

### 5. Onboarding Flow
- Automated welcome messages
- Initial setup wizard
- Resource provisioning
- Team introduction

## 📋 User Workflow

### New User Journey
1. **Registration** - User provides basic info (name, email, GitHub username)
2. **Verification** - Email and account verification
3. **Linking** - Connect Discord, GitHub, GitLens accounts
4. **Onboarding** - Automated setup and introduction
5. **Access Granted** - Full system access with assigned role

### Login Flow
1. User authenticates (username/password or OAuth)
2. MFA challenge (if enabled)
3. Session established
4. User redirected to dashboard

## 🔧 Configuration

IAM settings in `config.yaml`:

```yaml
iam:
  enabled: true
  registration:
    enabled: true
    require_approval: false
    default_role: "member"
    verification:
      email: true
      manual_review: false
  
  authentication:
    methods:
      - "password"
      - "github_oauth"
      - "discord_oauth"
    mfa:
      enabled: true
      required_for_roles: ["admin", "maintainer"]
    session:
      duration_hours: 24
      refresh_enabled: true
  
  identity_linking:
    platforms:
      github:
        enabled: true
        auto_discover: true
      discord:
        enabled: true
        sync_roles: true
      gitlens:
        enabled: true
        track_activity: true
  
  roles:
    - name: "admin"
      permissions: ["*"]
    - name: "maintainer"
      permissions: ["deploy", "review", "merge"]
    - name: "contributor"
      permissions: ["commit", "pr", "review"]
    - name: "member"
      permissions: ["read", "comment"]
```

## 🔐 Security

- **Password Hashing** - bcrypt with configurable rounds
- **Token Security** - JWT with short expiration and refresh tokens
- **MFA Support** - TOTP and SMS-based authentication
- **Audit Logging** - All authentication events logged
- **Rate Limiting** - Protection against brute force attacks
- **Session Management** - Secure session handling with revocation

## 📊 Integration Points

### GitLens Integration
- Link VS Code users to central identity
- Track code review activity
- Correlate commits with user profiles

### Discord Integration
- Sync Discord roles with IAM roles
- Send onboarding messages via Discord bot
- Notification preferences

### GitHub Integration
- OAuth authentication
- PR author/reviewer mapping
- Commit attribution

## 🚦 Usage Examples

### Register New User (CLI)
```bash
./departments/iam/register-user.sh \
  --name "Jane Doe" \
  --email "jane@example.com" \
  --github "janedoe" \
  --discord "jane#1234"
```

### Link Accounts
```bash
./departments/iam/link-identity.sh \
  --user "jane@example.com" \
  --platform "gitlens" \
  --identifier "jane-vscode-id"
```

### Onboard User via Discord
```
/iam register
# Bot prompts for information
# Automated account creation and linking
```

## 📈 Monitoring

- **User Registration Rate** - Track new sign-ups
- **Authentication Failures** - Detect suspicious activity
- **Identity Linking Success** - Monitor platform connections
- **Active Sessions** - Current logged-in users
- **MFA Adoption** - Security metric

## 🛠️ API Reference

### User Registration
```typescript
POST /api/iam/register
{
  "name": "John Doe",
  "email": "john@example.com",
  "github_username": "johndoe",
  "discord_id": "123456789"
}
```

### Authentication
```typescript
POST /api/iam/login
{
  "email": "john@example.com",
  "password": "secure_password",
  "mfa_token": "123456"
}
```

### Link Identity
```typescript
POST /api/iam/link
{
  "user_id": "user-123",
  "platform": "gitlens",
  "platform_id": "vscode-user-id"
}
```

## 📚 Resources

- [OAuth 2.0 Specification](https://oauth.net/2/)
- [OIDC Documentation](https://openid.net/connect/)
- [RBAC Best Practices](https://www.owasp.org/index.php/Access_Control)
- [MFA Implementation Guide](https://www.nist.gov/itl/applied-cybersecurity/tig/back-basics-multi-factor-authentication)

---

**Maintained by the Strategickhaos IAM Team**
*Securing sovereign digital identity*
