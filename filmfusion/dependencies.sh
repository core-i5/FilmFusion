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

# Install Redis
sudo apt-get install -y redis-server

# Enable and start the Redis service
sudo systemctl enable redis-server.service
sudo systemctl start redis-server.service

# Verify Redis is running
if systemctl status redis-server | grep -q "active (running)"; then
    echo "Redis is successfully installed and running!"
else
    echo "Redis installation failed or the service is not running."
fi
