# Scripts

This document describes the important scripts and commands used to run and manage this project.

## Docker Compose Commands

These commands are used to manage the entire application stack using Docker Compose.

- **`docker-compose up`**:
    - Description: Starts all services defined in the `docker-compose.yml` file.
    - How to run: Execute this command from the root directory of the project (where `docker-compose.yml` is located).
    - Directory: `g:/Half built apps/Youtube`

- **`docker-compose down`**:
    - Description: Stops all services defined in the `docker-compose.yml` file.
    - How to run: Execute this command from the root directory of the project.
    - Directory: `g:/Half built apps/Youtube`

- **`docker-compose build`**:
    - Description: Builds the Docker images for all services defined in the `docker-compose.yml` file.
    - How to run: Execute this command from the root directory of the project.
    - Directory: `g:/Half built apps/Youtube`

- **`docker-compose up -d`**:
    - Description: Starts all services in detached mode (running in the background).
    - How to run: Execute this command from the root directory of the project.
    - Directory: `g:/Half built apps/Youtube`

- **`docker-compose logs <service_name>`**:
    - Description: Views the logs of a specific service. Replace `<service_name>` with the name of the service (e.g., `chat-service`, `seo-service`, `api-gateway`).
    - How to run: Execute this command from the root directory of the project.
    - Directory: `g:/Half built apps/Youtube`

## Python Service Commands

These commands are used to run individual backend services directly (for development or debugging purposes).  You need to navigate to the service's directory first.

- **`chat-service`**:
    - Description: Runs the chat service.
    - How to run: `python src/app.py`
    - Directory: `g:/Half built apps/Youtube/chat-service`

- **`seo-service`**:
    - Description: Runs the seo service.
    - How to run: `python src/app.py`
    - Directory: `g:/Half built apps/Youtube/seo-service`

- **`api-gateway`**:
    - Description: Runs the api gateway.
    - How to run: `python src/app.py`
    - Directory: `g:/Half built apps/Youtube/api-gateway`

- **`knowledge-service`**:
    - Description: Runs the knowledge service.
    - How to run: `python src/app.py`
    - Directory: `g:/Half built apps/Youtube/knowledge-service`

- **`video-service`**:
    - Description: Runs the video service.
    - How to run: `python src/app.py`
    - Directory: `g:/Half built apps/Youtube/video-service`
