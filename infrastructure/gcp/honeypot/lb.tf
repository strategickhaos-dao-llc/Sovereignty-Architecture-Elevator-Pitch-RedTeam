# Regional HTTP Load Balancer for Honeypot SRA
# Uses pattern.regional-serverless-endpoint approach
# Single public IP + hostname pointing to the SRA honeypot

module "honeypot_sra_regional_lb" {
  source = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/net-lb-app-ext-regional"

  project_id = var.project_id
  region     = var.region
  name       = "honeypot-sra-frontend"

  backends = {
    sra = {
      protocol = "HTTP"
      port     = 80
      cloud_run = {
        service = google_cloud_run_v2_service.honeypot_sra.name
        region  = google_cloud_run_v2_service.honeypot_sra.location
      }
    }
  }
}
