import json
import time

import requests
from api_gateway.src.utils.error_handlers import (
    handle_bad_request,
    handle_internal_server_error,
    handle_not_found,
    handle_service_unavailable,
    handle_timeout,
)
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

# This is a test comment to trigger pre-commit hooks


app = Flask(__name__)
CORS(app)

# Register error handlers
app.register_error_handler(400, handle_bad_request)
app.register_error_handler(404, handle_not_found)
app.register_error_handler(500, handle_internal_server_error)
app.register_error_handler(503, handle_service_unavailable)
app.register_error_handler(504, handle_timeout)

# Define metrics
API_REQUESTS = Counter("api_requests_total", "Total API requests", ["method", "endpoint", "status"])
API_LATENCY = Histogram(
    "api_request_duration_seconds", "API request latency", ["method", "endpoint"]
)

# Service endpoints
CHAT_SERVICE = "http://chat-service:5000"
SEO_SERVICE = "http://seo-service:5001"
KNOWLEDGE_SERVICE = "http://knowledge-service:5002"
VIDEO_SERVICE = "http://video-service:5003"


@app.route("/")
def hello_world():
    return jsonify({"message": "Hello from API Gateway!"})


@app.route("/metrics")
def metrics():
    """Expose metrics for Prometheus"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/api/chat", methods=["POST"])
def chat_proxy():
    """Proxy requests to the chat service"""
    start_time = time.time()
    try:
        response = requests.post(f"{CHAT_SERVICE}/api/chat", json=request.json, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        API_REQUESTS.labels(method="POST", endpoint="/api/chat", status=response.status_code).inc()
        return Response(response.iter_content(), mimetype=response.headers["Content-Type"])
    except requests.exceptions.Timeout as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/chat", status="500").inc()
        return jsonify({"error": "Request timed out"}), 500
    except requests.exceptions.ConnectionError as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/chat", status="500").inc()
        return jsonify({"error": "Could not connect to chat service"}), 500
    except requests.exceptions.RequestException as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/chat", status="500").inc()
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        latency = time.time() - start_time
        API_LATENCY.labels(method="POST", endpoint="/api/chat").observe(latency)


@app.route("/api/seo/generate", methods=["POST"])
def seo_generate_proxy():
    """Proxy requests to the SEO service"""
    start_time = time.time()
    try:
        response = requests.post(f"{SEO_SERVICE}/generate", json=request.json, stream=True)
        response.raise_for_status()
        API_REQUESTS.labels(
            method="POST", endpoint="/api/seo/generate", status=response.status_code
        ).inc()
        return Response(response.iter_content(), mimetype=response.headers["Content-Type"])
    except requests.exceptions.Timeout as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/seo/generate", status="500").inc()
        return jsonify({"error": "Request timed out"}), 500
    except requests.exceptions.ConnectionError as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/seo/generate", status="500").inc()
        return jsonify({"error": "Could not connect to SEO service"}), 500
    except requests.exceptions.RequestException as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/seo/generate", status="500").inc()
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        latency = time.time() - start_time
        API_LATENCY.labels(method="POST", endpoint="/api/seo/generate").observe(latency)


@app.route("/api/knowledge/ingest", methods=["POST"])
def knowledge_ingest_proxy():
    """Proxy requests to the knowledge service for ingestion"""
    start_time = time.time()
    try:
        response = requests.post(f"{KNOWLEDGE_SERVICE}/ingest", json=request.json)
        response.raise_for_status()
        API_REQUESTS.labels(
            method="POST", endpoint="/api/knowledge/ingest", status=response.status_code
        ).inc()
        return jsonify(response.json())
    except requests.exceptions.Timeout as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/knowledge/ingest", status="500").inc()
        return jsonify({"error": "Request timed out"}), 500
    except requests.exceptions.ConnectionError as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/knowledge/ingest", status="500").inc()
        return jsonify({"error": "Could not connect to knowledge service"}), 500
    except requests.exceptions.RequestException as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/knowledge/ingest", status="500").inc()
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        latency = time.time() - start_time
        API_LATENCY.labels(method="POST", endpoint="/api/knowledge/ingest").observe(latency)


@app.route("/api/knowledge/query", methods=["POST"])
def knowledge_query_proxy():
    """Proxy requests to the knowledge service for querying"""
    start_time = time.time()
    try:
        response = requests.post(f"{KNOWLEDGE_SERVICE}/query", json=request.json)
        response.raise_for_status()
        API_REQUESTS.labels(
            method="POST", endpoint="/api/knowledge/query", status=response.status_code
        ).inc()
        return jsonify(response.json())
    except requests.exceptions.Timeout as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/knowledge/query", status="500").inc()
        return jsonify({"error": "Request timed out"}), 500
    except requests.exceptions.ConnectionError as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/knowledge/query", status="500").inc()
        return jsonify({"error": "Could not connect to knowledge service"}), 500
    except requests.exceptions.RequestException as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/knowledge/query", status="500").inc()
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        latency = time.time() - start_time
        API_LATENCY.labels(method="POST", endpoint="/api/knowledge/query").observe(latency)


@app.route("/api/video/process", methods=["POST"])
def video_process_proxy():
    """Proxy requests to the video service for processing"""
    start_time = time.time()
    try:
        files = {"video": (request.files["video"].filename, request.files["video"])}
        response = requests.post(f"{VIDEO_SERVICE}/process-video", files=files)
        response.raise_for_status()
        API_REQUESTS.labels(
            method="POST", endpoint="/api/video/process", status=response.status_code
        ).inc()
        return jsonify(response.json())
    except requests.exceptions.Timeout as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/video/process", status="500").inc()
        return jsonify({"error": "Request timed out"}), 500
    except requests.exceptions.ConnectionError as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/video/process", status="500").inc()
        return jsonify({"error": "Could not connect to video service"}), 500
    except requests.exceptions.RequestException as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/video/process", status="500").inc()
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        latency = time.time() - start_time
        API_LATENCY.labels(method="POST", endpoint="/api/video/process").observe(latency)


@app.route("/api/video/upload", methods=["POST"])
def video_upload_proxy():
    """Proxy requests to the video service for YouTube uploading"""
    start_time = time.time()
    try:
        response = requests.post(f"{VIDEO_SERVICE}/upload-to-youtube", json=request.json)
        response.raise_for_status()
        API_REQUESTS.labels(
            method="POST", endpoint="/api/video/upload", status=response.status_code
        ).inc()
        return jsonify(response.json())
    except requests.exceptions.Timeout as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/video/upload", status="500").inc()
        return jsonify({"error": "Request timed out"}), 500
    except requests.exceptions.ConnectionError as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/video/upload", status="500").inc()
        return jsonify({"error": "Could not connect to video service"}), 500
    except requests.exceptions.RequestException as e:
        API_REQUESTS.labels(method="POST", endpoint="/api/video/upload", status="500").inc()
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        latency = time.time() - start_time
        API_LATENCY.labels(method="POST", endpoint="/api/video/upload").observe(latency)


@app.route("/api/workflow/generate-and-upload", methods=["POST"])
def generate_and_upload_workflow():
    """Workflow that combines SEO generation and video processing/upload"""
    start_time = time.time()
    try:
        # Validate input
        if "keyword" not in request.form or "video" not in request.files:
            API_REQUESTS.labels(
                method="POST", endpoint="/api/workflow/generate-and-upload", status="400"
            ).inc()
            return jsonify({"error": "Both keyword and video file are required"}), 400

        keyword = request.form["keyword"]
        video_file = request.files["video"]

        if not video_file:
            API_REQUESTS.labels(
                method="POST", endpoint="/api/workflow/generate-and-upload", status="400"
            ).inc()
            return jsonify({"error": "Video file is required"}), 400

        # Step 1: Generate SEO data
        try:
            seo_response = requests.post(f"{SEO_SERVICE}/generate", json={"keyword": keyword})
            seo_response.raise_for_status()
            seo_data = seo_response.json()
        except requests.exceptions.RequestException as e:
            API_REQUESTS.labels(
                method="POST", endpoint="/api/workflow/generate-and-upload", status="500"
            ).inc()
            return jsonify({"error": f"Error generating SEO data: {str(e)}"}), 500

        # Step 2: Process the video
        try:
            files = {"video": (video_file.filename, video_file)}
            process_response = requests.post(f"{VIDEO_SERVICE}/process-video", files=files)
            process_response.raise_for_status()
            processed_data = process_response.json()
            if "error" in processed_data:
                return jsonify(processed_data), process_response.status_code
        except requests.exceptions.RequestException as e:
            API_REQUESTS.labels(
                method="POST", endpoint="/api/workflow/generate-and-upload", status="500"
            ).inc()
            return jsonify({"error": f"Error processing video: {str(e)}"}), 500

        # Step 3: Upload to YouTube
        try:
            upload_data = {
                "video_file": processed_data["processed_file"],
                "title": seo_data.get("title", "Default Title"),
                "description": seo_data.get("description", "Default Description"),
                "tags": seo_data.get("tags", []),
            }
            upload_response = requests.post(f"{VIDEO_SERVICE}/upload-to-youtube", json=upload_data)
            upload_response.raise_for_status()

            API_REQUESTS.labels(
                method="POST",
                endpoint="/api/workflow/generate-and-upload",
                status=upload_response.status_code,
            ).inc()
            return jsonify(upload_response.json())
        except requests.exceptions.RequestException as e:
            API_REQUESTS.labels(
                method="POST", endpoint="/api/workflow/generate-and-upload", status="500"
            ).inc()
            return jsonify({"error": f"Error uploading to YouTube: {str(e)}"}), 500

    except Exception as e:
        API_REQUESTS.labels(
            method="POST", endpoint="/api/workflow/generate-and-upload", status="500"
        ).inc()
        return jsonify({"error": f"Workflow error: {str(e)}"}), 500
    finally:
        latency = time.time() - start_time
        API_LATENCY.labels(method="POST", endpoint="/api/workflow/generate-and-upload").observe(
            latency
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
