
import pytest
from app.summarizer import TextSummarizer


def test_summarizer_initialization():
    """Test that the summarizer initializes correctly with a valid model name."""
    summarizer = TextSummarizer(model_name="facebook/bart-large-cnn")
    assert summarizer is not None
    assert summarizer.model_name == "facebook/bart-large-cnn"


def test_summarize_empty_text():
    """Test summarization with empty text."""
    summarizer = TextSummarizer()
    result = summarizer.summarize("")
    
    assert result["summary"] == ""
    assert result["original_length"] == 0
    assert result["summary_length"] == 0


@pytest.mark.skip(reason="Requires model download, use for local testing only")
def test_summarize_valid_text():
    """Test summarization with valid text."""
    summarizer = TextSummarizer()
    
    test_text = "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data."
    
    result = summarizer.summarize(test_text, max_length=50, min_length=10)
    
    assert result["summary"] != ""
    assert result["original_length"] == len(test_text)
    assert result["summary_length"] > 0
    assert result["summary_length"] <= 50  # Should respect the max_length parameter