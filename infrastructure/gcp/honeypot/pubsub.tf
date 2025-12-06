# Pub/Sub Topic for Legion Attack Analysis
# Events are published here from the honeypot for downstream analysis

resource "google_pubsub_topic" "legion_analysis" {
  name    = var.pubsub_topic_name
  project = var.project_id

  labels = {
    purpose     = "attack-analysis"
    environment = "security"
    managed_by  = "terraform"
  }
}
