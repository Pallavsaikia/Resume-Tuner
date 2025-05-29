# server/resume/service.py

import os
import uuid
import json
import asyncio
from fastapi import UploadFile
from config import AppConfig, ConfigKeys
from dataclasses import asdict  
import fitz  # PyMuPDF for PDF
import docx  # python-docx for DOCX
from sse_starlette.sse import EventSourceResponse
from ai.crew.extractor_resume_crew import ExtractResumeDataCrewSequential
from ai.agents.extractor_agents import  ExtractorAgent
from ai.llm.azure_open_ai import get_azure_open_ai_llm
from ai.tasks.extract_resume_task import ExtractResumeTask
from server.resume.models import Resume,ResumeType
import ast

class ResumeService:
    @staticmethod
    def get_upload_path(file: UploadFile):
        upload_dir = AppConfig.get(ConfigKeys.UPLOAD_DIR)
        if not upload_dir:
            raise ValueError("UPLOAD_DIR is not configured")

        os.makedirs(upload_dir, exist_ok=True)

        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(upload_dir, unique_filename)
        return file_path, unique_filename

    @staticmethod
    def save_file(file_path: str, content: bytes):
        with open(file_path, "wb") as f:
            f.write(content)

    @staticmethod
    def extract_text_from_resume(file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            return ResumeService.extract_text_from_pdf(file_path)
        elif ext == ".docx":
            return ResumeService.extract_text_from_docx(file_path)
        elif ext == ".txt":
            return ResumeService.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()

    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()

    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    @staticmethod
    def safe_json_parse(extracted_json_data:str):
        try:
            # First, check if it's already a dictionary
            if isinstance(extracted_json_data, dict):
                print("Data is already a dictionary")
                pass  # already parsed
            elif isinstance(extracted_json_data, str):
                # Try parsing as JSON first
                try:
                    extracted_json_data = json.loads(extracted_json_data)
                    print("Successfully parsed as JSON")
                except json.JSONDecodeError:
                    # If JSON parsing fails, try using ast.literal_eval for Python dict strings
                    try:
                        extracted_json_data = ast.literal_eval(extracted_json_data)
                        print("Successfully parsed as Python literal")
                    except (ValueError, SyntaxError) as e:
                        print(f"Failed to parse as Python literal: {e}")
                        # As a last resort, try eval (use with caution in production)
                        try:
                            extracted_json_data = eval(extracted_json_data)
                            print("Successfully parsed using eval")
                        except Exception as e:
                            print(f"Failed to parse using eval: {e}")
                            extracted_json_data = {}
            else:
                print(f"Unexpected data type: {type(extracted_json_data)}")
                extracted_json_data = None
                
        except Exception as e:
            print(f"General parsing error: {e}")
            extracted_json_data = None
            
        return extracted_json_data
    
    @staticmethod
    async def generate_resume_events(user_id: str, file_path: str, content: bytes, filename: str):


        async def event_generator():
            try:
                # Uploading
                yield f"event: status\ndata: {json.dumps({'step': 'uploading', 'message': 'Uploading file...'})}\n\n"
                ResumeService.save_file(file_path, content)


                # Parsing
                yield f"event: status\ndata: {json.dumps({'step': 'parsing', 'message': 'Parsing resume...'})}\n\n"
                
                text_content = ResumeService.extract_text_from_resume(file_path)
                print(text_content)
                # Extracting
                yield f"event: status\ndata: {json.dumps({'step': 'extracting', 'message': 'Extracting data...'})}\n\n"
                # await asyncio.sleep(1.5)
                llm=get_azure_open_ai_llm()
                extractor_agent=ExtractorAgent(llm).get_agent()
                
                crew=ExtractResumeDataCrewSequential(agents=[extractor_agent],tasks=[ExtractResumeTask.get_task(extractor_agent,text_content)]
                                                     ,verbose=False)
                extracted_data=crew.kickoff()
                print(extracted_data)
                
                extracted_json_data=extracted_data.raw
                print(type(extracted_json_data))
                extracted_json=ResumeService.safe_json_parse(extracted_json_data)
                if extracted_json is None:
                    raise Exception("Bad json")

                filename_only = os.path.basename(file_path)     
                new_resume = await Resume.create(
                    file_path=filename_only,
                    extracted_data= extracted_json,
                    resume_type=ResumeType.UPLOADED,  # or ResumeType.GENERATED
                    user_id=user_id
                )
                result = {
                    "status": "success",
                    "user_id": user_id,
                    "filename": filename,
                    "message": "Resume processed successfully",
                    "text_snippet": str(new_resume)  # first 500 chars as sample
                }
                yield f"event: done\ndata: {json.dumps(result)}\n\n"

            except Exception as e:
                yield f"event: error\ndata: {json.dumps({'message': str(e)})}\n\n"

        return EventSourceResponse(event_generator())
