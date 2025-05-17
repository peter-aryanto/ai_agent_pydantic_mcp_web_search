Basic rules for python app

- always import os
- use load_dotenv to load environment variables from .env file
- if llm_setup.py does not exist, create it. It must contain the method below as an addition to all the above:
```python
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

def setup_llm(llm: str, llm_base_url: str, llm_api_key: str):
    """Setup the llm."""
    llm = llm || os.getenv("LLM", "gpt-4o-mini")
    llm_base_url = llm_base_url || os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    llm_api_key = llm_api_key || os.getenv("LLM_API_KEY", raise Exception("Missing LLM_API_KEY"))
    openai_provider = OpenAIProvider(
        base_url=llm_base_url,
        api_key=llm_api_key,
        # model=OpenAIModel(llm),
    )
    openai_model = OpenAIModel(llm, provider=openai_provider)
    return openai_model
```
- add the dependencies from all the above into requirements.txt
- if .env file does not exist, then create it
- add the template of environment variables based on all the above into .env file
- create a shell script named 'init_this' to run the following steps (note that this needs to work in linux, e.g. use python3 instead of python):
  - deactivate any conda environment
  - if venv directory does not exist, then create python virtual environment in venv, activate that virtual environment and run pip install -r requirements.txt
  - if venv directory exists and the virtual environment is not yet active, then just activate the virtual environment
- create a shell script named 'reset_this' to run the following steps:
  - deactivate any conda environment
  - deactivate any python virtual environment
  - remove the venv directory
