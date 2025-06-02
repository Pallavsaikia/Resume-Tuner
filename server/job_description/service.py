# server/resume/service.py
from server.job_description.models import JobDescription
from ai.agents.resume_tuner_agent import ResumeTuningCrew

class JobDescriptionService:
    @staticmethod
    async def add_job_description(user_id:int,job_description:str,company_name):
        return await JobDescription.create(
            user_id=user_id,
            job_description=job_description,
            company_name=company_name
        )