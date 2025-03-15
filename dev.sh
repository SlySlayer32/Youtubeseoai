#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: ./dev.sh <service-name>"
  echo "Available services:"
  echo "  - api-gateway"
  echo "  - chat-service"
  echo "  - seo-service"
  echo "  - knowledge-service"
  echo "  - video-service"
  exit 1
fi

docker-compose exec $1 /bin/bash
