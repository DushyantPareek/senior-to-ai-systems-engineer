from fastapi import FastAPI
from pydantic import BaseModel
from app.services.llm_service import ask_llm
from fastapi.responses import StreamingResponse
from app.services.llm_service import stream_llm

app = FastAPI()


class AskRequest(BaseModel):
    question: str


@app.get("/")
async def root():
    return {"message": "AI Systems Engineer API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/ask")
async def ask(request: AskRequest):
    answer = await ask_llm(request.question)

    return {
        "question": request.question,
        "answer": answer
    }

@app.post("/ask/stream")
async def ask_stream(request: AskRequest):
    return StreamingResponse(
        stream_llm(request.question),
        media_type="text/plain"
    )
