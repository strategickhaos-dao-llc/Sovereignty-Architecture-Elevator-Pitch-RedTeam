# GCP Honeypot Deployment Architecture

This Terraform module deploys a **deliberately non-sovereign honeypot** infrastructure on Google Cloud Platform, designed to attract and analyze attack patterns while maintaining a clear security boundary between the honeypot and sovereign infrastructure.

## Architecture Overview

**Project:** `gen-lang-client-0012743775` (configurable)  
**Region:** `us-central1` (configurable)

### Components

#### 1. Signal Routing Authority (SRA) - Cloud Run & Load Balancer

Uses the `pattern.regional-serverless-endpoint` to deploy a Cloud Run service and expose it publicly via a regional external HTTP(S) Load Balancer.

- **Cloud Run Service (`honeypot-sra`):**
  - Name: `honeypot-sra`
  - Location: `us-central1`
  - Image: `gcr.io/cloudrun/hello` (placeholder, replace with Honeytrap image)
  - Container Port: `8080`
  - Ingress: `INGRESS_TRAFFIC_ALL` (allows traffic from anywhere)
  - Service Account: `honeypot-sra-sa`

- **Regional External HTTP(S) Load Balancer:**
  - Name: `honeypot-sra-frontend`
  - Purpose: Provides a single public IP and hostname, routing traffic to Cloud Run

#### 2. Honeytrap Logs Bucket

- **Google Cloud Storage Bucket (`honeytrap-attack-logs`):**
  - Location: `US-CENTRAL1`
  - Uniform bucket level access: `enabled`
  - Versioning: `enabled`
  - Lifecycle policies for cost optimization

#### 3. Legion Pub/Sub Topic

- **Google Cloud Pub/Sub Topic (`legion-attack-analysis`):**
  - Purpose: Receive summarized attack events for real-time Legion processing
  - Message retention: 7 days

#### 4. Service Account & IAM

- **Service Account (`honeypot-sra-sa`):**
  - `roles/storage.objectCreator` on attack logs bucket
  - `roles/pubsub.publisher` on Legion analysis topic

## Data Flow

```
                                    ┌─────────────────────────────────────────┐
                                    │           GCP Honeypot Zone             │
                                    │                                         │
┌──────────────┐                    │  ┌────────────────────────────────────┐ │
│   External   │                    │  │    Regional HTTP(S) LB             │ │
│   Traffic    │ ─────────────────────▶│    (honeypot-sra-frontend)         │ │
│   (Attacks)  │                    │  │    Public IP: x.x.x.x              │ │
└──────────────┘                    │  └──────────────────┬─────────────────┘ │
                                    │                     │                   │
                                    │                     ▼                   │
                                    │  ┌────────────────────────────────────┐ │
                                    │  │       Cloud Run Service            │ │
                                    │  │       (honeypot-sra)               │ │
                                    │  │                                    │ │
                                    │  │  ┌──────────────────────────────┐  │ │
                                    │  │  │    Honeytrap Flask App       │  │ │
                                    │  │  │    (your container image)    │  │ │
                                    │  │  └──────────────────────────────┘  │ │
                                    │  └───────────┬──────────┬─────────────┘ │
                                    │              │          │               │
                                    │              ▼          ▼               │
                                    │  ┌───────────────┐ ┌───────────────────┐│
                                    │  │  GCS Bucket   │ │  Pub/Sub Topic    ││
                                    │  │  (attack-logs)│ │  (legion-analysis)││
                                    │  │               │ │                   ││
                                    │  │  Raw attack   │ │  Real-time event  ││
                                    │  │  data storage │ │  streaming        ││
                                    │  └───────────────┘ └─────────┬─────────┘│
                                    │                              │          │
                                    └──────────────────────────────┼──────────┘
                                                                   │
                                                                   ▼
                                                    ┌──────────────────────────┐
                                                    │   Sovereign NATS Mesh    │
                                                    │   (Legion/NATS Bridge)   │
                                                    │                          │
                                                    │   External subscription  │
                                                    │   to Pub/Sub topic       │
                                                    └──────────────────────────┘
```

## Prerequisites

1. **GCP Project** with billing enabled
2. **Terraform** >= 1.0.0
3. **gcloud CLI** authenticated with appropriate permissions
4. **Required IAM Roles** for the deploying user:
   - `roles/run.admin`
   - `roles/compute.admin`
   - `roles/storage.admin`
   - `roles/pubsub.admin`
   - `roles/iam.serviceAccountAdmin`
   - `roles/serviceusage.serviceUsageAdmin`

## Usage

### Quick Start

```bash
# Initialize Terraform
cd infrastructure/gcp/honeypot
terraform init

# Review the plan
terraform plan -var="project_id=YOUR_PROJECT_ID"

# Apply the configuration
terraform apply -var="project_id=YOUR_PROJECT_ID"
```

### Using tfvars file

```bash
# Copy the example file
cp terraform.tfvars.example terraform.tfvars

# Edit with your values
vim terraform.tfvars

# Apply
terraform init
terraform apply
```

### Custom Configuration

```hcl
# terraform.tfvars
project_id        = "your-gcp-project-id"
region            = "us-central1"
honeypot_name     = "honeypot-sra"
container_image   = "gcr.io/your-project/honeytrap:latest"
container_port    = 8080
logs_bucket_name  = "honeytrap-attack-logs"
pubsub_topic_name = "legion-attack-analysis"

labels = {
  purpose     = "honeypot"
  environment = "production"
  managed_by  = "terraform"
  project     = "sovereignty-architecture"
}
```

## Outputs

After deployment, Terraform will output:

| Output | Description |
|--------|-------------|
| `cloud_run_service_url` | Direct URL to the Cloud Run service |
| `load_balancer_ip` | External IP address of the load balancer |
| `load_balancer_url` | HTTP URL of the load balancer frontend |
| `attack_logs_bucket` | Name of the GCS bucket for attack logs |
| `pubsub_topic` | Full path of the Pub/Sub topic |
| `service_account_email` | Email of the honeypot service account |
| `data_flow_summary` | Complete summary of the data flow architecture |

## Environment Variables

The Cloud Run service receives these environment variables:

| Variable | Description |
|----------|-------------|
| `HONEYTRAP_LOG_BUCKET` | GCS bucket name for storing raw attack logs |
| `LEGION_PUBSUB_TOPIC` | Full Pub/Sub topic path for event streaming |
| `GCP_PROJECT_ID` | GCP project ID for API calls |

## Connecting Legion/NATS Bridge

To subscribe to the Pub/Sub topic from your sovereign infrastructure:

```bash
# Create a subscription for the Legion bridge
gcloud pubsub subscriptions create legion-bridge-subscription \
  --topic=legion-attack-analysis \
  --ack-deadline=60 \
  --message-retention-duration=7d

# Pull messages for processing
gcloud pubsub subscriptions pull legion-bridge-subscription \
  --auto-ack \
  --limit=100
```

## Security Considerations

⚠️ **This is a deliberately exposed honeypot infrastructure.**

- **Public Access**: The Cloud Run service allows `allUsers` to invoke it
- **No Authentication**: Designed to attract and log attacks
- **Isolation**: Keep this infrastructure completely separate from production
- **Monitoring**: Enable Cloud Logging and Monitoring for visibility
- **Budget Alerts**: Set up billing alerts to prevent cost overruns

## Cost Optimization

The infrastructure includes several cost optimization features:

1. **Cloud Run Scaling**: Scales to 0 when idle
2. **GCS Lifecycle Policies**: 
   - Move to Nearline after 90 days
   - Move to Coldline after 365 days
3. **Pub/Sub Retention**: 7-day message retention

## Cleanup

To destroy all resources:

```bash
terraform destroy -var="project_id=YOUR_PROJECT_ID"
```

## Related Documentation

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Regional External HTTP(S) Load Balancer](https://cloud.google.com/load-balancing/docs/https)
- [Cloud Storage](https://cloud.google.com/storage/docs)
- [Pub/Sub](https://cloud.google.com/pubsub/docs)
- [Sovereignty Architecture](../../README.md)

## License

MIT License - See [LICENSE](../../../LICENSE) for details.
