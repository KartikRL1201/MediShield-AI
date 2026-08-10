from google import genai
from google.genai import types
from app.core.config import settings
from app.schemas.prescription import OCRResult
from app.services.nlp_parser import parse_prescription_text

async def process_prescription(file_bytes: bytes, mime_type: str) -> OCRResult:
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing from environment variables.")

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    # 1. We strictly tell Gemini to ONLY extract text, no JSON or structuring.
    prompt = """
    You are an expert OCR scanner. Analyze this image and extract all the text you see.
    Do not format the text. Do not return JSON. Just return the raw text exactly as it appears in the image, line by line.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=[
                types.Part.from_bytes(
                    data=file_bytes,
                    mime_type=mime_type,
                ),
                prompt
            ]
        )
        
        raw_ocr_text = response.text.strip()
        
        # 2. Pass the raw string to our non-LLM NLP parser to do the actual brain work
        final_result = parse_prescription_text(raw_ocr_text)
        
        return final_result
        
    except Exception as e:
        print(f"Error calling Gemini or NLP Parser: {e}")
        raise ValueError(f"Failed to process the prescription: {str(e)}")
