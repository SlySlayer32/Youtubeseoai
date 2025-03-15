I recommend a modular microservices architecture that integrates the Chat WebUI with the YouTube SEO Generator with the project-brief the focus point of the project while ensuring scalability and performance.

# Modular Component Integration

1. Core Service Layer
Container Orchestration:
Use Docker Compose for local development and deployment
```
services:
  chat-service:
    build: ./chat-service
    ports:
      - "5000:5000"
  seo-service:
    build: ./seo-service
    ports:
      - "5001:5001"
  api-gateway:
    build: ./api-gateway
    ports:
      - "80:80"
```
file: docker-compose.yml

2. Chat Service Enhancement (Based on Chat-WebUI)
The Chat WebUI provides an excellent foundation for the Multi-LLM Chat Interface component. I'll recommend these enhancements:

# Extend the existing Chat WebUI app.py with SEO-specific routes and functionality.
```
@app.route('/api/seo/generate', methods=['POST'])
def generate_seo_content():
    """
    Generate SEO content via the SEO service
    """
    keyword = request.json.get('keyword')
    model = request.json.get('model', 'default-model')
    conversation_history = request.json.get('conversation', [])

    # Call SEO service
    seo_response = requests.post(
        'http://seo-service:5001/generate',
        json={
            'keyword': keyword,
            'conversation_context': conversation_history
        }
    )

    # Return streaming response with SEO content
    return Response(stream_with_context(seo_response.iter_content()),
                   mimetype='text/event-stream')
```
file: app.py

3. SEO Service (Based on YouTube SEO Generator)
Convert the existing YouTube SEO Generator script into a service:
```
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
from seo_generator import (
    identify_category, generate_titles, generate_description,
    generate_tags, generate_hashtags, calculate_seo_score,
    get_top_videos, get_mock_analytics
)

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate_seo_content():
    """Generate SEO content based on keyword"""
    data = request.json
    keyword = data.get('keyword')
    conversation_context = data.get('conversation_context', [])

    # Generate SEO content
    category = identify_category(keyword)
    titles = generate_titles(keyword, category)

    # Stream back results
    def generate():
        yield json.dumps({"type": "titles", "data": titles}) + "\n"

        # Choose best title based on context or predefined criteria
        selected_title = select_best_title(titles, conversation_context)
        yield json.dumps({"type": "selected_title", "data": selected_title}) + "\n"

        description = generate_description(keyword, category, selected_title)
        yield json.dumps({"type": "description", "data": description}) + "\n"

        tags = generate_tags(keyword, category)
        yield json.dumps({"type": "tags", "data": tags}) + "\n"

        hashtags = generate_hashtags(tags, keyword)
        yield json.dumps({"type": "hashtags", "data": hashtags}) + "\n"

        seo_score = calculate_seo_score(selected_title, description, tags, hashtags)
        yield json.dumps({"type": "seo_score", "data": seo_score}) + "\n"

        analytics = get_mock_analytics()
        yield json.dumps({"type": "analytics", "data": analytics}) + "\n"

    return Response(generate(), mimetype='text/event-stream')

def select_best_title(titles, conversation_context):
    # Logic to select best title based on conversation context
    # Use LLM to analyze conversation and pick most relevant title
    # For now, just return first title
    return titles[0]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```
file: seo-service.py


4. Frontend Integration
Enhance the existing Chat WebUI frontend to incorporate SEO features:
```
// Add SEO mode toggle to UI

function initializeSEOMode() {
    const seoToggle = document.createElement('button');
    seoToggle.classList.add('seo-mode-toggle');
    seoToggle.textContent = 'SEO Mode';
    seoToggle.addEventListener('click', toggleSEOMode);
    document.querySelector('.chat-controls').appendChild(seoToggle);
}

function toggleSEOMode() {
    const isSEOMode = !appState.seoMode;
    appState.seoMode = isSEOMode;
    document.querySelector('.seo-mode-toggle').classList.toggle('active', isSEOMode);

    if (isSEOMode) {
        showSEOInterface();
    } else {
        hideSEOInterface();
    }
}

function showSEOInterface() {
    // Create SEO panel
    const seoPanel = document.createElement('div');
    seoPanel.classList.add('seo-panel');
    seoPanel.innerHTML = `
        <h3>YouTube SEO Generator</h3>
        <div class="seo-input">
            <input type="text" id="seo-keyword" placeholder="Enter keyword for SEO content">
            <button id="generate-seo">Generate</button>
        </div>
        <div class="seo-results"></div>
    `;

    document.querySelector('.chat-container').appendChild(seoPanel);

    // Add event listener
    document.getElementById('generate-seo').addEventListener('click', generateSEOContent);
}

async function generateSEOContent() {
    const keyword = document.getElementById('seo-keyword').value;
    const resultsContainer = document.querySelector('.seo-results');

    resultsContainer.innerHTML = '<div class="loading">Generating SEO content...</div>';

    try {
        // Call the SEO generation endpoint
        const response = await fetch('/api/seo/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                keyword: keyword,
                model: appState.selectedModel,
                conversation: appState.conversations[appState.currentConversationId]
            })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        resultsContainer.innerHTML = `
            <div class="seo-content">
                <div class="titles-container"></div>
                <div class="description-container"></div>
                <div class="tags-container"></div>
                <div class="hashtags-container"></div>
                <div class="score-container"></div>
                <div class="analytics-container"></div>
            </div>
        `;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const lines = decoder.decode(value).split('\n');
            for (const line of lines) {
                if (!line.trim()) continue;

                try {
                    const data = JSON.parse(line);
                    updateSEOInterface(data);
                } catch (e) {
                    console.error('Error parsing SSE data:', e);
                }
            }
        }
    } catch (error) {
        resultsContainer.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

function updateSEOInterface(data) {
    const { type, data: content } = data;

    switch (type) {
        case 'titles':
            const titlesContainer = document.querySelector('.titles-container');
            titlesContainer.innerHTML = `
                <h4>Suggested Titles</h4>
                <ul>
                    ${content.map((title, i) => `
                        <li>
                            <input type="radio" name="title" id="title-${i}" value="${title}" ${i === 0 ? 'checked' : ''}>
                            <label for="title-${i}">${title}</label>
                        </li>
                    `).join('')}
                </ul>
            `;
            break;

        case 'selected_title':
            // Highlight the selected title
            break;

        case 'description':
            const descContainer = document.querySelector('.description-container');
            descContainer.innerHTML = `
                <h4>Description</h4>
                <textarea class="seo-description" rows="8">${content}</textarea>
            `;
            break;

        case 'tags':
            const tagsContainer = document.querySelector('.tags-container');
            tagsContainer.innerHTML = `
                <h4>Tags</h4>
                <div class="tags-list">
                    ${content.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            `;
            break;

        case 'hashtags':
            const hashtagsContainer = document.querySelector('.hashtags-container');
            hashtagsContainer.innerHTML = `
                <h4>Hashtags</h4>
                <div class="hashtags-list">
                    ${content.map(tag => `<span class="hashtag">${tag}</span>`).join('')}
                </div>
            `;
            break;

        case 'seo_score':
            const scoreContainer = document.querySelector('.score-container');
            scoreContainer.innerHTML = `
                <h4>SEO Score</h4>
                <div class="seo-score-display">
                    <div class="score-bar" style="width: ${content}%"></div>
                    <span>${content}/100</span>
                </div>
            `;
            break;

        case 'analytics':
            const analyticsContainer = document.querySelector('.analytics-container');
            analyticsContainer.innerHTML = `
                <h4>Projected Analytics</h4>
                <div class="analytics-grid">
                    <div class="analytics-item">
                        <span class="label">Views</span>
                        <span class="value">${content.views.toLocaleString()}</span>
                    </div>
                    <div class="analytics-item">
                        <span class="label">Likes</span>
                        <span class="value">${content.likes.toLocaleString()}</span>
                    </div>
                    <div class="analytics-item">
                        <span class="label">Comments</span>
                        <span class="value">${content.comments.toLocaleString()}</span>
                    </div>
                    <div class="analytics-item">
                        <span class="label">Shares</span>
                        <span class="value">${content.shares.toLocaleString()}</span>
                    </div>
                </div>
            `;
            break;
    }
}
```
file: ./src/components/SEOGenerator.js

Advanced Features Implementation
1. Knowledge Management System
```
from flask import Flask, request, jsonify
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import ffmpeg
import tempfile
from tenacity import retry, wait_exponential, stop_after_attempt

app = Flask(__name__)

@app.route('/process-video', methods=['POST'])
def process_video():
    """Process and prepare video for upload"""
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']

    # Save temporary file
    temp_input = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    temp_output = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    video_file.save(temp_input.name)

    try:
        # Process video with ffmpeg
        (
            ffmpeg
            .input(temp_input.name)
            .output(temp_output.name, vcodec='libx264', preset='medium',
                    acodec='aac', audio_bitrate='128k', crf=23)
            .run(quiet=True, overwrite_output=True)
        )

        # Get file size and duration for metrics
        probe = ffmpeg.probe(temp_output.name)
        duration = float(probe['format']['duration'])
        file_size = os.path.getsize(temp_output.name)

        return jsonify({
            "status": "success",
            "processed_file": temp_output.name,
            "duration": duration,
            "file_size": file_size
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up input file if processing is complete
        if os.path.exists(temp_input.name):
            os.unlink(temp_input.name)

@app.route('/upload-to-youtube', methods=['POST'])
@retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(3))
def upload_to_youtube():
    """Upload processed video to YouTube with generated SEO content"""
    data = request.json
    video_file = data.get('video_file')
    title = data.get('title')
    description = data.get('description')
    tags = data.get('tags', [])
    category_id = data.get('category_id', '22')  # Default to People & Blogs

    if not all([video_file, title, description]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        # Initialize YouTube API client
        credentials = Credentials.from_authorized_user_info(
            json.loads(os.environ.get('YOUTUBE_CREDENTIALS')))
        youtube = build('youtube', 'v3', credentials=credentials)

        # Prepare upload request
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': 'private'  # Start as private, can be changed later
            }
        }

        # Execute upload
        media = MediaFileUpload(video_file,
                               mimetype='video/*',
                               resumable=True)

        upload_response = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        ).execute()

        video_id = upload_response.get('id')

        # Clean up the processed file
        if os.path.exists(video_file):
            os.unlink(video_file)

        return jsonify({
            "status": "success",
            "video_id": video_id,
            "video_url": f"https://www.youtube.com/watch?v={video_id}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
```
file: ./src/app.py

3. Integration Layer (API Gateway)
```
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# Service endpoints
CHAT_SERVICE = "http://chat-service:5000"
SEO_SERVICE = "http://seo-service:5001"
KNOWLEDGE_SERVICE = "http://knowledge-service:5002"
VIDEO_SERVICE = "http://video-service:5003"

@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    """Proxy requests to the chat service"""
    response = requests.post(f"{CHAT_SERVICE}/chat", json=request.json)
    return Response(response.iter_content(), mimetype=response.headers['Content-Type'])

@app.route('/api/seo/generate', methods=['POST'])
def seo_generate_proxy():
    """Proxy requests to the SEO service"""
    response = requests.post(f"{SEO_SERVICE}/generate", json=request.json)
    return Response(response.iter_content(), mimetype=response.headers['Content-Type'])

@app.route('/api/knowledge/ingest', methods=['POST'])
def knowledge_ingest_proxy():
    """Proxy requests to the knowledge service for ingestion"""
    response = requests.post(f"{KNOWLEDGE_SERVICE}/ingest", json=request.json)
    return jsonify(response.json())

@app.route('/api/knowledge/query', methods=['POST'])
def knowledge_query_proxy():
    """Proxy requests to the knowledge service for querying"""
    response = requests.post(f"{KNOWLEDGE_SERVICE}/query", json=request.json)
    return jsonify(response.json())

@app.route('/api/video/process', methods=['POST'])
def video_process_proxy():
    """Proxy requests to the video service for processing"""
    files = {'video': (request.files['video'].filename, request.files['video'])}
    response = requests.post(f"{VIDEO_SERVICE}/process-video", files=files)
    return jsonify(response.json())

@app.route('/api/video/upload', methods=['POST'])
def video_upload_proxy():
    """Proxy requests to the video service for YouTube uploading"""
    response = requests.post(f"{VIDEO_SERVICE}/upload-to-youtube", json=request.json)
    return jsonify(response.json())

@app.route('/api/workflow/generate-and-upload', methods=['POST'])
def generate_and_upload_workflow():
    """Complete workflow from SEO generation to video upload"""
    data = request.json
    keyword = data.get('keyword')
    video_file = request.files.get('video')

    if not keyword or not video_file:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        # 1. Generate SEO content
        seo_response = requests.post(
            f"{SEO_SERVICE}/generate",
            json={'keyword': keyword}
        )
        seo_data = json.loads(seo_response.text)

        # 2. Process video
        files = {'video': (video_file.filename, video_file)}
        process_response = requests.post(
            f"{VIDEO_SERVICE}/process-video",
            files=files
        )
        process_data = process_response.json()

        if process_response.status_code != 200:
            return jsonify({"error": "Video processing failed", "details": process_data}), 500

        # 3. Upload to YouTube with SEO content
        upload_response = requests.post(
            f"{VIDEO_SERVICE}/upload-to-youtube",
            json={
                'video_file': process_data['processed_file'],
                'title': seo_data['selected_title'],
                'description': seo_data['description'],
                'tags': seo_data['tags']
            }
        )

        return jsonify(upload_response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```
file: ./src/app.py

Deployment & Scaling
Docker Compose Configuration
```
version: '3.8'

services:
  api-gateway:
    build: ./api-gateway
    ports:
      - "80:80"
    depends_on:
      - chat-service
      - seo-service
      - knowledge-service
      - video-service
    networks:
      - app-network
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  chat-service:
    build: ./chat-service
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    networks:
      - app-network
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G

  seo-service:
    build: ./seo-service
    environment:
      - YOUTUBE_API_KEY=${YOUTUBE_API_KEY}
    networks:
      - app-network
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1'
          memory: 1G

  knowledge-service:
    build: ./knowledge-service
    volumes:
      - knowledge-data:/app/data
    networks:
      - app-network
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 2G

  video-service:
    build: ./video-service
    environment:
      - YOUTUBE_CREDENTIALS=${YOUTUBE_CREDENTIALS}
    volumes:
      - temp-video:/tmp
    networks:
      - app-network
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G

  redis:
    image: redis:alpine
    volumes:
      - redis-data:/data
    networks:
      - app-network

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    ports:
      - "9090:9090"
    networks:
      - app-network

  grafana:
    image: grafana/grafana
    volumes:
      - grafana-data:/var/lib/grafana
    ports:
      - "3000:3000"
    networks:
      - app-network
    depends_on:
      - prometheus

networks:
  app-network:
    driver: bridge

volumes:
  redis-data:
  knowledge-data:
  temp-video:
  prometheus-data:
  grafana-data:
```
file: ./docker-compose.yml

Kubernetes Configuration (Excerpts)
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chat-service
  template:
    metadata:
      labels:
        app: chat-service
    spec:
      containers:
      - name: chat-service
        image: ${DOCKER_REGISTRY}/chat-service:latest
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1"
        env:
        - name: REDIS_URL
          value: "redis://redis:6379"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: chat-service
spec:
  selector:
    app: chat-service
  ports:
  - port: 5000
    targetPort: 5000
  type: ClusterIP
```
file: ./kubernetes/chat-service.yaml

Performance Optimization
1. Caching Strategy
```
import redis
import json
import hashlib

class ResponseCache:
    def __init__(self, redis_url):
        self.redis = redis.from_url(redis_url)
        self.default_ttl = 3600  # 1 hour default TTL

    def get_cache_key(self, message, model, parameters):
        """Generate a deterministic cache key from request parameters"""
        key_data = {
            'message': message,
            'model': model,
            'parameters': parameters
        }
        serialized = json.dumps(key_data, sort_keys=True)
        return f"chat:response:{hashlib.md5(serialized.encode()).hexdigest()}"

    def get_cached_response(self, message, model, parameters):
        """Retrieve cached response if available"""
        cache_key = self.get_cache_key(message, model, parameters)
        cached = self.redis.get(cache_key)
        if cached:
            return json.loads(cached)
        return None

    def set_cached_response(self, message, model, parameters, response, ttl=None):
        """Cache a response with optional TTL"""
        cache_key = self.get_cache_key(message, model, parameters)
        self.redis.setex(
            cache_key,
            ttl or self.default_ttl,
            json.dumps(response)
        )
```
file: ./src/cache.py

2. Load Testing Configuration
```
from locust import HttpUser, task, between
import random

class YouTubeSEOUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def generate_seo_content(self):
        keywords = [
            "Python programming",
            "Machine learning tutorial",
            "Data science basics",
            "Web development 2023",
            "JavaScript frameworks comparison"
        ]

        self.client.post(
            "/api/seo/generate",
            json={
                "keyword": random.choice(keywords)
            },
            stream=True
        )

    @task(3)
    def chat_conversation(self):
        prompts = [
            "How to optimize YouTube videos?",
            "What are the best SEO practices for 2023?",
            "How can I increase my YouTube channel visibility?",
            "What keywords should I use for tech tutorials?",
            "How to write better video descriptions?"
        ]

        self.client.post(
            "/api/chat",
            json={
                "message": random.choice(prompts),
                "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                "conversation": []
            },
            stream=True
        )
```
file: ./locustfile.py

Monitoring & Analytics
Prometheus Configuration
```
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'api-gateway'
    static_configs:
      - targets: ['api-gateway:80']

  - job_name: 'chat-service'
    static_configs:
      - targets: ['chat-service:5000']

  - job_name: 'seo-service'
    static_configs:
      - targets: ['seo-service:5001']

  - job_name: 'knowledge-service'
    static_configs:
      - targets: ['knowledge-service:5002']

  - job_name: 'video-service'
    static_configs:
      - targets: ['video-service:5003']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```
file: ./prometheus.yml

# Adding Metrics Endpoints to Services
```
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

# Define metrics
CHAT_REQUESTS = Counter('chat_requests_total', 'Total chat requests', ['model', 'status'])
CHAT_LATENCY = Histogram('chat_request_duration_seconds', 'Chat request latency', ['model'])
SEO_REQUESTS = Counter('seo_requests_total', 'Total SEO generation requests', ['status'])
SEO_LATENCY = Histogram('seo_request_duration_seconds', 'SEO generation latency')

class MetricsMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'] == '/metrics':
            resp = generate_latest()
            headers = [
                ('Content-Type', CONTENT_TYPE_LATEST),
                ('Content-Length', str(len(resp)))
            ]
            start_response('200 OK', headers)
            return [resp]

        # For other requests, pass through to the app
        return self.app(environ, start_response)

def track_chat_request(model, status="success"):
    """Track a chat request in metrics"""
    CHAT_REQUESTS.labels(model=model, status=status).inc()

def track_chat_latency(model):
    """Create a timer context for tracking chat request latency"""
    return CHAT_LATENCY.labels(model=model).time()

def track_seo_request(status="success"):
    """Track an SEO generation request in metrics"""
    SEO_REQUESTS.labels(status=status).inc()

def track_seo_latency():
    """Create a timer context for tracking SEO generation latency"""
    return SEO_LATENCY.time()
```
file: ./metrics.py

CI/CD Implementation
GitHub Actions Workflow
```
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov flake8
        pip install -r requirements.txt
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    - name: Test with pytest
      run: |
        pytest --cov=./ --cov-report=xml
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    - name: Login to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ secrets.DOCKER_REGISTRY }}
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    - name: Build and push Chat Service
      uses: docker/build-push-action@v4
      with:
        context: ./chat-service
        push: true
        tags: ${{ secrets.DOCKER_REGISTRY }}/chat-service:latest
    - name: Build and push SEO Service
      uses: docker/build-push-action@v4
      with:
        context: ./seo-service
        push: true
        tags: ${{ secrets.DOCKER_REGISTRY }}/seo-service:latest
    - name: Build and push API Gateway
      uses: docker/build-push-action@v4
      with:
        context: ./api-gateway
        push: true
        tags: ${{ secrets.DOCKER_REGISTRY }}/api-gateway:latest
    - name: Build and push Knowledge Service
      uses: docker/build-push-action@v4
      with:
        context: ./knowledge-service
        push: true
        tags: ${{ secrets.DOCKER_REGISTRY }}/knowledge-service:latest
    - name: Build and push Video Service
      uses: docker/build-push-action@v4
      with:
        context: ./video-service
        push: true
        tags: ${{ secrets.DOCKER_REGISTRY }}/video-service:latest

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Kubernetes Tools
      uses: azure/setup-kubectl@v3
    - name: Set Kubernetes Context
      uses: azure/k8s-set-context@v3
      with:
        kubeconfig: ${{ secrets.KUBE_CONFIG }}
    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f k8s/namespace.yaml
        kubectl apply -f k8s/
```
file: .github/workflows/ci-cd.yml

1. A/B Testing for SEO Content
```
import sqlite3
import random
import uuid
from datetime import datetime

class ABTesting:
    def __init__(self, db_path="ab_testing.db"):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ab_experiments (
            id TEXT PRIMARY KEY,
            name TEXT,
            created_at TIMESTAMP
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ab_variants (
            id TEXT PRIMARY KEY,
            experiment_id TEXT,
            name TEXT,
            content TEXT,
            impressions INTEGER DEFAULT 0,
            clicks INTEGER DEFAULT 0,
            conversions INTEGER DEFAULT 0,
            FOREIGN KEY (experiment_id) REFERENCES ab_experiments(id)
        )
        ''')

        conn.commit()
        conn.close()

    def create_experiment(self, name, variants):
        """Create a new A/B test experiment with variants"""
        experiment_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO ab_experiments (id, name, created_at) VALUES (?, ?, ?)",
            (experiment_id, name, datetime.now())
        )

        for variant_name, content in variants.items():
            variant_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO ab_variants (id, experiment_id, name, content) VALUES (?, ?, ?, ?)",
                (variant_id, experiment_id, variant_name, content)
            )

        conn.commit()
        conn.close()
        return experiment_id

    def get_random_variant(self, experiment_id):
        """Get a random variant from an experiment and increment impressions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, content FROM ab_variants WHERE experiment_id = ?",
            (experiment_id,)
        )

        variants = cursor.fetchall()
        if not variants:
            conn.close()
            return None

        variant = random.choice(variants)
        variant_id, variant_name, content = variant

        # Increment impressions
        cursor.execute(
            "UPDATE ab_variants SET impressions = impressions + 1 WHERE id = ?",
            (variant_id,)
        )

        conn.commit()
        conn.close()

        return {
            "id": variant_id,
            "name": variant_name,
            "content": content
        }

    def record_click(self, variant_id):
        """Record a click for a variant"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE ab_variants SET clicks = clicks + 1 WHERE id = ?",
            (variant_id,)
        )

        conn.commit()
        conn.close()

    def record_conversion(self, variant_id):
        """Record a conversion for a variant"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE ab_variants SET conversions = conversions + 1 WHERE id = ?",
            (variant_id,)
        )

        conn.commit()
        conn.close()

    def get_experiment_results(self, experiment_id):
        """Get the results of an experiment"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT name, impressions, clicks, conversions
        FROM ab_variants
        WHERE experiment_id = ?
        ''', (experiment_id,))

        results = []
        for row in cursor.fetchall():
            name, impressions, clicks, conversions = row
            ctr = (clicks / impressions) if impressions > 0 else 0
            cvr = (conversions / clicks) if clicks > 0 else 0

            results.append({
                "name": name,
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "ctr": ctr,
                "cvr": cvr
            })

        conn.close()
        return results
```
file: ab_testing.py

2. Advanced SEO Analytics Dashboard
```
import React, { useState, useEffect } from 'react';
import { Line, Bar, Pie } from 'react-chartjs-2';
import { Card, Row, Col, Table, Input, DatePicker, Button, Select } from 'antd';
import moment from 'moment';

const { RangePicker } = DatePicker;
const { Option } = Select;

const SEOAnalyticsDashboard = () => {
    const [analytics, setAnalytics] = useState({
        videoPerformance: [],
        keywordPerformance: [],
        titleEffectiveness: [],
        viewsOverTime: [],
        engagementMetrics: {}
    });
    const [dateRange, setDateRange] = useState([moment().subtract(30, 'days'), moment()]);
    const [selectedVideos, setSelectedVideos] = useState([]);
    const [videos, setVideos] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchVideos();
    }, []);

    useEffect(() => {
        if (selectedVideos.length > 0) {
            fetchAnalytics();
        }
    }, [selectedVideos, dateRange]);

    const fetchVideos = async () => {
        try {
            const response = await fetch('/api/videos');
            const data = await response.json();
            setVideos(data);
        } catch (error) {
            console.error('Error fetching videos:', error);
        }
    };

    const fetchAnalytics = async () => {
        setLoading(true);
        try {
            const [startDate, endDate] = dateRange;
            const response = await fetch('/api/analytics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    videoIds: selectedVideos,
                    startDate: startDate.format('YYYY-MM-DD'),
                    endDate: endDate.format('YYYY-MM-DD')
                })
            });

            const data = await response.json();
            setAnalytics(data);
        } catch (error) {
            console.error('Error fetching analytics:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleDateRangeChange = (dates) => {
        setDateRange(dates);
    };

    const handleVideoSelection = (value) => {
        setSelectedVideos(value);
    };

    return (
        <div className="seo-analytics-dashboard">
            <h1>YouTube SEO Analytics Dashboard</h1>

            <Card className="filters-card">
                <Row gutter={16}>
                    <Col span={12}>
                        <label>Select Videos:</label>
                        <Select
                            mode="multiple"
                            style={{ width: '100%' }}
                            placeholder="Select videos to analyze"
                            value={selectedVideos}
                            onChange={handleVideoSelection}
                        >
                            {videos.map(video => (
                                <Option key={video.id} value={video.id}>
                                    {video.title}
                                </Option>
                            ))}
                        </Select>
                    </Col>
                    <Col span={8}>
                        <label>Date Range:</label>
                        <RangePicker
                            value={dateRange}
                            onChange={handleDateRangeChange}
                        />
                    </Col>
                    <Col span={4}>
                        <Button
                            type="primary"
                            onClick={fetchAnalytics}
                            loading={loading}
                            style={{ marginTop: '24px' }}
                        >
                            Update Analytics
                        </Button>
                    </Col>
                </Row>
            </Card>

            <Row gutter={16} className="dashboard-row">
                <Col span={24}>
                    <Card title="Views Over Time" loading={loading}>
                        <Line
                            data={{
                                labels: analytics.viewsOverTime.map(item => item.date),
                                datasets: [
                                    {
                                        label: 'Views',
                                        data: analytics.viewsOverTime.map(item => item.views),
                                        borderColor: 'rgba(75, 192, 192, 1)',
                                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                    }
                                ]
                                    }
                                ]
                            }}
                            options={{
                                responsive: true,
                                scales: {
                                    x: {
                                        title: {
                                            display: true,
                                            text: 'Date'
                                        }
                                    },
                                    y: {
                                        title: {
                                            display: true,
                                            text: 'Views'
                                        },
                                        beginAtZero: true
                                    }
                                }
                            }}
                        />
                    </Card>
                </Col>
            </Row>

            <Row gutter={16} className="dashboard-row">
                <Col span={12}>
                    <Card title="Keyword Performance" loading={loading}>
                        <Bar
                            data={{
                                labels: analytics.keywordPerformance.map(item => item.keyword),
                                datasets: [
                                    {
                                        label: 'CTR (%)',
                                        data: analytics.keywordPerformance.map(item => item.ctr * 100),
                                        backgroundColor: 'rgba(153, 102, 255, 0.6)',
                                    },
                                    {
                                        label: 'Avg. Watch Time (min)',
                                        data: analytics.keywordPerformance.map(item => item.avgWatchTime / 60),
                                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                                    }
                                ]
                            }}
                            options={{
                                responsive: true,
                                scales: {
                                    y: {
                                        beginAtZero: true
                                    }
                                }
                            }}
                        />
                    </Card>
                </Col>
                <Col span={12}>
                    <Card title="Title Effectiveness" loading={loading}>
                        <Bar
                            data={{
                                labels: analytics.titleEffectiveness.map(item => item.title.substring(0, 20) + '...'),
                                datasets: [
                                    {
                                        label: 'Impressions',
                                        data: analytics.titleEffectiveness.map(item => item.impressions),
                                        backgroundColor: 'rgba(255, 159, 64, 0.6)',
                                    },
                                    {
                                        label: 'Clicks',
                                        data: analytics.titleEffectiveness.map(item => item.clicks),
                                        backgroundColor: 'rgba(255, 99, 132, 0.6)',
                                    }
                                ]
                            }}
                            options={{
                                responsive: true,
                                scales: {
                                    y: {
                                        beginAtZero: true
                                    }
                                }
                            }}
                        />
                    </Card>
                </Col>
            </Row>

            <Row gutter={16} className="dashboard-row">
                <Col span={8}>
                    <Card title="Engagement Metrics" loading={loading}>
                        <Pie
                            data={{
                                labels: ['Likes', 'Comments', 'Shares', 'Saves'],
                                datasets: [
                                    {
                                        data: [
                                            analytics.engagementMetrics.likes || 0,
                                            analytics.engagementMetrics.comments || 0,
                                            analytics.engagementMetrics.shares || 0,
                                            analytics.engagementMetrics.saves || 0
                                        ],
                                        backgroundColor: [
                                            'rgba(255, 99, 132, 0.6)',
                                            'rgba(54, 162, 235, 0.6)',
                                            'rgba(255, 206, 86, 0.6)',
                                            'rgba(75, 192, 192, 0.6)'
                                        ]
                                    }
                                ]
                            }}
                        />
                    </Card>
                </Col>
                <Col span={16}>
                    <Card title="Video Performance" loading={loading}>
                        <Table
                            dataSource={analytics.videoPerformance}
                            rowKey="videoId"
                            pagination={false}
                            columns={[
                                {
                                    title: 'Video Title',
                                    dataIndex: 'title',
                                    key: 'title',
                                    render: text => text.length > 40 ? text.substring(0, 40) + '...' : text
                                },
                                {
                                    title: 'Views',
                                    dataIndex: 'views',
                                    key: 'views',
                                    sorter: (a, b) => a.views - b.views
                                },
                                {
                                    title: 'CTR (%)',
                                    dataIndex: 'ctr',
                                    key: 'ctr',
                                    render: value => (value * 100).toFixed(2) + '%',
                                    sorter: (a, b) => a.ctr - b.ctr
                                },
                                {
                                    title: 'Avg. Watch Time',
                                    dataIndex: 'avgWatchTime',
                                    key: 'avgWatchTime',
                                    render: value => {
                                        const minutes = Math.floor(value / 60);
                                        const seconds = Math.round(value % 60);
                                        return `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
                                    },
                                    sorter: (a, b) => a.avgWatchTime - b.avgWatchTime
                                },
                                {
                                    title: 'SEO Score',
                                    dataIndex: 'seoScore',
                                    key: 'seoScore',
                                    render: value => `${value}/100`,
                                    sorter: (a, b) => a.seoScore - b.seoScore
                                }
                            ]}
                        />
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default SEOAnalyticsDashboard;
```
file: ./src/dashboard.js

# Conclusion To clarify how the existing Chat WebUI structure will be integrated, here's a detailed explanation of what happens with each component:

Static Assets Integration
The static folder from the Chat WebUI contains essential frontend assets that will be handled as follows:

1. CSS and Fonts
static/css/
static/fonts/

# These will be moved to the new chat-service/static/ directory
KaTeX fonts and styling will be preserved for mathematical notation support
Font Awesome icons will be maintained for UI elements
The main styles.css will be extended to include new SEO-related UI components

2. JavaScript Libraries
static/js/

# All existing JavaScript libraries (KaTeX, highlight.js, PDF.js, etc.) will be retained to maintain the original chat functionality, The main scripts.js will be refactored to incorporate SEO-specific functionalities:
* SEO mode toggle
* YouTube keyword analysis
* Title/description generation interface
* Analytics dashboard integration
* The existing APIs for document handling (PDF, Word) will be preserved

3. Images and Icons

static/images/


# All existing icons will be retained and augmented with additional SEO-specific icons This ensures UI consistency between the original chat features and new SEO features

# HTML Templates
templates/index.html

# The main template will be enhanced to include new UI sections for SEO operations The existing chat interface will remain the primary interaction point New UI components will be added as expandable panels or tabs Will maintain responsive design for both desktop and mobile users

# Application Structure in New Architecture

chat-service/

* app.py (core Flask application from Chat WebUI)
* static/ (all original static assets)
* templates/ (original and new templates)

* routes/ (new folder for modular route handling)

* chat_routes.py (chat functionality)
* seo_routes.py (SEO functionality)

* services/ (new folder for business logic)

* model_service.py (LLM interactions)
* tool_service.py (search, YouTube, etc.)

seo-service/

* Contains the refactored YouTube SEO Generator functionality
* No UI components of its own (uses chat-service UI)

shared-frontend/

* New React components for SEO dashboards
* Integrated with the existing vanilla JS in Chat WebUI

# Integration Benefits This approach provides several advantages: reserves User Experience: Users familiar with Chat WebUI will still recognize the interface Minimizes Code Duplication: Reuses all existing CSS, JS libraries, and assets Modular Enhancement: Adds SEO capabilities without breaking existing functionality Progressive Deployment: Allows phased rollout of new features
