from pydantic import BaseModel
from typing import Optional

class CompareResult(BaseModel):
    element: str
    gender: str
    game: str
class GuessRequest(BaseModel):
    skylander_name: str
    image_url: Optional[str] = None

class GuessResponse(BaseModel):
    correct: bool
    comparison: CompareResult

class SkylanderInfo(BaseModel):
    name: str
    element: str
    gender: str
    game: str
    species: str