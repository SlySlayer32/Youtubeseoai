#!/bin/bash

ACTION=$1
SERVICE=$2

# Default to all services if none specified
if [ -z "$SERVICE" ]; then
  SERVICES=("api-gateway" "chat-service" "seo-service" "knowledge-service" "video-service")
else
  SERVICES=("$SERVICE")
fi

# Function to run tests
run_tests() {
  for service in "${SERVICES[@]}"; do
    echo "Running tests for $service..."
    docker-compose run --rm $service pytest -v
  done
}

# Function to run lint checks
run_lint() {
  for service in "${SERVICES[@]}"; do
    echo "Running lint checks for $service..."
    docker-compose run --rm $service flake8 .
  done
}

# Function to automatically fix linting issues
fix_lint() {
  for service in "${SERVICES[@]}"; do
    echo "Auto-fixing code in $service..."
    docker-compose run --rm $service bash -c "black . && isort ."
  done
}

# Main execution
case "$ACTION" in
  "test")
    run_tests
    ;;
  "lint")
    run_lint
    ;;
  "fix")
    fix_lint
    ;;
  "all")
    run_tests
    run_lint
    ;;
  *)
    echo "Usage: ./quality.sh [test|lint|fix|all] [service-name]"
    echo "Examples:"
    echo "  ./quality.sh test           # Run tests for all services"
    echo "  ./quality.sh lint chat-service  # Run lint checks for chat-service only"
    echo "  ./quality.sh fix            # Auto-fix code style in all services"
    echo "  ./quality.sh all            # Run both tests and lint checks"
    exit 1
    ;;
esac
