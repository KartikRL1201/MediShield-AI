from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.prescription import OCRResult
from app.services.ocr_service import process_prescription

router = APIRouter()

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp", "application/pdf"]

@router.post("/upload", response_model=OCRResult)
async def upload_prescription(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Unified Prescription Processing API:
    Accepts an image, uses Gemini Vision solely for raw OCR text extraction, and then structures the data using our custom NLP engine.
    """
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {file.content_type}. Please upload a JPEG, PNG, WEBP, or PDF."
        )
        
    try:
        # Read the file directly into memory
        file_bytes = await file.read()
        
        # Pass to the unified AI & NLP engine
        result = await process_prescription(file_bytes, file.content_type)
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred while processing the prescription.")
