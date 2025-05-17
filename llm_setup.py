import os
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()

def setup_llm(llm: str = None, llm_base_url: str = None, llm_api_key: str = None):
    """Setup the llm."""
    llm = llm or os.getenv("LLM", "gpt-4o-mini")
    llm_base_url = llm_base_url or os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    llm_api_key = llm_api_key or os.getenv("LLM_API_KEY")
    
    if not llm_api_key:
        raise Exception("Missing LLM_API_KEY")
        
    openai_provider = OpenAIProvider(
        base_url=llm_base_url,
        api_key=llm_api_key,
    )
    openai_model = OpenAIModel(llm, provider=openai_provider)
    return openai_model
