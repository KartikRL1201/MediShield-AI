from fastapi import APIRouter
from app.api.v1 import auth, medicines, prescriptions

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(medicines.router, prefix="/medicines", tags=["medicines"])
api_router.include_router(prescriptions.router, prefix="/prescriptions", tags=["prescriptions"])
