#!/bin/bash

# Update and install necessary dependencies
sudo apt-get update
sudo apt-get install -y apt-transport-https openjdk-11-jdk wget

# Import the Elasticsearch PGP key
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

# Add the Elasticsearch repository to your system
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-8.x.list

# Update the package list and install Elasticsearch
sudo apt-get update
sudo apt-get install -y elasticsearch

# Enable and start the Elasticsearch service
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service

# Verify Elasticsearch is running
if systemctl status elasticsearch | grep -q "active (running)"; then
    echo "Elasticsearch is successfully installed and running!"
else
    echo "Elasticsearch installation failed or the service is not running."
fi
