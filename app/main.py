from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

from .models import SummarizeRequest, SummarizeResponse
from .summarizer import TextSummarizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Text Summarization API",
    description="A microservice for text summarization using Hugging Face Transformers",
    version="1.0.0",
)

# CORS configuration to allow frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the summarizer on startup
summarizer = None

@app.on_event("startup")
async def startup_event():
    """Load the model when the app starts"""
    global summarizer
    logger.info("Loading summarization model...")
    start_time = time.time()
    summarizer = TextSummarizer()
    load_time = time.time() - start_time
    logger.info(f"Model loaded in {load_time:.2f} seconds")


@app.post("/summarize", response_model=SummarizeResponse, tags=["Summarization"])
async def summarize_text(request: SummarizeRequest):
    """
    Summarize the provided text
    
    - **text**: The text content to summarize
    - **max_length**: Maximum length of the summary (optional)
    - **min_length**: Minimum length of the summary (optional)
    """
    if not summarizer:
        raise HTTPException(status_code=503, detail="The summarization model is not loaded yet")
    
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    logger.info(f"Received summarization request: {len(request.text)} characters")
    
    try:
        result = summarizer.summarize(
            text=request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        
        logger.info(f"Summarization completed: {result['summary_length']} characters")
        return result
    
    except Exception as e:
        logger.error(f"Error during summarization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Summarization error: {str(e)}")


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": summarizer is not None}