from fastapi import APIRouter
from server.authentication.router import router as auth_router
from server.resume.router import router as resume_router
from server.job_description.router import router as jd_router

router = APIRouter(prefix="/v1", tags=["v1"])
router.include_router(auth_router)
router.include_router(resume_router)
router.include_router(jd_router)