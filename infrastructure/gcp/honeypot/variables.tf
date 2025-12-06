# Variables for GCP Honeypot Infrastructure
# Honeypot is log- and alert-only, never trusted for production routing

variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "gen-lang-client-0012743775"
}

variable "region" {
  description = "GCP Region for resources"
  type        = string
  default     = "us-central1"
}

variable "honeypot_image" {
  description = "Container image for honeypot SRA (default: placeholder, replace with Honeytrap image)"
  type        = string
  default     = "gcr.io/cloudrun/hello"
}

variable "honeypot_container_port" {
  description = "Port for the honeypot container"
  type        = number
  default     = 8080
}

variable "logs_bucket_name" {
  description = "Name of the GCS bucket for honeytrap attack logs"
  type        = string
  default     = "honeytrap-attack-logs"
}

variable "pubsub_topic_name" {
  description = "Name of the Pub/Sub topic for Legion analysis"
  type        = string
  default     = "legion-attack-analysis"
}
