from typing import List, Optional, Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class WorkItem(BaseModel):
    timespan: Optional[str] = Field(None, description="Duration or time period (e.g., '2020-2022', 'Jan 2021 - Present')")
    designation: str = Field(..., description="Designation of the work experience")
    description: Optional[str] = Field(None, description="description of work done in the experience")
    company_name: str = Field(..., description="Name of the company for the experience.Usually along with designation")

class ProjectItem(BaseModel):
    name: Optional[str] = Field(None, description="Name of the project")
    description: Optional[str] = Field(None, description="Work done in the project as text")

class ExtractResumeFieldToolSchema(BaseModel):
    firstname: Optional[str] = Field(None, description="First name from resume")
    lastname: Optional[str] = Field(None, description="Last name from resume")
    middlename: Optional[str] = Field(None, description="Middle name from resume")
    linkedin_url: Optional[str] = Field(None, description="URL of LinkedIn profile from resume")
    github_url: Optional[str] = Field(None, description="URL of GitHub profile from resume")
    email: Optional[str] = Field(None, description="Email address from resume")
    skills: List[str] = Field(..., description="Skills/Tools/Libraries from resume")
    work_experience: Optional[List[WorkItem]] = Field(default_factory=list, description="Work experience entries with designation,timespan and description")
    projects: Optional[List[ProjectItem]] = Field(default_factory=list, description="Project entries from resume")
    certifications: Optional[List[str]] = Field(default_factory=list, description="certification entries from resume")
   
class ExtractResumeFieldTool(BaseTool):
    name: str = "extract_resume_data"
    description: str = "Extracts specified fields from a resume."
    args_schema: Type[BaseModel] = ExtractResumeFieldToolSchema
   
    class Config:
        arbitrary_types_allowed = True
        check_fields = False
   
    def _run(self, **kwargs) -> dict:
        # Handle data preprocessing before validation
        processed_kwargs = self._preprocess_data(kwargs)
        validated_data = ExtractResumeFieldToolSchema(**processed_kwargs)
        result = validated_data.model_dump()
        
        print("Running extraction with result:", result)
        return result
    
    def _preprocess_data(self, data: dict) -> dict:
        """Preprocess data to handle field mapping"""
        processed = data.copy()
        
        # Handle projects field mapping
        if 'projects' in processed and processed['projects']:
            projects_list = []
            for item in processed['projects']:
                if isinstance(item, dict):
                    # Map title to name if title exists and name doesn't
                    if 'title' in item and 'name' not in item:
                        item['name'] = item['title']
                    projects_list.append(item)
            processed['projects'] = projects_list
        
        return processed