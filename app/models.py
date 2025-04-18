from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    text: str = Field(..., description="The text to summarize")
    max_length: int = Field(150, description="Maximum length of the summary")
    min_length: int = Field(30, description="Minimum length of the summary")
    
    class Config:
        schema_extra = {
            "example": {
                "text": "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data. The goal is a computer capable of understanding the contents of documents, including the contextual nuances of the language within them. The technology can then accurately extract information and insights contained in the documents as well as categorize and organize the documents themselves.",
                "max_length": 100,
                "min_length": 30
            }
        }


class SummarizeResponse(BaseModel):
    summary: str = Field(..., description="The generated summary")
    original_length: int = Field(..., description="Character count of the original text")
    summary_length: int = Field(..., description="Character count of the summary")