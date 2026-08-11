from pydantic import BaseModel
from typing import List

class InteractionCheckRequest(BaseModel):
    medicines: List[str]

class InteractionDetail(BaseModel):
    drug_a: str
    drug_b: str
    severity: str
    reason: str
    recommendation: str

class InteractionCheckResponse(BaseModel):
    interactions: List[InteractionDetail]
    unknown_medicines: List[str] = []
    status: str # "Safe", "Dangerous", or "Unknown"
