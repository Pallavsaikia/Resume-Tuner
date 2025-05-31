from crewai.project import CrewBase
from crewai.llm import LLM
from crewai.agent import Agent
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import json
@CrewBase
class ResumeTuningCrew:
    def __init__(self, llm: LLM):
        self.llm = llm
    @agent
    def resume_analyst_agent(self):
        return Agent(
            role="Resume Tuner",
            goal="Tune the given resume to the given Job description so that its easy to pass auto ATS filter and HRs",
            backstory="""You are an expert resume analyst with over 10 years of experience in recruitment 
            and career coaching. You have a keen eye for identifying what makes a resume stand out and 
            what might hold it back. You understand current hiring trends and ATS systems. 
            Respond should be similar  structure to the json that we get for resume.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

   
    @task
    def job_matching_task(self):
        return Task(
            description="""Compare the resume against the target job description and identify matches and gaps.
            
            Resume Data: {resume}
            Job Description: {job_description}
            User Comment: {comment}
            
            Create a  resume in the same json structure focusing more in skills in common .Remove irrelevant skills
            Work experience tune it to more inclined version to the JD
            Humanize the text
            Dont fake experience but at the same time be soft on skills.Take into account what user wants.
            
            Response in the json format we get as input for resume""",
            expected_output="Strictly Json Response.A fine tuned Resume with updated objective and skills and fine tuned work experience that increases the chances of passing HR and ATS for the JD.",
            agent=self.resume_analyst_agent()
        )

    @crew
    def crew(self):
        return Crew(
            agents=[
                self.resume_analyst_agent(),
            ],
            tasks=[
                self.job_matching_task(),
            ],
            process=Process.sequential,
            verbose=True
        )
