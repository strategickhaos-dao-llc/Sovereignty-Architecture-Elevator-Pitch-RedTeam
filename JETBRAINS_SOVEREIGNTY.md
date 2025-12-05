# JetBrains Sovereign Development Environment

**A comprehensive guide for configuring JetBrains IDEs (WebStorm, Rider, AI Pro) for the Strategickhaos sovereign development ecosystem.**

## 🏛️ Overview

This document provides the complete setup and configuration for a sovereign JetBrains development environment that integrates with the Strategickhaos architecture. The stack includes:

| Component | JetBrains Tool | Purpose |
|-----------|---------------|---------|
| SwarmGate / Solidity / CI | WebStorm + AI Pro | Smart contract dev, scripts, workflows |
| Sovereignty-Architecture / DevOps Plane | Rider + AI Pro | .NET, infra automation, Kubernetes |
| AI orchestration, agent routing | AI Pro | Prompt engineering, LLM integration |
| Azure DevOps, Kubernetes, cloud infra | Azd plugin | Provision + deploy sovereign workloads |

## 🔐 Security First Setup (CRITICAL)

### 1. Enable Two-Factor Authentication (2FA)

**This is mandatory for sovereign infrastructure operations.**

1. Go to: **JetBrains Account → Security → Turn on 2FA**
2. Use an authenticator app (Authy, Google Authenticator, or 1Password)
3. Store backup codes securely in your Vault

This protects:
- Your repositories
- AI agent configurations
- IDE plugins and settings
- Azure DevOps connections

### 2. Configure AI Exclusions

**Prevent sensitive data from being sent to AI services.**

Navigate to: **Settings → Tools → JetBrains AI → Exclusions**

Add these patterns to protect your secrets:

```
**/secrets/**
**/.env
**/.env.*
**/*.pem
**/*.key
**/*.kube
**/vault/**
**/.idea/keymaps/**
**/config/private/**
**/*.pfx
**/*.p12
**/kubeconfig*
**/.aws/**
**/.azure/**
**/.gcp/**
**/credentials*
**/*secret*
**/*token*
```

### 3. Review Payment & Subscriptions

For full sovereignty with zero financial drift:
- Review auto-renewal settings at **Account → Payment Methods**
- Set calendar reminders for subscription expiry dates
- Consider removing saved payment methods if not actively needed

## 🚀 IDE Configuration

### WebStorm Setup

WebStorm is optimized for:
- TypeScript / JavaScript / Node.js development
- Solidity smart contracts (with Hardhat plugin)
- CI/CD workflow scripts
- Shell scripting

#### Sign in to AI Assistant
1. **Settings → Tools → JetBrains AI → Sign in**
2. Verify AI exclusions are configured (see Security section above)

#### Recommended Plugins
- **Hardhat** - Solidity development support
- **Kubernetes** - K8s manifest editing and deployment
- **Docker** - Container management
- **GitToolBox** - Enhanced Git integration
- **.env files support** - Environment variable management
- **YAML/Ansible Support** - Infrastructure-as-code editing

### Rider Setup

Rider is optimized for:
- .NET / C# development
- Infrastructure automation
- Kubernetes operators
- Backend services

#### Sign in to AI Assistant
1. **Settings → Tools → JetBrains AI → Sign in**
2. Verify AI exclusions are configured (see Security section above)

#### Recommended Plugins
- **Azure Toolkit for Rider** - Azure resource management
- **Kubernetes** - K8s manifest editing and deployment
- **Docker** - Container management
- **Terraform and HCL** - Infrastructure-as-code support

## 🤖 AI Pro Features

Once AI Pro is enabled and signed in, you unlock:

| Feature | Description |
|---------|-------------|
| AI Code Completion | Context-aware suggestions across entire codebase |
| AI Test Generation | Automatic unit test creation for methods |
| Inline Refactors | AI-powered code restructuring suggestions |
| Multi-file PR Summaries | Automated pull request descriptions |
| AI-assisted Security Scans | Vulnerability detection in code |
| Infrastructure Change Plans | DevOps automation suggestions |
| "Explain this code" | Context-aware code documentation |
| "Fix this" | One-click bug fixes with AI suggestions |

## 📦 Importable Settings

### Code Style Configuration

Create or import these settings for consistent code formatting:

#### JavaScript/TypeScript (WebStorm)
```xml
<!-- .idea/codeStyles/Project.xml -->
<component name="ProjectCodeStyleConfiguration">
  <code_scheme name="Strategickhaos" version="173">
    <TypeScriptCodeStyleSettings version="0">
      <option name="FORCE_SEMICOLON_STYLE" value="true" />
      <option name="FORCE_QUOTE_STYLE" value="true" />
      <option name="USE_DOUBLE_QUOTES" value="false" />
      <option name="SPACE_BEFORE_FUNCTION_LEFT_PARENTH" value="false" />
      <option name="USE_PUBLIC_MODIFIER" value="true" />
    </TypeScriptCodeStyleSettings>
  </code_scheme>
</component>
```

#### C# (Rider)
```xml
<!-- .idea/codeStyles/Project.xml -->
<component name="ProjectCodeStyleConfiguration">
  <code_scheme name="Strategickhaos" version="173">
    <csharpCodeStyleSettings>
      <option name="BRACES_FOR_IFELSE" value="REQUIRED" />
      <option name="BRACES_FOR_FOR" value="REQUIRED" />
      <option name="BRACES_FOR_FOREACH" value="REQUIRED" />
      <option name="BRACES_FOR_WHILE" value="REQUIRED" />
      <option name="INDENT_SIZE" value="4" />
      <option name="BLANK_LINES_AROUND_NAMESPACE" value="1" />
    </csharpCodeStyleSettings>
  </code_scheme>
</component>
```

### Run Configurations

#### WebStorm - Node.js Development Server
```xml
<!-- .idea/runConfigurations/Dev_Server.xml -->
<component name="ProjectRunConfigurationManager">
  <configuration name="Dev Server" type="NodeJSConfigurationType">
    <node-options>--experimental-specifier-resolution=node</node-options>
    <working-dir>$PROJECT_DIR$</working-dir>
    <method v="2">
      <option name="NpmBeforeRunTask" enabled="true">
        <package-json value="$PROJECT_DIR$/package.json" />
        <command value="install" />
      </option>
    </method>
  </configuration>
</component>
```

#### Rider - .NET Application
```xml
<!-- .idea/runConfigurations/DotNet_Run.xml -->
<component name="ProjectRunConfigurationManager">
  <configuration name=".NET Run" type="DotNetProject">
    <option name="EXE_PATH" value="" />
    <option name="PROGRAM_PARAMETERS" value="" />
    <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$" />
    <option name="PASS_PARENT_ENVS" value="1" />
    <envs>
      <env name="ASPNETCORE_ENVIRONMENT" value="Development" />
    </envs>
  </configuration>
</component>
```

### Live Templates

#### TypeScript Async Function
```xml
<template name="asyncfn" value="async function $NAME$($PARAMS$): Promise&lt;$RETURN$&gt; {&#10;    $END$&#10;}" description="Async function with Promise return type" toReformat="true" toShortenFQNames="true">
  <variable name="NAME" expression="" defaultValue="" alwaysStopAt="true" />
  <variable name="PARAMS" expression="" defaultValue="" alwaysStopAt="true" />
  <variable name="RETURN" expression="" defaultValue="void" alwaysStopAt="true" />
  <context>
    <option name="TypeScript" value="true" />
  </context>
</template>
```

#### Kubernetes ConfigMap
```xml
<template name="k8scm" value="apiVersion: v1&#10;kind: ConfigMap&#10;metadata:&#10;  name: $NAME$&#10;  namespace: $NAMESPACE$&#10;data:&#10;  $KEY$: $VALUE$&#10;" description="Kubernetes ConfigMap" toReformat="true" toShortenFQNames="true">
  <variable name="NAME" expression="" defaultValue="my-config" alwaysStopAt="true" />
  <variable name="NAMESPACE" expression="" defaultValue="default" alwaysStopAt="true" />
  <variable name="KEY" expression="" defaultValue="key" alwaysStopAt="true" />
  <variable name="VALUE" expression="" defaultValue="value" alwaysStopAt="true" />
  <context>
    <option name="YAML" value="true" />
  </context>
</template>
```

## 🔧 Inspection Profiles

### Security-Focused Inspections

Enable these inspections for sovereignty-critical code:

```xml
<!-- .idea/inspectionProfiles/Sovereignty.xml -->
<component name="InspectionProjectProfileManager">
  <profile version="1.0">
    <option name="myName" value="Sovereignty" />
    <inspection_tool class="HardcodedPassword" enabled="true" level="ERROR" />
    <inspection_tool class="SqlInjection" enabled="true" level="ERROR" />
    <inspection_tool class="InsecureApiCall" enabled="true" level="WARNING" />
    <inspection_tool class="WeakCrypto" enabled="true" level="WARNING" />
    <inspection_tool class="PathTraversal" enabled="true" level="ERROR" />
    <inspection_tool class="CommandInjection" enabled="true" level="ERROR" />
    <inspection_tool class="XSSPossibility" enabled="true" level="WARNING" />
    <inspection_tool class="InsecureDeserialization" enabled="true" level="ERROR" />
  </profile>
</component>
```

## 🌐 Azure Dev (Azd) Plugin Configuration

The Azd plugin integrates with Azure DevOps for:
- Provisioning cloud resources
- Deploying sovereign workloads
- Managing infrastructure lifecycle

### Setup
1. Install the **Azure Toolkit** plugin
2. Authenticate with `az login` in terminal
3. Configure default subscription and resource group

### Key Commands
```bash
# Initialize Azure resources
azd init

# Provision infrastructure
azd provision

# Deploy application
azd deploy

# Full lifecycle (provision + deploy)
azd up
```

## 📊 Strategickhaos Ecosystem Mapping

| Repository / Component | Primary IDE | Secondary IDE | Key Features |
|----------------------|-------------|---------------|--------------|
| SwarmGate | WebStorm | - | TypeScript, Solidity, CI/CD |
| Sovereignty-Architecture | Rider | WebStorm | .NET, YAML, Kubernetes |
| quantum-symbolic-emulator | WebStorm | Rider | TypeScript, Node.js |
| valoryield-engine | Rider | - | C#, .NET, Azure |
| Infrastructure configs | WebStorm | - | YAML, Docker, K8s |

## 🛡️ Security Checklist

Before starting development, verify:

- [ ] 2FA is enabled on JetBrains account
- [ ] AI exclusions are configured for all sensitive patterns
- [ ] No payment methods saved (or auto-renewal disabled)
- [ ] Plugins are from verified sources only
- [ ] IDE is updated to latest stable version
- [ ] Vault integration is configured (if applicable)
- [ ] `.idea` folder is added to `.gitignore` for sensitive projects

## 📚 Resources

- [JetBrains Security Guide](https://www.jetbrains.com/help/idea/security.html)
- [JetBrains AI Documentation](https://www.jetbrains.com/help/idea/ai-assistant.html)
- [WebStorm Documentation](https://www.jetbrains.com/help/webstorm/)
- [Rider Documentation](https://www.jetbrains.com/help/rider/)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/)

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Sovereign development demands sovereign tools."*
