from pydantic import BaseModel, Field
from typing import List

class AIQueryRequest(BaseModel):
    medicines: List[str] = Field(..., description="List of medicines the user is asking about", example=["dolo 650", "amoxicillin"])
    query: str = Field(..., description="The user's question about the medicines", example="What are the side effects?")

class AIQueryResponse(BaseModel):
    answer: str
