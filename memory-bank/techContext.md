# Tech Context

## Technologies Used

- **Programming Languages:** Python, JavaScript, potentially React for frontend components.
- **Backend Frameworks:** Flask (Python) for microservices.
- **Frontend Frameworks/Libraries:** Vanilla JavaScript (existing Chat WebUI), React (for new SEO dashboard and potentially refactored components).
- **Containerization:** Docker.
- **Orchestration:** Docker Compose (local), Kubernetes (production).
- **Caching:** Redis.
- **Monitoring and Analytics:** Prometheus, Grafana.
- **CI/CD:** GitHub Actions.
- **YouTube API:** For SEO service and potentially video service.
- **LLMs:** Multiple LLMs for chat interface and SEO content generation (details to be specified).

## Development Setup

- **Local Development Environment:** Docker Compose to run all services locally, environment variables managed via `.env` file.
- **Version Control:** Git, GitHub.
- **Testing Frameworks:** pytest (Python).
- **Linting:** flake8 (Python).

## Environment Variables

- Environment variables are managed using a `.env` file at the root of the project.
- The following environment variables must be set in the `.env` file:
    - `YOUTUBE_API_KEY`: YouTube Data API v3 key.
    - `YOUTUBE_CREDENTIALS`: YouTube API credentials in JSON format.
    - `REDIS_URL`: URL for the Redis instance.

## Scripts

Refer to `docs/scripts.md` for a list of useful scripts and commands for running and managing this project.

## Technical Constraints

- **Performance:** The system should be performant and scalable to handle a large number of users and requests. Caching and load balancing will be crucial.
- **Scalability:** The microservices architecture should allow for independent scaling of each service based on demand.
- **Maintainability:** The codebase should be modular and well-documented to ensure maintainability.
- **Security:** Secure API communication between services and protect user data.
- **YouTube API Limits:** Be mindful of YouTube API usage limits and implement appropriate error handling and retry mechanisms.
- **LLM API Limits and Costs:** Consider API limits and costs associated with different LLM providers.

## Dependencies

- **Python Dependencies:** Flask, Flask-CORS, requests, prometheus-client, potentially google-api-python-client, ffmpeg-python, tenacity, sqlite3, etc. (detailed in `requirements.txt` for each service).
- **JavaScript Dependencies:** React, react-chartjs-2, antd (for SEO dashboard, potentially managed via npm/yarn if React is used more extensively).
- **Docker:** Docker and Docker Compose should be installed for local development.
- **Kubernetes:** Kubernetes cluster access for production deployment.
- **Redis:** Redis instance for caching.
- **Prometheus and Grafana:** Prometheus and Grafana instances for monitoring.
- **GitHub Actions:** GitHub repository for CI/CD pipeline.
- **YouTube API Key:** Required for SEO service and video service.
- **LLM API Keys:** API keys for the chosen LLM providers.
