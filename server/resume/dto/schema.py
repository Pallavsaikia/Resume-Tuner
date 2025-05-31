from pydantic import BaseModel

class TuneResumeDTO(BaseModel):
    resume_id: int
    job_description: str
    comment:str