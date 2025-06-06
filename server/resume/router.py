from fastapi import APIRouter
from server.middleware.authenticate import authenticate
from fastapi import Request
from fastapi import APIRouter, Request, UploadFile, File
from server.resume.controller import process_resume,tune_resume,generate_resume_controller
from server.resume.dto.schema import TuneResumeDTO,ResumeGenerateDTO
router = APIRouter(prefix="/resume", tags=["resume"])





@router.post("/upload")
@authenticate
async def upload_resume(request: Request, file: UploadFile = File(...)):
    return await process_resume(request, file)


@router.post("/tune")
@authenticate
async def match_resume(request:Request, data: TuneResumeDTO):
    return await tune_resume(request,data)

@router.post("/generate")
@authenticate
async def generate_resume(request:Request, data: ResumeGenerateDTO):
    return await generate_resume_controller(request,data)