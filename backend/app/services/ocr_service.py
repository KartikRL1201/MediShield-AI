from google import genai
from google.genai import types
from app.core.config import settings
from app.schemas.prescription import OCRResult
import json

async def process_prescription(file_bytes: bytes, mime_type: str) -> OCRResult:
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing from environment variables.")

    # Initialize the new genai client
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    prompt = """
    You are an expert medical AI assistant. Analyze this prescription image or document.
    Extract every medication listed.
    
    Return the data strictly as a JSON object matching this schema:
    {
      "medicines": [
        {
          "name": "Medicine Name",
          "dosage": "500mg",
          "frequency": "Twice a day",
          "duration": "7 days"
        }
      ]
    }
    
    Do not include any markdown formatting, backticks, or conversational text. Return raw JSON only.
    """
    
    try:
        # Pass the raw bytes to the new Gemini Vision API
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[
                types.Part.from_bytes(
                    data=file_bytes,
                    mime_type=mime_type,
                ),
                prompt
            ]
        )
        
        # Parse the JSON response
        text_response = response.text.strip()
        if text_response.startswith('```json'):
            text_response = text_response[7:-3].strip()
        elif text_response.startswith('```'):
            text_response = text_response[3:-3].strip()
            
        json_data = json.loads(text_response)
        
        # Map to Pydantic schema
        return OCRResult(**json_data)
        
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        # In a real app, we might want to log this securely.
        raise ValueError("Failed to extract data from the prescription. The image might be too blurry.")
