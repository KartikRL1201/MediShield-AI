from fastapi import APIRouter
from app.api.v1 import auth, medicines, prescriptions, interactions, allergies, ai

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(medicines.router, prefix="/medicines", tags=["Medicines"])
api_router.include_router(prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"])
api_router.include_router(interactions.router, prefix="/interactions", tags=["Interactions"])
api_router.include_router(allergies.router, prefix="/allergies", tags=["Allergies"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI"])
