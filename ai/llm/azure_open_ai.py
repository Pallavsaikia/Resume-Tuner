from crewai.llm import LLM
import os 

def get_azure_open_ai_llm(temperature=0.7)->LLM:
    return LLM(
        model="azure/"+os.getenv("AZURE_OPENAI_DEPLOYMENT"),  # Use azure prefix
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_VERSION", "2023-07-01-preview"),
        temperature=temperature
    )