# GCP Honeypot Infrastructure - Outputs
# Provides information about deployed resources

output "cloud_run_service_url" {
  description = "URL of the deployed Cloud Run service"
  value       = google_cloud_run_v2_service.honeypot_sra.uri
}

output "cloud_run_service_name" {
  description = "Name of the Cloud Run service"
  value       = google_cloud_run_v2_service.honeypot_sra.name
}

output "load_balancer_ip" {
  description = "External IP address of the load balancer frontend"
  value       = google_compute_address.honeypot_ip.address
}

output "load_balancer_url" {
  description = "HTTP URL of the load balancer frontend"
  value       = "http://${google_compute_address.honeypot_ip.address}"
}

output "attack_logs_bucket" {
  description = "Name of the GCS bucket for attack logs"
  value       = google_storage_bucket.attack_logs.name
}

output "attack_logs_bucket_url" {
  description = "URL of the GCS bucket for attack logs"
  value       = google_storage_bucket.attack_logs.url
}

output "pubsub_topic" {
  description = "Full path of the Pub/Sub topic for Legion analysis"
  value       = google_pubsub_topic.legion_analysis.id
}

output "pubsub_topic_name" {
  description = "Name of the Pub/Sub topic for Legion analysis"
  value       = google_pubsub_topic.legion_analysis.name
}

output "service_account_email" {
  description = "Email of the honeypot service account"
  value       = google_service_account.honeypot_sra.email
}

output "service_account_id" {
  description = "Unique ID of the honeypot service account"
  value       = google_service_account.honeypot_sra.unique_id
}

output "data_flow_summary" {
  description = "Summary of the honeypot data flow architecture"
  value = {
    ingress         = "External traffic → Load Balancer (${google_compute_address.honeypot_ip.address}:80)"
    processing      = "Load Balancer → Cloud Run (${google_cloud_run_v2_service.honeypot_sra.name})"
    log_storage     = "Cloud Run → GCS Bucket (${google_storage_bucket.attack_logs.name})"
    event_streaming = "Cloud Run → Pub/Sub Topic (${google_pubsub_topic.legion_analysis.name})"
    analysis        = "Pub/Sub → Legion/NATS Bridge (external subscription)"
  }
}
