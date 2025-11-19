variable "cluster_name" {
  description = "Name of the K3s cluster"
  type        = string
}

variable "node_count" {
  description = "Number of nodes in the cluster"
  type        = number
  default     = 1
}

# K3s cluster configuration
# In production, this would create actual infrastructure
# For chaos-god-local, it uses existing local setup
resource "null_resource" "k3s_cluster" {
  provisioner "local-exec" {
    command = <<-EOT
      echo "K3s cluster ${var.cluster_name} with ${var.node_count} nodes initialized"
      echo "In production mode, this would provision actual K3s nodes"
    EOT
  }
}

output "cluster_endpoint" {
  value       = "https://kubernetes.default.svc"
  description = "Cluster API endpoint"
}

output "cluster_name" {
  value       = var.cluster_name
  description = "Cluster name"
}
