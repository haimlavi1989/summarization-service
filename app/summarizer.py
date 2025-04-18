from transformers import pipeline


class TextSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        """
        Initialize the text summarizer with the specified model
        
        Args:
            model_name (str): The name of the model to use from Hugging Face
        """
        self.model_name = model_name
        # Load the summarization pipeline with the specified model
        self.summarizer = pipeline("summarization", model=model_name)
        
    def summarize(self, text, max_length=150, min_length=30):
        """
        Generate a summary of the provided text
        
        Args:
            text (str): The text to summarize
            max_length (int): The maximum length of the summary in tokens
            min_length (int): The minimum length of the summary in tokens
            
        Returns:
            dict: Dictionary containing the summary and metadata
        """
        # Ensure text is not empty
        if not text or len(text.strip()) == 0:
            return {
                "summary": "",
                "original_length": 0,
                "summary_length": 0
            }
        
        # Generate the summary
        summary = self.summarizer(
            text, 
            max_length=max_length, 
            min_length=min_length, 
            do_sample=False
        )
        
        # Extract the summary text from the result
        summary_text = summary[0]['summary_text'] if summary else ""
        
        return {
            "summary": summary_text,
            "original_length": len(text),
            "summary_length": len(summary_text)
        }