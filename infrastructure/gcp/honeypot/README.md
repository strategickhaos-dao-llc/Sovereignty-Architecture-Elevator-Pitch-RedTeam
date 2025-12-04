# GCP Honeypot Infrastructure

This directory contains Terraform configuration for deploying a **deliberately non-sovereign honeypot** on Google Cloud Platform.

## ⚠️ Important Note

This honeypot is **log- and alert-only**, never trusted for production routing. It is intentionally exposed to capture and analyze attack patterns.

## Architecture

The infrastructure includes:

1. **Cloud Run SRA (honeypot-sra)** - Serverless container running the honeytrap application
2. **Regional HTTP Load Balancer** - Single public IP fronting the Cloud Run service
3. **GCS Bucket (honeytrap-attack-logs)** - Raw attack log storage with versioning
4. **Pub/Sub Topic (legion-attack-analysis)** - Event stream for Legion analysis
5. **Service Account** - Dedicated identity with minimal required permissions

## Resources

| Resource | Name | Description |
|----------|------|-------------|
| Cloud Run Service | honeypot-sra | Main honeypot application |
| Service Account | honeypot-sra-sa | Identity for the honeypot |
| GCS Bucket | honeytrap-attack-logs | Attack log storage |
| Pub/Sub Topic | legion-attack-analysis | Event stream for analysis |
| Regional LB | honeypot-sra-frontend | Public endpoint |

## Prerequisites

- Google Cloud SDK installed and configured
- Terraform >= 1.0.0
- GCP Project: `gen-lang-client-0012743775` (or update `var.project_id`)
- Required APIs enabled:
  - Cloud Run API
  - Cloud Storage API
  - Pub/Sub API
  - Compute Engine API (for load balancer)

## Usage

### 1. Initialize Terraform

```bash
cd infrastructure/gcp/honeypot
terraform init
```

### 2. Review the Plan

```bash
terraform plan
```

### 3. Apply the Configuration

```bash
terraform apply
```

### 4. Get Outputs

```bash
terraform output
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `project_id` | `gen-lang-client-0012743775` | GCP Project ID |
| `region` | `us-central1` | GCP Region |
| `honeypot_image` | `gcr.io/cloudrun/hello` | Container image (replace with Honeytrap) |
| `honeypot_container_port` | `8080` | Container port |
| `logs_bucket_name` | `honeytrap-attack-logs` | GCS bucket name |
| `pubsub_topic_name` | `legion-attack-analysis` | Pub/Sub topic name |

## Next Steps

Once this infrastructure is deployed:

1. **Replace the placeholder image** with your Honeytrap Flask application
2. **Configure the Flask app** to:
   - Log each request to `honeytrap-attack-logs` bucket (raw payload + metadata)
   - Publish summarized events to `legion-attack-analysis` topic
3. **Subscribe from Legion** to `legion-attack-analysis` from your Legion/NATS bridge

## Outputs

After applying, you'll get:

- `honeypot_service_url` - The Cloud Run service URL
- `honeypot_service_name` - The Cloud Run service name
- `honeytrap_logs_bucket` - GCS bucket name for logs
- `legion_pubsub_topic` - Pub/Sub topic name
- `legion_pubsub_topic_id` - Full Pub/Sub topic ID
- `honeypot_service_account_email` - Service account email

## Security Considerations

- The honeypot is **intentionally publicly accessible** (`allUsers` invoker role)
- All ingress traffic is allowed (`INGRESS_TRAFFIC_ALL`)
- This is by design for capturing attack traffic
- **Never** route production traffic through this honeypot
- Attack logs are preserved with versioning for forensic analysis

## Related Documentation

- [pattern.regional-serverless-endpoint](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Foundation Fabric](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric)
