# Project Overview

This project combines a multi-LLM chat interface with a YouTube SEO generator to streamline content creation and optimization for YouTube videos.

## Project Structure

The project is structured as a modular microservices architecture. The main directories are:

- `api-gateway`:  API Gateway service (Flask/Python).
- `chat-service`: Chat service (Flask/Python), enhanced with SEO features.
- `seo-service`: SEO content generation service (Flask/Python).
- `knowledge-service`: (Future) Knowledge management service (Flask/Python).
- `video-service`: (Future) Video processing and YouTube upload service (Flask/Python).
- `Chat-WebUI-main`:  The existing Chat WebUI frontend (Vanilla JavaScript).
- `memory-bank`: Contains project documentation and context.
- `docs`: Contains project documentation, including this `readme.md` and `scripts.md`.

## Memory Bank Documentation

The `memory-bank` folder contains important project documentation:

- `project-brief.md`:  Core requirements and goals of the project.
- `productContext.md`:  Purpose, problems solved, and user experience goals.
- `activeContext.md`:  Current work focus, recent changes, and next steps.
- `systemPatterns.md`:  System architecture, design patterns, and component relationships.
- `techContext.md`:  Technologies used, development setup, and technical constraints.
- `progress.md`:  What works, what's left to build, and current status.
- `.clinerules`: Project intelligence and learned patterns.

## Setup

To set up the development environment, follow these steps:

1.  **Install Docker and Docker Compose**:  Make sure you have Docker and Docker Compose installed on your system.  Refer to the official Docker documentation for installation instructions.
2.  **Install Python Dependencies**:  Each service (`chat-service`, `seo-service`, `api-gateway`, `knowledge-service`, `video-service`) has its own `requirements.txt` file.  Navigate to each service directory and run `pip install -r requirements.txt` to install the necessary Python packages.
3.  **Set Environment Variables**:
    - You need to set the following environment variables:
        - `YOUTUBE_CREDENTIALS`:  (Required for `video-service`) Credentials for accessing the YouTube API.
        - `YOUTUBE_API_KEY`: (Required for `seo-service`) API key for accessing the YouTube API.
        - `REDIS_URL`: (Required for `chat-service`) URL for the Redis instance.
    - **Important**: Since MCP servers cannot directly prompt for user input during runtime, you will need to set these environment variables manually in your system or in the Docker Compose configuration.
    - **Note**: The `YOUTUBE_CREDENTIALS` environment variable requires a JSON string. You may need to escape the JSON string when setting it as an environment variable.

## Quick Setup with Docker

For the easiest setup, use the provided scripts:

1. Make sure Docker and Docker Compose are installed on your system
2. Set required environment variables:
   ```bash
   export YOUTUBE_API_KEY=your_api_key
   export YOUTUBE_CREDENTIALS='{"your":"credentials"}'
   export REDIS_URL=redis://redis:6379/0
   ```
3. Run the setup script:
   ```bash
   ./setup.sh
   ```

That's it! All services will be built and started automatically.

To access a development shell in any service:
```bash
./dev.sh api-gateway  # Replace with any service name
```

## Quality Checks

To run tests and linting:
```bash
./quality.sh all
```

To automatically fix linting issues:
```bash
./quality.sh fix
```

## Running the Application

To start the entire application stack, use Docker Compose:

1.  Navigate to the root directory of the project (`g:/Half built apps/Youtube`).
2.  Run the command `docker-compose up`.  This will start all the services defined in the `docker-compose.yml` file.
3.  To run the services in detached mode (in the background), use the command `docker-compose up -d`.

## Accessing the Application

Once the services are running:

-   **Chat WebUI**:  Access the Chat WebUI in your browser. The port may vary depending on your setup, but it's typically on port 80 (API Gateway).
-   **API Gateway**:  The API Gateway is the entry point for all services.  You can access the API endpoints through the API Gateway's URL (e.g., `http://localhost:80/api/chat`, `http://localhost:80/api/seo/generate`).

## Testing

The project uses `pytest` for testing (Python). To run the tests:

1.  Navigate to the directory containing the tests (e.g., the service directory).
2.  Run the command `pytest`.

## Further Information

-   See `docs/scripts.md` for a list of useful scripts and commands.
-   Refer to the `memory-bank` folder for detailed project documentation and context.
