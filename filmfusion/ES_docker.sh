#!/bin/bash

# Set the Elasticsearch version you want to use
ELASTICSEARCH_VERSION="8.10.2"

# Pull the Elasticsearch Docker image
docker pull docker.elastic.co/elasticsearch/elasticsearch:$ELASTICSEARCH_VERSION

# Run the Elasticsearch container
docker run -d --name elasticsearch \
  -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
  docker.elastic.co/elasticsearch/elasticsearch:$ELASTICSEARCH_VERSION

# Wait a few seconds for Elasticsearch to start
echo "Waiting for Elasticsearch to start..."
sleep 15

# Check if Elasticsearch is running
if curl -s http://localhost:9200 | grep -q "You Know, for Search"; then
    echo "Elasticsearch is successfully installed and running!"
else
    echo "Elasticsearch installation failed or the service is not running."
fi
