
from crewai.task import Task 
from crewai.agent import Agent

class ExtractResumeTask:
    @staticmethod
    def get_task(agent:Agent,resume_text):
        return Task(
            description=f'Here is the resume data please extract the necessary information.\n{resume_text}',
            expected_output='Let us know whats missing',
            agent=agent
        )