variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "sovereignty-eks"
}

variable "region" {
  description = "AWS region for EKS cluster"
  type        = string
  default     = "us-west-2"
}

variable "node_count" {
  description = "Number of worker nodes"
  type        = number
  default     = 3
}

# EKS cluster configuration
# This is a placeholder for production EKS deployment
resource "null_resource" "eks_cluster" {
  provisioner "local-exec" {
    command = <<-EOT
      echo "EKS cluster ${var.cluster_name} in ${var.region}"
      echo "Production: Would deploy managed Kubernetes with ${var.node_count} nodes"
    EOT
  }
}

output "cluster_endpoint" {
  value       = "https://eks-${var.cluster_name}.amazonaws.com"
  description = "EKS cluster endpoint"
}

output "cluster_name" {
  value       = var.cluster_name
  description = "EKS cluster name"
}
