from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(
    title="Grammar Naturalizer API",
    version="0.1.0",
    description="English grammar checking and natural sentence rewriting for typed communication.",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "grammar-naturalizer"}
