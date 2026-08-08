from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractedMedicine(BaseModel):
    name: str = Field(description="The brand or generic name of the medicine")
    dosage: Optional[str] = Field(None, description="The strength or dosage (e.g., 500mg, 10ml)")
    frequency: Optional[str] = Field(None, description="How often to take it (e.g., Twice a day, 1x/day)")
    duration: Optional[str] = Field(None, description="How long to take it (e.g., 7 days, 2 weeks)")

class OCRResult(BaseModel):
    medicines: List[ExtractedMedicine] = Field(description="A list of all medications found in the prescription")
    raw_text: Optional[str] = Field(None, description="The raw unformatted text extracted from the image (optional)")
