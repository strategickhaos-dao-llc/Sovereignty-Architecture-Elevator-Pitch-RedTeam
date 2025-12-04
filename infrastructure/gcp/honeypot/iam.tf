# IAM Configuration for Honeypot Service Account
# Service account for the Cloud Run honeypot with required permissions

resource "google_service_account" "honeypot_sra_sa" {
  account_id   = "honeypot-sra-sa"
  display_name = "Honeypot SRA Service Account"
  project      = var.project_id
}

# Grant storage.objectCreator role for writing logs to GCS bucket
resource "google_project_iam_member" "honeypot_sra_sa_storage" {
  project = var.project_id
  role    = "roles/storage.objectCreator"
  member  = "serviceAccount:${google_service_account.honeypot_sra_sa.email}"
}

# Grant Pub/Sub publisher role for publishing to Legion analysis topic
resource "google_pubsub_topic_iam_member" "honeypot_publisher" {
  topic  = google_pubsub_topic.legion_analysis.name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${google_service_account.honeypot_sra_sa.email}"
}

# Public access for Cloud Run honeypot (intentionally exposed)
resource "google_cloud_run_v2_service_iam_member" "honeypot_invoker" {
  name     = google_cloud_run_v2_service.honeypot_sra.name
  location = google_cloud_run_v2_service.honeypot_sra.location
  project  = var.project_id
  role     = "roles/run.invoker"
  member   = "allUsers"
}
