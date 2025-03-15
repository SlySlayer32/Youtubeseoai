import json
import time

from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)
CORS(app)

# Define metrics
KNOWLEDGE_REQUESTS = Counter("knowledge_requests_total", "Total knowledge requests", ["endpoint"])
KNOWLEDGE_LATENCY = Histogram(
    "knowledge_request_duration_seconds", "Knowledge request latency", ["endpoint"]
)

knowledge_data = {}


@app.route("/metrics")
def metrics():
    """Expose metrics for Prometheus"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/ingest", methods=["POST"])
def ingest_knowledge():
    """Endpoint to ingest knowledge data"""
    start_time = time.time()
    try:
        data = request.json
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid knowledge data format. Must be a JSON object."}), 400
        knowledge_id = data.get("id")
        if not knowledge_id:
            return jsonify({"error": "Knowledge data must have an 'id' field."}), 400
        knowledge_data[knowledge_id] = data
        result = jsonify(
            {
                "status": "success",
                "message": f"Knowledge ingested with id: {knowledge_id}",
                "knowledge_ids": list(knowledge_data.keys()),
            }
        )
        KNOWLEDGE_REQUESTS.labels(endpoint="/ingest").inc()
        return result
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        latency = time.time() - start_time
        KNOWLEDGE_LATENCY.labels(endpoint="/ingest").observe(latency)


@app.route("/query", methods=["POST"])
def query_knowledge():
    """Endpoint to query knowledge data"""
    start_time = time.time()
    try:
        query = request.json.get("query")
        if not query:
            return jsonify({"error": "Query text is required."}), 400
        results = []
        for knowledge_item in knowledge_data.values():
            if query.lower() in json.dumps(knowledge_item).lower():  # Simple keyword search
                results.append(knowledge_item)
        result = jsonify({"status": "success", "query": query, "response": results})
        KNOWLEDGE_REQUESTS.labels(endpoint="/query").inc()
        return result
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        latency = time.time() - start_time
        KNOWLEDGE_LATENCY.labels(endpoint="/query").observe(latency)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
