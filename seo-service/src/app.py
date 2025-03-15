import json
import os
import time

import requests
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from seo_generator import (
    calculate_seo_score,
    generate_description,
    generate_hashtags,
    generate_tags,
    generate_titles,
    get_mock_analytics,
    identify_category,
)

from ab_testing import ABTesting

ab_testing = ABTesting()

API_KEY = os.environ.get("YOUTUBE_API_KEY")
if not API_KEY:
    raise ValueError("No YOUTUBE_API_KEY set")

app = Flask(__name__)
CORS(app)

# Define metrics
SEO_REQUESTS = Counter("seo_requests_total", "Total SEO generation requests")
SEO_LATENCY = Histogram("seo_request_duration_seconds", "SEO generation latency")


@app.route("/metrics")
def metrics():
    """Expose metrics for Prometheus"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/generate", methods=["POST"])
def generate_seo_content():
    """Generate SEO content based on keyword"""
    start_time = time.time()
    try:
        data = request.json
        keyword = data.get("keyword")
        conversation_context = data.get("conversation_context", [])

        # Generate SEO content
        category = identify_category(keyword)
        titles = generate_titles(keyword, category)

        # A/B test the titles
        experiment_name = f"SEO Title A/B Test - {keyword}"
        experiment_id = ab_testing.create_experiment(
            experiment_name,
            {
                "Original Title": titles[0],
                "Alternative Title": titles[1] if len(titles) > 1 else titles[0],
            },
        )

        variant = ab_testing.get_random_variant(experiment_id)
        selected_title = variant["content"]

        # Stream back results
        def generate():
            yield json.dumps({"type": "titles", "data": titles}) + "\\n"

            yield json.dumps({"type": "selected_title", "data": selected_title}) + "\\n"

            description = generate_description(keyword, category, selected_title)
            yield json.dumps({"type": "description", "data": description}) + "\\n"

            tags = generate_tags(keyword, category)
            yield json.dumps({"type": "tags", "data": tags}) + "\\n"

            hashtags = generate_hashtags(tags, keyword)
            yield json.dumps({"type": "hashtags", "data": hashtags}) + "\\n"

            seo_score = calculate_seo_score(selected_title, description, tags, hashtags)
            yield json.dumps({"type": "seo_score", "data": seo_score}) + "\\n"

            analytics = get_mock_analytics()
            yield json.dumps({"type": "analytics", "data": analytics}) + "\\n"

            top_videos = get_top_videos(API_KEY, keyword)
            yield json.dumps({"type": "top_videos", "data": top_videos}) + "\\n"

        response = Response(generate(), mimetype="text/event-stream")
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        latency = time.time() - start_time
        SEO_REQUESTS.inc()
        SEO_LATENCY.observe(latency)


def select_best_title(titles, conversation_context):
    # Logic to select best title based on conversation context
    # Use LLM to analyze conversation and pick most relevant title
    # For now, just return first title
    return titles[0]


def get_top_videos(api_key: str, query: str, max_results: int = 5) -> list[dict]:
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults={max_results}&key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        videos = response.json().get("items", [])
        return [
            {
                "title": v["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={v['id']['videoId']}"
                if "videoId" in v["id"]
                else None,
            }
            for v in videos
        ]
    except requests.RequestException as e:
        print(f"Error fetching videos: {e}")
        return []


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
