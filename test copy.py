import sys
from crewai import Agent, Task
import os
from dotenv import load_dotenv
from crewai import Crew, Process
from langchain_openai import AzureChatOpenAI

load_dotenv()

print("API KEY:", os.getenv("AZURE_OPENAI_KEY"))
print("ENDPOINT:", os.getenv("AZURE_OPENAI_ENDPOINT"))
print("DEPLOYMENT:", os.getenv("AZURE_OPENAI_DEPLOYMENT"))

# Ensure all required vars are present
assert os.getenv("AZURE_OPENAI_KEY"), "Missing AZURE_OPENAI_KEY"
assert os.getenv("AZURE_OPENAI_ENDPOINT"), "Missing AZURE_OPENAI_ENDPOINT"
assert os.getenv("AZURE_OPENAI_DEPLOYMENT"), "Missing AZURE_OPENAI_DEPLOYMENT"
assert os.getenv("OPENAI_API_KEY"), "Missing OPENAI_API_KEY"


# SOLUTION 2: Alternative approach using CrewAI's LLM configuration
# If the above fails, try this approach:

# Alternative LLM configuration for CrewAI
from crewai.llm import LLM

# Configure CrewAI's LLM wrapper
crewai_llm = LLM(
    model="azure/gpt-4o-mini",  # Use azure prefix
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_VERSION", "2023-07-01-preview"),
    temperature=0.7
)

# Alternative agent configuration
researcher_alt = Agent(
    role='Senior Researcher',
    goal='Discover groundbreaking technologies',
    verbose=True,
    llm=crewai_llm,
    backstory='A curious mind fascinated by cutting-edge innovation and the potential to change the world, you know everything about tech.',
    allow_delegation=False
)

research_task_alt = Task(
    description='Identify the next big trend in AI',
    expected_output='5 paragraphs on the next big AI trend',
    agent=researcher_alt
)

tech_crew_alt = Crew(
    agents=[researcher_alt],
    tasks=[research_task_alt],
    process=Process.sequential,
    verbose=True
)

# Begin the task execution
try:
    print("Attempting primary approach...")
    raise Exception("adada")
    print("Success! Result:", result)
except Exception as e:
    print(f"Primary approach failed: {e}")
    print("Trying alternative approach...")
    try:
        result = tech_crew_alt.kickoff()
        print("Success with alternative! Result:", result)
    except Exception as e2:
        print(f"Alternative approach also failed: {e2}")
        print("\nTroubleshooting suggestions:")
        print("1. Check if your Azure OpenAI deployment is active")
        print("2. Verify your API key has proper permissions")
        print("3. Try upgrading CrewAI: pip install --upgrade crewai")
        print("4. Check if your deployment name matches exactly")