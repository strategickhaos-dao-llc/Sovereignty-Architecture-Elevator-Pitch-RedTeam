# GCP Honeypot Deployment Architecture - Main Configuration
# Implements pattern.regional-serverless-endpoint with Cloud Run and Load Balancer
#
# Architecture Overview:
# 1. Signal Routing Authority (SRA) - Cloud Run & Regional HTTP(S) Load Balancer
# 2. Honeytrap Logs Bucket - GCS for attack log storage
# 3. Legion Pub/Sub Topic - Real-time attack event streaming
# 4. Service Account with minimal required permissions

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "run.googleapis.com",
    "compute.googleapis.com",
    "pubsub.googleapis.com",
    "storage.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
  ])

  project                    = var.project_id
  service                    = each.value
  disable_on_destroy         = false
  disable_dependent_services = false
}

# =============================================================================
# Service Account - honeypot-sra-sa
# =============================================================================
resource "google_service_account" "honeypot_sra" {
  account_id   = "${var.honeypot_name}-sa"
  display_name = "Honeypot SRA Service Account"
  description  = "Service account for honeypot Cloud Run service with permissions to write logs and publish events"
  project      = var.project_id

  depends_on = [google_project_service.required_apis]
}

# =============================================================================
# GCS Bucket - honeytrap-attack-logs
# =============================================================================
resource "google_storage_bucket" "attack_logs" {
  name                        = "${var.logs_bucket_name}-${var.project_id}"
  location                    = var.region
  project                     = var.project_id
  uniform_bucket_level_access = true
  force_destroy               = false

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  labels = var.labels

  depends_on = [google_project_service.required_apis]
}

# Grant Storage Object Creator role to service account on the bucket
resource "google_storage_bucket_iam_member" "logs_writer" {
  bucket = google_storage_bucket.attack_logs.name
  role   = "roles/storage.objectCreator"
  member = "serviceAccount:${google_service_account.honeypot_sra.email}"
}

# =============================================================================
# Pub/Sub Topic - legion-attack-analysis
# =============================================================================
resource "google_pubsub_topic" "legion_analysis" {
  name    = var.pubsub_topic_name
  project = var.project_id

  labels = var.labels

  message_retention_duration = "604800s" # 7 days

  depends_on = [google_project_service.required_apis]
}

# Grant Pub/Sub Publisher role to service account on the topic
resource "google_pubsub_topic_iam_member" "publisher" {
  topic  = google_pubsub_topic.legion_analysis.name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${google_service_account.honeypot_sra.email}"
}

# =============================================================================
# Cloud Run Service - honeypot-sra
# =============================================================================
resource "google_cloud_run_v2_service" "honeypot_sra" {
  name     = var.honeypot_name
  location = var.region
  project  = var.project_id

  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.honeypot_sra.email

    containers {
      image = var.container_image

      ports {
        container_port = var.container_port
      }

      env {
        name  = "HONEYTRAP_LOG_BUCKET"
        value = google_storage_bucket.attack_logs.name
      }

      env {
        name  = "LEGION_PUBSUB_TOPIC"
        value = "projects/${var.project_id}/topics/${google_pubsub_topic.legion_analysis.name}"
      }

      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  labels = var.labels

  depends_on = [
    google_project_service.required_apis,
    google_storage_bucket.attack_logs,
    google_pubsub_topic.legion_analysis,
  ]
}

# Allow unauthenticated access to Cloud Run service (required for honeypot)
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  name     = google_cloud_run_v2_service.honeypot_sra.name
  location = google_cloud_run_v2_service.honeypot_sra.location
  project  = var.project_id
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# =============================================================================
# Regional External HTTP(S) Load Balancer - honeypot-sra-frontend
# =============================================================================

# Serverless NEG for Cloud Run
resource "google_compute_region_network_endpoint_group" "serverless_neg" {
  name                  = "${var.honeypot_name}-neg"
  region                = var.region
  project               = var.project_id
  network_endpoint_type = "SERVERLESS"

  cloud_run {
    service = google_cloud_run_v2_service.honeypot_sra.name
  }

  depends_on = [google_project_service.required_apis]
}

# Backend service for the load balancer
resource "google_compute_region_backend_service" "honeypot_backend" {
  name                  = "${var.honeypot_name}-backend"
  region                = var.region
  project               = var.project_id
  protocol              = "HTTP"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  timeout_sec           = 30

  backend {
    group = google_compute_region_network_endpoint_group.serverless_neg.id
  }
}

# URL map for routing
resource "google_compute_region_url_map" "honeypot_url_map" {
  name            = "${var.honeypot_name}-url-map"
  region          = var.region
  project         = var.project_id
  default_service = google_compute_region_backend_service.honeypot_backend.id
}

# HTTP proxy for the load balancer
resource "google_compute_region_target_http_proxy" "honeypot_proxy" {
  name    = "${var.honeypot_name}-http-proxy"
  region  = var.region
  project = var.project_id
  url_map = google_compute_region_url_map.honeypot_url_map.id
}

# Reserve a regional external IP address
resource "google_compute_address" "honeypot_ip" {
  name         = "${var.honeypot_name}-ip"
  region       = var.region
  project      = var.project_id
  address_type = "EXTERNAL"
  network_tier = "STANDARD"

  depends_on = [google_project_service.required_apis]
}

# Forwarding rule (frontend)
resource "google_compute_forwarding_rule" "honeypot_frontend" {
  name                  = "${var.honeypot_name}-frontend"
  region                = var.region
  project               = var.project_id
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  port_range            = "80"
  target                = google_compute_region_target_http_proxy.honeypot_proxy.id
  ip_address            = google_compute_address.honeypot_ip.id
  network_tier          = "STANDARD"

  labels = var.labels
}
