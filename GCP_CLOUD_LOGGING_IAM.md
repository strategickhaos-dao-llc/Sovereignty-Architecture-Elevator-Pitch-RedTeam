# Google Cloud Logging IAM Roles Reference

> Updated: 2025-12-02 | Based on Google Cloud Logging IAM Documentation

This guide provides a comprehensive reference for Google Cloud Logging IAM roles, permissions, and best practices for the Strategickhaos Sovereignty Architecture.

## 🏛️ Overview

Google Cloud Logging IAM (Identity and Access Management) controls who has what type of access to Cloud Logging resources. Understanding these roles is critical for:

- **Security compliance** - Ensuring least-privilege access
- **Audit requirements** - Controlling who can view sensitive log data
- **Operational efficiency** - Enabling the right teams to manage logging configuration
- **Multi-tenant architectures** - Delegating appropriate access to different teams

---

## 📋 Cloud Logging Roles Matrix

| Role | ID | Main Purpose | Can Write Logs? | Can Read Normal Logs? | Can Read Private Logs? | Can Manage Sinks/Exclusions/Metrics/Views? | Full Admin? |
|------|----|--------------|-----------------|-----------------------|------------------------|---------------------------------------------|-------------|
| **Logs Writer** | `roles/logging.logWriter` | Only write log entries (the role most services need) | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Logs Bucket Writer** | `roles/logging.bucketWriter` | Write directly into a specific log bucket (rarely needed) | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Logs Viewer** | `roles/logging.viewer` | Read-only access to logs, sinks, metrics, etc. | ❌ No | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Private Logs Viewer** | `roles/logging.privateLogViewer` | Same as Logs Viewer + ability to read private (restricted-field) logs | ❌ No | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Logs View Accessor** | `roles/logging.viewAccessor` | Very narrow: only access logs inside a specific Log View | ❌ No | ✅ Yes (view only) | ❌ No | ❌ No | ❌ No |
| **Logs Configuration Writer** | `roles/logging.configWriter` | Manage sinks, exclusions, log metrics, views, etc. | ❌ No | ✅ Yes (list/get) | ❌ No | ✅ Yes | ❌ No |
| **Logging Admin** | `roles/logging.admin` | Full control over everything in Cloud Logging | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Log Field Accessor** | `roles/logging.fieldAccessor` | Only read restricted fields in logs (compliance use) | ❌ No | ❌ No | ❌ N/A | ❌ No | ❌ No |
| **Log Link Accessor** | `roles/logging.linkViewer` | Only see BigQuery/Cloud Storage links for buckets | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |

---

## 🔑 Role Details

### Logs Writer (`roles/logging.logWriter`)

**Purpose**: The role most commonly assigned to service accounts that need to emit logs.

**Key Permissions**:
- `logging.logEntries.create` - Write log entries
- `logging.logEntries.route` - Route log entries to destinations

**Use Cases**:
- GKE node service accounts
- Cloud Run service accounts
- Compute Engine instance service accounts
- Any workload that emits logs

```bash
# Grant Logs Writer to a service account
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:my-service@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/logging.logWriter"
```

---

### Logs Bucket Writer (`roles/logging.bucketWriter`)

**Purpose**: Write directly to a specific log bucket (rarely needed).

**Key Permissions**:
- `logging.buckets.write` - Write to log buckets

**Use Cases**:
- Cross-project log routing
- Custom log aggregation scenarios
- Log forwarding from external systems

---

### Logs Viewer (`roles/logging.viewer`)

**Purpose**: Read-only access to logs and logging configuration.

**Key Permissions**:
- `logging.logEntries.list` - List/read log entries
- `logging.sinks.get` / `logging.sinks.list` - View sinks
- `logging.logMetrics.get` / `logging.logMetrics.list` - View metrics
- Various `.get` and `.list` permissions

**Use Cases**:
- Developers debugging applications
- Analysts reviewing application behavior
- Support teams investigating issues

```bash
# Grant Logs Viewer to a user
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="user:developer@example.com" \
    --role="roles/logging.viewer"
```

---

### Private Logs Viewer (`roles/logging.privateLogViewer`)

**Purpose**: Same as Logs Viewer, plus access to private/restricted-field logs.

**Key Permissions**:
- All permissions from `roles/logging.viewer`
- `logging.privateLogEntries.list` - Read private log entries

**Use Cases**:
- Security teams needing access to sensitive audit logs
- Compliance teams reviewing restricted data
- Incident response teams during investigations

> ⚠️ **Important**: Even project Owners/Editors do NOT automatically have `logging.privateLogEntries.list`. You must explicitly grant `roles/logging.admin` or `roles/logging.privateLogViewer`.

---

### Logs View Accessor (`roles/logging.viewAccessor`)

**Purpose**: Very narrow scope - access only logs within a specific Log View.

**Key Permissions**:
- Access to logs within the assigned view only

**Use Cases**:
- Delegated access to specific teams
- Multi-tenant log segregation
- Vendor/contractor limited access

```bash
# Grant access to a specific log view
gcloud logging views add-iam-policy-binding VIEW_ID \
    --location=LOCATION \
    --bucket=BUCKET_ID \
    --member="user:contractor@example.com" \
    --role="roles/logging.viewAccessor"
```

---

### Logs Configuration Writer (`roles/logging.configWriter`)

**Purpose**: Manage logging configuration without being able to write log data.

**Key Permissions**:
- Create/update/delete sinks
- Create/update/delete exclusions
- Create/update/delete log metrics
- Create/update/delete views
- Most list/get permissions

**Use Cases**:
- Platform/SRE teams managing log routing
- DevOps engineers configuring log exports
- Teams setting up log-based metrics and alerts

```bash
# Grant Configuration Writer to a platform team
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="group:platform-team@example.com" \
    --role="roles/logging.configWriter"
```

---

### Logging Admin (`roles/logging.admin`)

**Purpose**: Full control over all Cloud Logging resources.

**Key Permissions**:
- All logging permissions
- `logging.privateLogEntries.list`
- Full CRUD on all logging resources

**Use Cases**:
- Logging administrators
- Emergency access scenarios
- Initial setup and configuration

> ⚠️ **Warning**: This role is very broad. Avoid granting it unless absolutely necessary. Consider combining `configWriter` + `viewer` or `privateLogViewer` instead.

---

### Log Field Accessor (`roles/logging.fieldAccessor`)

**Purpose**: Read restricted fields in logs (very narrow compliance use).

**Key Permissions**:
- `logging.fields.access` - Access to restricted log fields

**Use Cases**:
- Compliance auditors needing specific field access
- Legal discovery scenarios
- Specialized audit requirements

---

### Log Link Accessor (`roles/logging.linkViewer`)

**Purpose**: View BigQuery/Cloud Storage links for log buckets.

**Key Permissions**:
- View linked datasets
- View linked storage buckets

**Use Cases**:
- Teams that need to know where logs are exported
- Analysts working with exported log data

---

## 🎯 Best Practices & Common Scenarios

### Scenario 1: Service Account for Workloads (Write Logs Only)

**Requirement**: A service account needs to emit logs but not read them.

**Solution**: Grant `roles/logging.logWriter`

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:workload-sa@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/logging.logWriter"
```

---

### Scenario 2: Developer / Analyst (Read Normal Logs)

**Requirement**: Developers need to read logs for debugging.

**Solution**: Grant `roles/logging.viewer`

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="user:developer@example.com" \
    --role="roles/logging.viewer"
```

---

### Scenario 3: Security Team (Read Private Logs)

**Requirement**: Security team needs access to sensitive audit logs but should not manage configuration.

**Solution**: Grant `roles/logging.privateLogViewer`

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="group:security-team@example.com" \
    --role="roles/logging.privateLogViewer"
```

---

### Scenario 4: Platform/SRE Team (Manage Configuration + Read Logs)

**Requirement**: Platform team needs to manage sinks, exclusions, metrics, and views while also being able to read logs.

**Solution**: Grant `roles/logging.configWriter` + `roles/logging.viewer`

```bash
# Configuration management
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="group:platform-sre@example.com" \
    --role="roles/logging.configWriter"

# Log reading
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="group:platform-sre@example.com" \
    --role="roles/logging.viewer"
```

Or if they need private logs:

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="group:platform-sre@example.com" \
    --role="roles/logging.configWriter"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="group:platform-sre@example.com" \
    --role="roles/logging.privateLogViewer"
```

---

### Scenario 5: Full Logging Admin

**Requirement**: Complete control over Cloud Logging (use sparingly).

**Solution**: Grant `roles/logging.admin`

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="user:logging-admin@example.com" \
    --role="roles/logging.admin"
```

> ⚠️ **Warning**: Prefer combining specific roles rather than granting full admin access.

---

### Scenario 6: Delegated Access to Specific Log View

**Requirement**: External contractor needs access only to a specific subset of logs.

**Solution**: Create a Log View and grant `roles/logging.viewAccessor`

```bash
# Create a view (example: only application logs)
gcloud logging views create app-logs-view \
    --location=global \
    --bucket=_Default \
    --description="Application logs only" \
    --log-filter='resource.type="gae_app" OR resource.type="cloud_run_revision"'

# Grant access to the view
gcloud logging views add-iam-policy-binding app-logs-view \
    --location=global \
    --bucket=_Default \
    --member="user:contractor@external.com" \
    --role="roles/logging.viewAccessor"
```

---

## ⚠️ Important Notes (2025 Documentation Updates)

### Private Logs Access

`logging.privateLogEntries.list` is **only** available in:
- `roles/logging.admin`
- `roles/logging.privateLogViewer`

Even project `Owner` or `Editor` roles do **NOT** automatically include this permission.

### No Single "All Except Private" Role

There is no single role that provides "all logging access except private logs." To achieve configuration management + normal log reading:

```
roles/logging.configWriter + roles/logging.viewer
```

To include private logs:

```
roles/logging.configWriter + roles/logging.privateLogViewer
```

### Telco Automation Roles

Some Telco Automation roles bundle Logging Viewer permissions. They effectively act like `roles/logging.viewer` plus Telco-specific permissions.

---

## 🔗 Integration with Strategickhaos Architecture

### Kubernetes Service Account Mapping

For GKE workloads using Workload Identity:

```yaml
# Kubernetes ServiceAccount annotation
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  annotations:
    iam.gke.io/gcp-service-account: my-app@PROJECT_ID.iam.gserviceaccount.com
```

```bash
# Grant Logs Writer to the GCP service account
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:my-app@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/logging.logWriter"

# Bind Kubernetes SA to GCP SA
gcloud iam service-accounts add-iam-policy-binding my-app@PROJECT_ID.iam.gserviceaccount.com \
    --member="serviceAccount:PROJECT_ID.svc.id.goog[NAMESPACE/my-app]" \
    --role="roles/iam.workloadIdentityUser"
```

### Discord Bot Integration

For the Discord Ops Bot to read logs for the `/logs` command:

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:discord-ops-bot@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/logging.viewer"
```

### Event Gateway Log Shipping

For the Event Gateway to write logs to GCP:

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:event-gateway@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/logging.logWriter"
```

### Refinory AI Agent Access

For the Refinory AI agent to analyze logs:

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:refinory-agent@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/logging.viewer"
```

---

## 📊 Role Comparison Quick Reference

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CLOUD LOGGING IAM ROLES HIERARCHY                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  WRITE PERMISSIONS                                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  roles/logging.logWriter        → Write log entries (most common)    │  │
│  │  roles/logging.bucketWriter     → Write to specific buckets (rare)   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  READ PERMISSIONS                                                           │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  roles/logging.viewer           → Read normal logs                   │  │
│  │  roles/logging.privateLogViewer → Read normal + private logs         │  │
│  │  roles/logging.viewAccessor     → Read logs in specific view only    │  │
│  │  roles/logging.fieldAccessor    → Read restricted fields only        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  CONFIGURATION PERMISSIONS                                                  │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  roles/logging.configWriter     → Manage sinks, exclusions, metrics  │  │
│  │  roles/logging.linkViewer       → View export links only             │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  FULL ACCESS                                                                │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  roles/logging.admin            → EVERYTHING (use sparingly)         │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Additional Resources

- [Google Cloud Logging Documentation](https://cloud.google.com/logging/docs)
- [IAM Roles Reference](https://cloud.google.com/logging/docs/access-control)
- [Log Views and Scopes](https://cloud.google.com/logging/docs/logs-views)
- [Workload Identity for GKE](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity)

---

**Maintained by the Strategickhaos Infrastructure Team**

*Part of the Sovereignty Architecture documentation suite*
