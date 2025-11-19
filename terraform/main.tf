terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
    vault = {
      source  = "hashicorp/vault"
      version = "~> 3.20"
    }
  }

  backend "local" {
    path = "terraform.tfstate"
  }
}

# Provider configurations
provider "kubernetes" {
  config_path = var.kubeconfig_path
}

provider "helm" {
  kubernetes {
    config_path = var.kubeconfig_path
  }
}

provider "vault" {
  address = var.vault_address
  token   = var.vault_token
}

# Variables
variable "kubeconfig_path" {
  description = "Path to kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "vault_address" {
  description = "Vault server address"
  type        = string
  default     = "http://localhost:8200"
}

variable "vault_token" {
  description = "Vault authentication token"
  type        = string
  sensitive   = true
  default     = ""
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "chaos-god-local"
}

# Module calls based on environment
module "k3s_cluster" {
  source = "./modules/k3s-cluster"
  
  cluster_name = "sovereignty-${var.environment}"
  node_count   = var.environment == "prod" ? 5 : 1
}

module "vault" {
  source = "./modules/vault"
  
  environment = var.environment
  depends_on  = [module.k3s_cluster]
}

module "tailscale" {
  source = "./modules/tailscale"
  
  environment = var.environment
  depends_on  = [module.k3s_cluster]
}

# Outputs
output "cluster_endpoint" {
  value       = module.k3s_cluster.cluster_endpoint
  description = "Kubernetes cluster endpoint"
}

output "vault_address" {
  value       = module.vault.vault_address
  description = "Vault server address"
}

output "tailscale_status" {
  value       = module.tailscale.status
  description = "Tailscale network status"
}
