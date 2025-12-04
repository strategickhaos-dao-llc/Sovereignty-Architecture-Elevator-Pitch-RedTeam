# GCP Honeypot Infrastructure - Variables
# This module deploys a deliberately non-sovereign honeypot using GCP services

variable "project_id" {
  description = "GCP Project ID for honeypot deployment"
  type        = string
  default     = "gen-lang-client-0012743775"
}

variable "region" {
  description = "GCP region for resource deployment"
  type        = string
  default     = "us-central1"
}

variable "honeypot_name" {
  description = "Base name for honeypot resources"
  type        = string
  default     = "honeypot-sra"
}

variable "container_image" {
  description = "Container image for Cloud Run service"
  type        = string
  default     = "gcr.io/cloudrun/hello"
}

variable "container_port" {
  description = "Port the container listens on"
  type        = number
  default     = 8080
}

variable "logs_bucket_name" {
  description = "Name of the GCS bucket for attack logs"
  type        = string
  default     = "honeytrap-attack-logs"
}

variable "pubsub_topic_name" {
  description = "Name of the Pub/Sub topic for Legion analysis"
  type        = string
  default     = "legion-attack-analysis"
}

variable "labels" {
  description = "Labels to apply to all resources"
  type        = map(string)
  default = {
    purpose     = "honeypot"
    environment = "production"
    managed_by  = "terraform"
    project     = "sovereignty-architecture"
  }
}
