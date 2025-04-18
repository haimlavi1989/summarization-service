import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.summarizer import TextSummarizer


@pytest.fixture
def client():
    """Create a test client for the app."""
    return TestClient(app)


@pytest.fixture
def mock_summarizer():
    """Create a mock for the TextSummarizer."""
    with patch("app.main.summarizer") as mock:
        # Set up the mock to return a predictable response
        mock.summarize.return_value = {
            "summary": "This is a test summary.",
            "original_length": 100,
            "summary_length": 23
        }
        yield mock


def test_health_check(client):
    """Test the health check endpoint."""
    with patch("app.main.summarizer", None):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "model_loaded": False}
    
    with patch("app.main.summarizer", MagicMock()):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "model_loaded": True}


def test_summarize_endpoint_with_mock(client, mock_summarizer):
    """Test the summarize endpoint with a mocked summarizer."""
    # Test with valid input
    response = client.post(
        "/summarize",
        json={"text": "This is a test.", "max_length": 100, "min_length": 10}
    )
    
    assert response.status_code == 200
    assert response.json() == {
        "summary": "This is a test summary.",
        "original_length": 100,
        "summary_length": 23
    }
    
    # Test with empty text
    response = client.post(
        "/summarize",
        json={"text": "", "max_length": 100, "min_length": 10}
    )
    
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_summarize_endpoint_model_not_loaded(client):
    """Test the summarize endpoint when model is not loaded."""
    with patch("app.main.summarizer", None):
        response = client.post(
            "/summarize",
            json={"text": "This is a test.", "max_length": 100, "min_length": 10}
        )
        
        assert response.status_code == 503
        assert "not loaded" in response.json()["detail"].lower()


@pytest.mark.skip(reason="Requires actual model, use for local testing only")
def test_summarize_endpoint_integration(client):
    """Integration test for the summarize endpoint with the actual model."""
    # Set up the app to use the actual model
    from app.main import startup_event
    app.dependency_overrides = {}
    startup_event()
    
    # Test with valid input
    response = client.post(
        "/summarize",
        json={
            "text": "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language.",
            "max_length": 50,
            "min_length": 10
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["summary"] != ""
    assert data["original_length"] > 0
    assert data["summary_length"] > 0