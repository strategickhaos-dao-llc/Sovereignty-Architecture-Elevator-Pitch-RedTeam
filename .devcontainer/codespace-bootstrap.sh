#!/bin/bash
echo "Waking the dormant dragons..."

# Connect to all clusters (authentication handled automatically in Codespaces)
gcloud container clusters get-credentials jarvis-swarm-personal-001 --zone=us-central1 --project=jarvis-swarm-personal
gcloud container clusters get-credentials red-team --zone=us-central1 --project=jarvis-swarm-personal
gcloud container clusters get-credentials autopilot-cluster-1 --zone=us-central1 --project=jarvis-swarm-personal

# Set up kubectl aliases
echo "alias k='kubectl'" >> ~/.bashrc
echo "alias kgp='kubectl get pods -A'" >> ~/.bashrc
echo "alias kgn='kubectl get nodes'" >> ~/.bashrc

# Clone the living organism (skip if already exists)
if [ ! -d ~/swarm-immune ]; then
  git clone https://github.com/strategickhaos/swarm-immune.git ~/swarm-immune
fi
cd ~/swarm-immune || exit 0

echo "Swarm Immune System DNA loaded."
echo "Run: cd ~/swarm-immune && python main.py monitor"
echo "Or: python main.py deploy gke --cluster jarvis-swarm-personal-001"
