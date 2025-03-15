import json
import unittest.mock as mock

import pytest
import requests
from api_gateway.src.app import app  # Import the Flask app


def mock_response(status_code=200, json_data=None, text=None, headers=None):
    """Helper function to create a mock response object"""
    mock_resp = mock.MagicMock()
    mock_resp.status_code = status_code
    mock_resp.raise_for_status = mock.MagicMock()
    if status_code >= 400:
        mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError()
    if json_data is not None:
        mock_resp.json.return_value = json_data
    if text is not None:
        mock_resp.text = text
        mock_resp.iter_content.return_value = [text.encode("utf-8")]
    mock_resp.headers = headers or {"Content-Type": "application/json"}
    return mock_resp


def test_chat_proxy_empty_message(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"response": "Message cannot be empty"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/chat", json={"message": ""})
        assert response.status_code == 200
        assert response.get_json() == {"response": "Message cannot be empty"}
        mock_post.assert_called_with(
            "http://chat-service:5000/api/chat", json={"message": ""}, stream=True
        )


def test_chat_proxy_long_message(test_client):
    with mock.patch("requests.post") as mock_post:
        long_message = "x" * 1000
        response_data = {"response": "Message processed"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/chat", json={"message": long_message})
        assert response.status_code == 200
        assert response.get_json() == {"response": "Message processed"}
        mock_post.assert_called_with(
            "http://chat-service:5000/api/chat", json={"message": long_message}, stream=True
        )


def test_chat_proxy_special_characters(test_client):
    with mock.patch("requests.post") as mock_post:
        special_message = "!@#$%^&*()"
        response_data = {"response": "Special characters handled"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/chat", json={"message": special_message})
        assert response.status_code == 200
        assert response.get_json() == {"response": "Special characters handled"}
        mock_post.assert_called_with(
            "http://chat-service:5000/api/chat", json={"message": special_message}, stream=True
        )


def test_chat_proxy_missing_message(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"error": "Message field is required"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/chat", json={})
        assert response.status_code == 200
        assert response.get_json() == {"error": "Message field is required"}
        mock_post.assert_called_with("http://chat-service:5000/api/chat", json={}, stream=True)


def test_chat_proxy_unicode_message(test_client):
    with mock.patch("requests.post") as mock_post:
        unicode_message = "Hello 世界"
        response_data = {"response": "Unicode message processed"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/chat", json={"message": unicode_message})
        assert response.status_code == 200
        assert response.get_json() == {"response": "Unicode message processed"}
        mock_post.assert_called_with(
            "http://chat-service:5000/api/chat", json={"message": unicode_message}, stream=True
        )


def test_chat_proxy_numeric_message(test_client):
    with mock.patch("requests.post") as mock_post:
        numeric_message = "12345"
        response_data = {"response": "Numeric message processed"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/chat", json={"message": numeric_message})
        assert response.status_code == 200
        assert response.get_json() == {"response": "Numeric message processed"}
        mock_post.assert_called_with(
            "http://chat-service:5000/api/chat", json={"message": numeric_message}, stream=True
        )


def test_chat_proxy_whitespace_message(test_client):
    with mock.patch("requests.post") as mock_post:
        whitespace_message = "   "
        response_data = {"response": "Whitespace-only message"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/chat", json={"message": whitespace_message})
        assert response.status_code == 200
        assert response.get_json() == {"response": "Whitespace-only message"}
        mock_post.assert_called_with(
            "http://chat-service:5000/api/chat", json={"message": whitespace_message}, stream=True
        )


def test_chat_proxy(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"response": "Mocked chat response"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/chat", json={"message": "Test message"})
        assert response.status_code == 200
        assert response.get_json() == {"response": "Mocked chat response"}
        mock_post.assert_called_with(
            "http://chat-service:5000/api/chat", json={"message": "Test message"}, stream=True
        )


def test_seo_generate_proxy(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"title": "Mocked SEO title"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/seo/generate", json={"keyword": "test"})
        assert response.status_code == 200
        assert response.get_json() == {"title": "Mocked SEO title"}
        mock_post.assert_called_with(
            "http://seo-service:5001/generate", json={"keyword": "test"}, stream=True
        )


def test_seo_generate_proxy_empty_keyword(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"error": "Keyword cannot be empty"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/seo/generate", json={"keyword": ""})
        assert response.status_code == 200
        assert response.get_json() == {"error": "Keyword cannot be empty"}
        mock_post.assert_called_with(
            "http://seo-service:5001/generate", json={"keyword": ""}, stream=True
        )


def test_knowledge_ingest_proxy(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"status": "success"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/knowledge/ingest", json={"data": "test"})
        assert response.status_code == 200
        assert response.get_json() == {"status": "success"}
        mock_post.assert_called_with(
            "http://knowledge-service:5002/ingest", json={"data": "test"}, stream=True
        )


def test_knowledge_ingest_proxy_large_data(test_client):
    with mock.patch("requests.post") as mock_post:
        large_data = "x" * 10000
        response_data = {"status": "Large data processed"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/knowledge/ingest", json={"data": large_data})
        assert response.status_code == 200
        assert response.get_json() == {"status": "Large data processed"}
        mock_post.assert_called_with(
            "http://knowledge-service:5002/ingest", json={"data": large_data}, stream=True
        )


def test_knowledge_query_proxy(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"results": "Mocked query results"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/knowledge/query", json={"query": "test"})
        assert response.status_code == 200
        assert response.get_json() == {"results": "Mocked query results"}
        mock_post.assert_called_with(
            "http://knowledge-service:5002/query", json={"query": "test"}, stream=True
        )


def test_knowledge_query_proxy_empty_query(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"error": "Query cannot be empty"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/knowledge/query", json={"query": ""})
        assert response.status_code == 200
        assert response.get_json() == {"error": "Query cannot be empty"}
        mock_post.assert_called_with(
            "http://knowledge-service:5002/query", json={"query": ""}, stream=True
        )


def test_video_process_proxy(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"status": "success"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        data = {"video": "test"}
        response = test_client.post(
            "/api/video/process", data=data, content_type="multipart/form-data"
        )
        assert response.status_code == 200
        assert response.get_json() == {"status": "success"}
        mock_post.assert_called_with(
            "http://video-service:5003/process-video", data=data, stream=True
        )


def test_video_process_proxy_invalid_format(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"error": "Invalid video format"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        data = {"video": "invalid"}
        response = test_client.post(
            "/api/video/process", data=data, content_type="multipart/form-data"
        )
        assert response.status_code == 200
        assert response.get_json() == {"error": "Invalid video format"}
        mock_post.assert_called_with(
            "http://video-service:5003/process-video", data=data, stream=True
        )


def test_video_upload_proxy(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"status": "success"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/video/upload", json={"data": "test"})
        assert response.status_code == 200
        assert response.get_json() == {"status": "success"}
        mock_post.assert_called_with(
            "http://video-service:5003/upload-to-youtube", json={"data": "test"}, stream=True
        )


def test_video_upload_proxy_missing_data(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"error": "Missing video data"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/video/upload", json={})
        assert response.status_code == 200
        assert response.get_json() == {"error": "Missing video data"}
        mock_post.assert_called_with(
            "http://video-service:5003/upload-to-youtube", json={}, stream=True
        )


def test_video_upload_proxy_large_file(test_client):
    with mock.patch("requests.post") as mock_post:
        large_data = "x" * 1000000
        response_data = {"status": "Large file processed"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/video/upload", json={"data": large_data})
        assert response.status_code == 200
        assert response.get_json() == {"status": "Large file processed"}
        mock_post.assert_called_with(
            "http://video-service:5003/upload-to-youtube", json={"data": large_data}, stream=True
        )


def test_video_upload_proxy_invalid_json(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"error": "Invalid JSON format"}
        mock_post.return_value = mock_response(
            status_code=400, json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post(
            "/api/video/upload", data="invalid json", content_type="application/json"
        )
        assert response.status_code == 400
        assert response.get_json() == {"error": "Invalid JSON format"}
        mock_post.assert_called_with(
            "http://video-service:5003/upload-to-youtube", data="invalid json", stream=True
        )


def test_video_upload_proxy_unicode_filename(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"status": "Unicode filename accepted"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post(
            "/api/video/upload", json={"data": "test", "filename": "视频.mp4"}
        )
        assert response.status_code == 200
        assert response.get_json() == {"status": "Unicode filename accepted"}
        mock_post.assert_called_with(
            "http://video-service:5003/upload-to-youtube",
            json={"data": "test", "filename": "视频.mp4"},
            stream=True,
        )


def test_video_upload_proxy_service_timeout(test_client):
    with mock.patch("requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.ConnectTimeout
        response = test_client.post("/api/video/upload", json={"data": "test"})
        assert response.status_code == 504
        assert response.get_json() == {"error": "Service timeout"}
        mock_post.assert_called_with(
            "http://video-service:5003/upload-to-youtube", json={"data": "test"}, stream=True
        )


def test_video_upload_proxy_unsupported_media_type(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"error": "Unsupported media type"}
        mock_post.return_value = mock_response(
            status_code=415, json_data=response_data, text=json.dumps(response_data)
        )
        response = test_client.post("/api/video/upload", data="test", content_type="text/plain")
        assert response.status_code == 415
        assert response.get_json() == {"error": "Unsupported media type"}
        mock_post.assert_called_with(
            "http://video-service:5003/upload-to-youtube", data="test", stream=True
        )


def test_generate_and_upload_workflow(test_client):
    with mock.patch("requests.post") as mock_post:
        seo_response_data = {
            "title": "Mocked SEO title",
            "description": "Mocked SEO description",
            "tags": ["tag1", "tag2"],
        }
        video_process_response_data = {"processed_file": "test_file.mp4"}
        video_upload_response_data = {"status": "success"}

        mock_post.side_effect = [
            mock_response(json_data=seo_response_data, text=json.dumps(seo_response_data)),
            mock_response(
                json_data=video_process_response_data, text=json.dumps(video_process_response_data)
            ),
            mock_response(
                json_data=video_upload_response_data, text=json.dumps(video_upload_response_data)
            ),
        ]

        data = {"keyword": "test", "video": "test"}
        response = test_client.post(
            "/api/workflow/generate-and-upload", data=data, content_type="multipart/form-data"
        )

        assert response.status_code == 200
        assert response.get_json() == {"status": "success"}
        mock_post.assert_any_call(
            "http://seo-service:5001/generate", json={"keyword": "test"}, stream=True
        )
        mock_post.assert_any_call(
            "http://video-service:5003/process-video", data={"video": "test"}, stream=True
        )
        mock_post.assert_any_call(
            "http://video-service:5003/upload-to-youtube",
            json={
                "video_file": "test_file.mp4",
                "title": "Mocked SEO title",
                "description": "Mocked SEO description",
                "tags": ["tag1", "tag2"],
            },
            stream=True,
        )


def test_generate_and_upload_workflow_invalid_keyword(test_client):
    with mock.patch("requests.post") as mock_post:
        response_data = {"error": "Invalid keyword"}
        mock_post.return_value = mock_response(
            json_data=response_data, text=json.dumps(response_data)
        )
        data = {"keyword": "", "video": "test"}
        response = test_client.post(
            "/api/workflow/generate-and-upload", data=data, content_type="multipart/form-data"
        )
        assert response.status_code == 200
        assert response.get_json() == {"error": "Invalid keyword"}
        mock_post.assert_called_with(
            "http://seo-service:5001/generate", json={"keyword": ""}, stream=True
        )


def test_generate_and_upload_workflow_large_video(test_client):
    with mock.patch("requests.post") as mock_post:
        large_video = "x" * 10000000
        seo_response_data = {
            "title": "Large Video Title",
            "description": "Large Video Description",
            "tags": ["large", "video"],
        }
        video_process_response_data = {"processed_file": "large_video.mp4"}
        video_upload_response_data = {"status": "success"}

        mock_post.side_effect = [
            mock_response(json_data=seo_response_data, text=json.dumps(seo_response_data)),
            mock_response(
                json_data=video_process_response_data, text=json.dumps(video_process_response_data)
            ),
            mock_response(
                json_data=video_upload_response_data, text=json.dumps(video_upload_response_data)
            ),
        ]

        data = {"keyword": "test", "video": large_video}
        response = test_client.post(
            "/api/workflow/generate-and-upload", data=data, content_type="multipart/form-data"
        )

        assert response.status_code == 200
        assert response.get_json() == {"status": "success"}
        mock_post.assert_any_call(
            "http://seo-service:5001/generate", json={"keyword": "test"}, stream=True
        )
        mock_post.assert_any_call(
            "http://video-service:5003/process-video", data={"video": large_video}, stream=True
        )
        mock_post.assert_any_call(
            "http://video-service:5003/upload-to-youtube",
            json={
                "video_file": "large_video.mp4",
                "title": "Large Video Title",
                "description": "Large Video Description",
                "tags": ["large", "video"],
            },
            stream=True,
        )


def test_generate_and_upload_workflow_special_chars_keyword(test_client):
    with mock.patch("requests.post") as mock_post:
        special_keyword = "!@#$%^&*()"
        seo_response_data = {
            "title": "Special Title",
            "description": "Special Description",
            "tags": ["special"],
        }
        video_process_response_data = {"processed_file": "special_video.mp4"}
        video_upload_response_data = {"status": "success"}

        mock_post.side_effect = [
            mock_response(json_data=seo_response_data, text=json.dumps(seo_response_data)),
            mock_response(
                json_data=video_process_response_data, text=json.dumps(video_process_response_data)
            ),
            mock_response(
                json_data=video_upload_response_data, text=json.dumps(video_upload_response_data)
            ),
        ]

        data = {"keyword": special_keyword, "video": "test"}
        response = test_client.post(
            "/api/workflow/generate-and-upload", data=data, content_type="multipart/form-data"
        )

        assert response.status_code == 200
        assert response.get_json() == {"status": "success"}
        mock_post.assert_any_call(
            "http://seo-service:5001/generate", json={"keyword": special_keyword}, stream=True
        )
        mock_post.assert_any_call(
            "http://video-service:5003/process-video", data={"video": "test"}, stream=True
        )
        mock_post.assert_any_call(
            "http://video-service:5003/upload-to-youtube",
            json={
                "video_file": "special_video.mp4",
                "title": "Special Title",
                "description": "Special Description",
                "tags": ["special"],
            },
            stream=True,
        )


def test_generate_and_upload_workflow_unicode_data(test_client):
    with mock.patch("requests.post") as mock_post:
        unicode_keyword = "测试关键词"
        seo_response_data = {
            "title": "Unicode Title 标题",
            "description": "Unicode Description 描述",
            "tags": ["unicode", "测试"],
        }
        video_process_response_data = {"processed_file": "unicode_video.mp4"}
        video_upload_response_data = {"status": "success"}

        mock_post.side_effect = [
            mock_response(json_data=seo_response_data, text=json.dumps(seo_response_data)),
            mock_response(
                json_data=video_process_response_data, text=json.dumps(video_process_response_data)
            ),
            mock_response(
                json_data=video_upload_response_data, text=json.dumps(video_upload_response_data)
            ),
        ]

        data = {"keyword": unicode_keyword, "video": "test"}
        response = test_client.post(
            "/api/workflow/generate-and-upload", data=data, content_type="multipart/form-data"
        )

        assert response.status_code == 200
        assert response.get_json() == {"status": "success"}
        mock_post.assert_any_call(
            "http://seo-service:5001/generate", json={"keyword": unicode_keyword}, stream=True
        )
        mock_post.assert_any_call(
            "http://video-service:5003/process-video", data={"video": "test"}, stream=True
        )
        mock_post.assert_any_call(
            "http://video-service:5003/upload-to-youtube",
            json={
                "video_file": "unicode_video.mp4",
                "title": "Unicode Title 标题",
                "description": "Unicode Description 描述",
                "tags": ["unicode", "测试"],
            },
            stream=True,
        )


def test_generate_and_upload_workflow_missing_video(test_client):
    with mock.patch("requests.post") as mock_post:
        seo_response_data = {
            "title": "Test Title",
            "description": "Test Description",
            "tags": ["test"],
        }
        mock_post.return_value = mock_response(
            json_data=seo_response_data, text=json.dumps(seo_response_data)
        )

        data = {"keyword": "test"}
        response = test_client.post(
            "/api/workflow/generate-and-upload", data=data, content_type="multipart/form-data"
        )

        assert response.status_code == 400
        assert response.get_json() == {"error": "Video file is required"}
        mock_post.assert_called_with(
            "http://seo-service:5001/generate", json={"keyword": "test"}, stream=True
        )


def test_generate_and_upload_workflow_unsupported_video_format(test_client):
    with mock.patch("requests.post") as mock_post:
        seo_response_data = {
            "title": "Test Title",
            "description": "Test Description",
            "tags": ["test"],
        }
        video_process_response_data = {"error": "Unsupported video format"}

        mock_post.side_effect = [
            mock_response(json_data=seo_response_data, text=json.dumps(seo_response_data)),
            mock_response(
                status_code=415,
                json_data=video_process_response_data,
                text=json.dumps(video_process_response_data),
            ),
        ]

        data = {"keyword": "test", "video": "test.txt"}
        response = test_client.post(
            "/api/workflow/generate-and-upload", data=data, content_type="multipart/form-data"
        )

        assert response.status_code == 415
        assert response.get_json() == {"error": "Unsupported video format"}
        mock_post.assert_any_call(
                text=json.dumps(video_process_response_data),
            ),
        ]

        data = {"keyword": "test", "video": "test.txt"}
        response = test_client.post(
            "/api/workflow/generate-and-upload", data=data, content_type="multipart/form-data"
        )

        assert response.status_code == 415
        assert response.get_json() == {"error": "Unsupported video format"}
        mock_post.assert_any_call(
            "http://seo-service:5001/generate", json={"keyword": "test"}, stream=True
        )
        mock_post.assert_any_call(
            "http://video-service:5003/process-video", data={"video": "test.txt"}, stream=True
        )
