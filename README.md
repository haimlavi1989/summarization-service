# Text Summarization Microservice

A RESTful API service that provides text summarization using Hugging Face's Transformers library with the BART model.

## Project Structure

```
summarization-service/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI application
│   ├── models.py           # Pydantic models for request/response
│   └── summarizer.py       # Summarization logic
├── tests/
│   ├── __init__.py
│   ├── test_api.py         # API tests
│   └── test_summarizer.py  # Summarizer module tests
├── Dockerfile
├── requirements.txt
└── README.md
```

## Technology Stack

- **FastAPI**: Modern, high-performance web framework for building APIs
- **Hugging Face Transformers**: State-of-the-art NLP library providing pre-trained models
- **BART Model**: facebook/bart-large-cnn - trained for text summarization tasks
- **Pytest**: Testing framework for unit and integration tests
- **Docker**: Container platform for easy deployment and scalability

## Features

- RESTful API with one main endpoint (`POST /summarize`) for text summarization
- Health check endpoint (`GET /health`) for monitoring service status
- Configurable summary length parameters
- Response includes original text length and summary length metrics
- Comprehensive API documentation with OpenAPI/Swagger

## Installation & Setup

### Local Development Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd summarization-service
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the service:
   ```
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Docker Setup

1. Build the Docker image:
   ```
   docker build -t summarization-service .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 summarization-service
   ```

The API will be available at `http://localhost:8000`

## API Usage

### Summarize Text

**Endpoint:** `POST /summarize`

**Request Body:**
```json
{
  "text": "Your long text to summarize goes here...",
  "max_length": 150,
  "min_length": 30
}
```

**Response:**
```json
{
  "summary": "The generated summary of your text.",
  "original_length": 1200,
  "summary_length": 120
}
```

### Check Health

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## API Documentation

Once the service is running, you can access the Swagger/OpenAPI documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run the test suite:
```
pytest
```

Some tests are marked with `@pytest.mark.skip` because they require downloading the model. To run these tests:
```
pytest --no-skip
```

## Performance Considerations

- The first request may take longer as the model needs to be loaded into memory.
- The BART model requires significant memory (~1.6GB), so ensure your deployment environment has sufficient resources.
- Consider using a smaller model or quantized models for resource-constrained environments.

## Future Improvements

- Add caching for frequently requested summaries
- Implement rate limiting
- Add authentication for API access
- Support for multiple summarization models
- Implement asynchronous processing for long texts
