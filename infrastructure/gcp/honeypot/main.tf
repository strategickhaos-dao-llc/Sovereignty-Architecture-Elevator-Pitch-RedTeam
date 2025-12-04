# Cloud Run Honeypot SRA Service
# Deliberately non-sovereign honeypot - log- and alert-only
# Never trusted for production routing

resource "google_cloud_run_v2_service" "honeypot_sra" {
  name     = "honeypot-sra"
  location = var.region
  project  = var.project_id

  template {
    service_account = google_service_account.honeypot_sra_sa.email

    containers {
      image = var.honeypot_image

      ports {
        container_port = var.honeypot_container_port
      }

      env {
        name  = "HONEYTRAP_LOG_BUCKET"
        value = var.logs_bucket_name
      }

      env {
        name  = "LEGION_PUBSUB_TOPIC"
        value = "projects/${var.project_id}/topics/${var.pubsub_topic_name}"
      }
    }
  }

  # Intentionally allow all traffic - this is a honeypot
  ingress = "INGRESS_TRAFFIC_ALL"

  labels = {
    purpose     = "honeypot"
    environment = "security"
    managed_by  = "terraform"
  }
}
