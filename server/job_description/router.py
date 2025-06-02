from fastapi import APIRouter
from server.middleware.authenticate import authenticate
from fastapi import Request
from server.job_description.controller import job_description_add
from server.job_description.dto.schema import JobDescriptionDTO
from fastapi import Request

router = APIRouter(prefix="/job-description", tags=["job-description"])





@router.post("/add")
@authenticate
async def add(request:Request,data: JobDescriptionDTO):
    return await job_description_add(request,data)
