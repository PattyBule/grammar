from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class GrammarIssue(BaseModel):
    issue_type: Literal[
        "spelling",
        "grammar",
        "tense",
        "article",
        "preposition",
        "punctuation",
        "word_choice",
        "sentence_structure",
    ]
    original_text: str
    suggestion: str
    explanation: str
    severity: Literal["low", "medium", "high"]
    start_index: Optional[int] = None
    end_index: Optional[int] = None


class ToneAnalysis(BaseModel):
    tone: Literal["direct", "neutral", "polite", "formal", "friendly", "harsh"]
    intensity: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    reasons: List[str] = []


class RewriteOption(BaseModel):
    style: Literal["neutral", "natural", "polite", "formal", "friendly", "casual"]
    text: str
    explanation: str


class GrammarCheckRequest(BaseModel):
    text: str = Field(..., min_length=1)


class ToneAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1)


class RewriteRequest(BaseModel):
    text: str = Field(..., min_length=1)
    style: Literal["neutral", "natural", "polite", "formal", "friendly", "casual"] = "natural"
    context: Literal["chat", "email", "work", "study", "daily"] = "chat"


class GrammarCheckResponse(BaseModel):
    text: str
    corrected_text: str
    issues: List[GrammarIssue]


class RewriteResponse(BaseModel):
    original_text: str
    corrected_text: str
    tone_analysis: ToneAnalysis
    rewrite_options: List[RewriteOption]
    summary: str
