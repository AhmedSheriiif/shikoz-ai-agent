from pydantic import BaseModel
from typing import List, Literal

class AnalysisResult(BaseModel):
    summary: str
    language: Literal["arabic", "english"]
    key_points: List[str]
    sentiment: Literal["positive", "negative", "neutral"]
