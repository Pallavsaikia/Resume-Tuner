# server/resume/controller.py

import os
import uuid
import asyncio
import json
from fastapi import UploadFile, Request
from sse_starlette.sse import EventSourceResponse
from config import AppConfig, ConfigKeys
from server.resume.dto.schema import TuneResumeDTO
# server/resume/controller.py

from fastapi import Request, UploadFile
from server.job_description.service import JobDescriptionService
from server.job_description.dto.schema import JobDescriptionDTO



async def job_description_add(request:Request,data: JobDescriptionDTO):
    return await JobDescriptionService.add_job_description(request.state.user_id,data.job_description,data.company_name)
