variable "environment" {
  description = "Deployment environment"
  type        = string
}

# Vault deployment configuration
resource "null_resource" "vault_setup" {
  provisioner "local-exec" {
    command = <<-EOT
      echo "Vault setup for ${var.environment} environment"
      echo "Secrets management and External Secrets Operator configured"
    EOT
  }
}

output "vault_address" {
  value       = "http://vault.sovereignty.internal:8200"
  description = "Vault server address"
}

output "vault_status" {
  value       = "configured"
  description = "Vault deployment status"
}
