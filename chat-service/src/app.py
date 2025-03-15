import time

from flask import Flask, Response, jsonify
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)

# Define metrics
CHAT_REQUESTS = Counter("chat_requests_total", "Total chat requests")
CHAT_LATENCY = Histogram("chat_request_duration_seconds", "Chat request latency")


@app.route("/")
def hello_world():
    return jsonify({"message": "Hello from Chat Service!"})


@app.route("/metrics")
def metrics():
    """Expose metrics for Prometheus"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/api/chat")
def chat():
    """Chat endpoint"""
    start_time = time.time()
    try:
        # Simulate some work
        message = "Simulated chat response"
        status_code = 200
        return jsonify({"message": message})
    except Exception as e:
        status_code = 500
        return jsonify({"error": str(e)}), 500
    finally:
        latency = time.time() - start_time
        CHAT_REQUESTS.inc()
        CHAT_LATENCY.observe(latency)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
