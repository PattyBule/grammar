from fastapi import APIRouter
from app.api.schemas import GrammarCheckRequest, GrammarCheckResponse, RewriteRequest, RewriteResponse, ToneAnalysisRequest
from app.services.grammar_service import GrammarService
from app.services.tone_service import ToneService
from app.services.rewrite_service import RewriteService

router = APIRouter()

grammar_service = GrammarService()
tone_service = ToneService()
rewrite_service = RewriteService()


@router.get("/styles")
def get_styles():
    return {
        "styles": ["neutral", "natural", "polite", "formal", "friendly", "casual"]
    }


@router.post("/grammar/check", response_model=GrammarCheckResponse)
def grammar_check(payload: GrammarCheckRequest):
    result = grammar_service.check_and_correct(payload.text)
    return GrammarCheckResponse(
        text=payload.text,
        corrected_text=result["corrected_text"],
        issues=result["issues"],
    )


@router.post("/tone/analyze")
def tone_analyze(payload: ToneAnalysisRequest):
    result = tone_service.analyze(payload.text)
    return result


@router.post("/rewrite", response_model=RewriteResponse)
def rewrite_text(payload: RewriteRequest):
    result = rewrite_service.process(payload)
    return RewriteResponse(**result)
