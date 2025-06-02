from pydantic import BaseModel

class JobDescriptionDTO(BaseModel):
    company_name: str
    job_description: str