from crewai.crew import Crew,CrewOutput
from crewai.agent import Agent
from crewai.task import Task
from crewai import Crew, Process

class ExtractResumeDataCrewSequential:

    def __init__(self, agents:list[Agent],tasks=list[Task],verbose=False):
        self.crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=verbose
        )

    def get_crew(self)->Crew:
        return self.crew
    
    def kickoff(self)->CrewOutput:
        return self.crew.kickoff()