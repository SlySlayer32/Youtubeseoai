#!/bin/bash

echo "Setting up YouTube SEO Generator environment..."

# Load environment variables from .env file
if [ -f .env ]; then
  echo "Loading environment variables from .env file..."
  export $(grep -v '^#' .env | xargs)
else
  echo "Error: .env file not found. Exiting..."
  exit 1
fi

# Check required environment variables
if [ -z "$YOUTUBE_API_KEY" ]; then
  echo "Error: YOUTUBE_API_KEY environment variable is not set. Exiting..."
  exit 1
fi

# Check required environment variables
if [ -z "$REDIS_URL" ]; then
  echo "Error: REDIS_URL environment variable is not set. Exiting..."
  exit 1
fi

# Change directory to where docker-compose.yaml is located
cd "$(dirname "$0")"

# Build all services
echo "Building Docker containers for all services..."
docker-compose build
if [ $? -ne 0 ]; then
  echo "Error building Docker containers. Exiting..."
  exit 1
fi

# Start the services
echo "Starting all services..."
docker-compose up -d
if [ $? -ne 0 ]; then
  echo "Error starting services. Exiting..."
  exit 1
fi

echo "Setup complete! Your services are now running."
echo "- Access the Chat WebUI at http://localhost:80"
echo "- To view logs: docker-compose logs -f"
echo "- To stop services: docker-compose down"
