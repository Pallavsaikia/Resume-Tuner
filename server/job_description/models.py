from tortoise import fields
from tortoise.models import Model
from server.users.models import User

class JobDescription(Model):
    id = fields.IntField(pk=True)
    job_description = fields.TextField(description="Full text of the job description")
    company_name = fields.CharField(max_length=255, description="Name of the company")
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="job_description", on_delete=fields.CASCADE
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "job_description"

    def __str__(self):
        return f"JobDescription({self.company_name})"
