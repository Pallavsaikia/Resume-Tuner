# server/resume/controller.py

import os
import uuid
import asyncio
import json
from fastapi import UploadFile, Request
from sse_starlette.sse import EventSourceResponse
from config import AppConfig, ConfigKeys
from server.resume.dto.schema import TuneResumeDTO,ResumeGenerateDTO
# server/resume/controller.py

from fastapi import Request, UploadFile
from server.resume.service import ResumeService


async def process_resume(request: Request, file: UploadFile):
    user_id = request.state.user_id
    content = await file.read()
    file_path, filename = ResumeService.get_upload_path(file)
    return await ResumeService.generate_resume_events(user_id, file_path, content, filename)


async def tune_resume(request:Request, data: TuneResumeDTO):
    return await ResumeService.tune_resume_events(request.state.user_id,data.resume_id,data.job_description_id,data.comment)


async def generate_resume_controller(request:Request, data: ResumeGenerateDTO):
    return await ResumeService.generate_resume_service(request.state.user_id,data.resume_id)