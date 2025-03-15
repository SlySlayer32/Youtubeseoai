import json
import os
import tempfile
import time

import ffmpeg
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from tenacity import retry, stop_after_attempt, wait_exponential

app = Flask(__name__)
CORS(app)

# Define metrics
VIDEO_REQUESTS = Counter("video_requests_total", "Total video requests", ["endpoint"])
VIDEO_LATENCY = Histogram("video_request_duration_seconds", "Video request latency", ["endpoint"])


@app.route("/metrics")
def metrics():
    """Expose metrics for Prometheus"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/process-video", methods=["POST"])
def process_video():
    """Process and prepare video for upload"""
    start_time = time.time()
    try:
        if "video" not in request.files:
            return jsonify({"error": "No video file provided"}), 400

        video_file = request.files["video"]

        # Save temporary file
        temp_input = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        temp_output = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        video_file.save(temp_input.name)

        try:
            # Process video with ffmpeg
            (
                ffmpeg.input(temp_input.name)
                .output(
                    temp_output.name,
                    vcodec="libx264",
                    preset="medium",
                    acodec="aac",
                    audio_bitrate="128k",
                    crf=23,
                )
                .run(quiet=True, overwrite_output=True)
            )

            # Get file size and duration for metrics
            probe = ffmpeg.probe(temp_output.name)
            duration = float(probe["format"]["duration"])
            file_size = os.path.getsize(temp_output.name)

            result = jsonify(
                {
                    "status": "success",
                    "processed_file": temp_output.name,
                    "duration": duration,
                    "file_size": file_size,
                }
            )
            VIDEO_REQUESTS.labels(endpoint="/process-video").inc()
            return result
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            # Clean up input file if processing is complete
            if os.path.exists(temp_input.name):
                os.unlink(temp_input.name)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        latency = time.time() - start_time
        VIDEO_LATENCY.labels(endpoint="/process-video").observe(latency)


@app.route("/upload-to-youtube", methods=["POST"])
@retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(3))
def upload_to_youtube():
    """Upload processed video to YouTube with generated SEO content"""
    start_time = time.time()
    try:
        data = request.json
        video_file = data.get("video_file")
        title = data.get("title")
        description = data.get("description")
        tags = data.get("tags", [])
        category_id = data.get("category_id", "22")  # Default to People & Blogs

        if not all([video_file, title, description]):
            return jsonify({"error": "Missing required parameters"}), 400

        youtube_credentials_json = os.environ.get("YOUTUBE_CREDENTIALS")
        if not youtube_credentials_json:
            return jsonify({"error": "YOUTUBE_CREDENTIALS environment variable is not set"}), 500
        try:
            credentials = Credentials.from_authorized_user_info(
                json.loads(youtube_credentials_json)
            )
        except Exception as e:
            return jsonify({"error": f"Failed to load YouTube credentials: {str(e)}"}), 500

        try:
            # Initialize YouTube API client
            youtube = build("youtube", "v3", credentials=credentials)

            # Prepare upload request
            request_body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": category_id,
                },
                "status": {"privacyStatus": "private"},  # Start as private, can be changed later
            }

            # Execute upload
            media = MediaFileUpload(video_file, mimetype="video/*", resumable=True)

            upload_response = (
                youtube.videos()
                .insert(part="snippet,status", body=request_body, media_body=media)
                .execute()
            )

            video_id = upload_response.get("id")

            # Clean up the processed file
            if os.path.exists(video_file):
                os.unlink(video_file)

            result = jsonify(
                {
                    "status": "success",
                    "video_id": video_id,
                    "video_url": f"https://www.youtube.com/watch?v={video_id}",
                }
            )
            VIDEO_REQUESTS.labels(endpoint="/upload-to-youtube").inc()
            return result
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        latency = time.time() - start_time
        VIDEO_LATENCY.labels(endpoint="/upload-to-youtube").observe(latency)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
