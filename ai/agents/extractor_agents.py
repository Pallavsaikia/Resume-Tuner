from crewai.llm import LLM
from crewai.agent import Agent
from ai.tools.extract_resume import ExtractResumeFieldTool


class ExtractorAgent:
    def __init__(self,llm:LLM):
        self.agent=Agent(
            role='Resume Data Extractor',
            goal='Extract the dat with tools at disposal to extract resume data',
            verbose=True,
            llm=llm,
            tools=[ExtractResumeFieldTool()],
            backstory='you are a expert in extracting resume data',
            allow_delegation=False
        )
        
    def get_agent(self)->Agent:
        return self.agent