# Outputs for GCP Honeypot Infrastructure

output "honeypot_service_url" {
  description = "URL of the Cloud Run honeypot service"
  value       = google_cloud_run_v2_service.honeypot_sra.uri
}

output "honeypot_service_name" {
  description = "Name of the Cloud Run honeypot service"
  value       = google_cloud_run_v2_service.honeypot_sra.name
}

output "honeytrap_logs_bucket" {
  description = "Name of the GCS bucket for honeytrap logs"
  value       = google_storage_bucket.honeytrap_logs.name
}

output "legion_pubsub_topic" {
  description = "Name of the Pub/Sub topic for Legion analysis"
  value       = google_pubsub_topic.legion_analysis.name
}

output "legion_pubsub_topic_id" {
  description = "Full Pub/Sub topic ID for Legion analysis"
  value       = google_pubsub_topic.legion_analysis.id
}

output "honeypot_service_account_email" {
  description = "Email of the honeypot service account"
  value       = google_service_account.honeypot_sra_sa.email
}
