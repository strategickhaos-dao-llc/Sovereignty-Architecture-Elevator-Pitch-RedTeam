# GCS Bucket for Raw Honeypot Logs
# Stores attack logs with versioning enabled for forensic analysis

resource "google_storage_bucket" "honeytrap_logs" {
  name                        = var.logs_bucket_name
  project                     = var.project_id
  location                    = var.region
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  # Prevent accidental deletion of attack log data
  lifecycle {
    prevent_destroy = true
  }

  labels = {
    purpose     = "honeytrap-logs"
    environment = "security"
    managed_by  = "terraform"
  }
}
