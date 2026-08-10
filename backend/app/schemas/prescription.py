from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractedMedicine(BaseModel):
    name: str = Field(description="The brand or generic name of the medicine")
    dosage: Optional[str] = Field(None, description="The strength or dosage (e.g., 500mg, 10ml)")
    frequency: Optional[str] = Field(None, description="How often to take it (e.g., Twice a day, 1x/day)")
    duration: Optional[str] = Field(None, description="How long to take it (e.g., 7 days, 2 weeks)")
    instructions: Optional[str] = Field(None, description="Any additional instructions (e.g., take with food)")
    confidence_score: float = Field(default=1.0, description="Confidence score of the parsed data (0.0 to 1.0)")

class OCRResult(BaseModel):
    medicines: List[ExtractedMedicine] = Field(description="A list of all medications found in the prescription")
    raw_text: Optional[str] = Field(None, description="The raw text extracted from the image, if available")

class NLPParseRequest(BaseModel):
    raw_text: str = Field(description="The raw, messy text string from an OCR scanner")
