from tortoise import fields
from tortoise.models import Model
from server.users.models import User
from server.job_description.models import JobDescription  # Adjust the import as needed
from typing import Optional, Dict, Any
from enum import Enum

class ResumeType(str, Enum):
    UPLOADED = "uploaded"
    GENERATED = "generated"


class Resume(Model):
    id = fields.IntField(pk=True)
    file_path = fields.CharField(max_length=255, null=True)
    comment = fields.TextField(null=True, description="Optional long-form comment about the resume")
    resume_type = fields.CharEnumField(
        ResumeType,
        default=ResumeType.UPLOADED,
        description="Whether the resume was uploaded or generated"
    )

    extracted_data: Optional[Dict[str, Any]] = fields.JSONField(
        null=True, description="Extracted structured details from the resume"
    )

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="resumes", on_delete=fields.CASCADE
    )

    job_description: fields.ForeignKeyRelation[JobDescription] = fields.ForeignKeyField(
        "models.JobDescription", related_name="resumes", null=True, on_delete=fields.SET_NULL
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "resume"

    def __str__(self):
        return f"Resume({self.file_path})"
