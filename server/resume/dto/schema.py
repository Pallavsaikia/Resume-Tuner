from pydantic import BaseModel

class TuneResumeDTO(BaseModel):
    resume_id: int
    job_description_id: int
    comment:str