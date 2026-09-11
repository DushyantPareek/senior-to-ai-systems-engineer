from fastapi import (
    FastAPI,
    HTTPException
)
from pydantic import BaseModel, Field
from app.services.llm_service import (
    ask_llm,
    stream_llm,
    LLMConnectionError,
    LLMTimeoutError,
    LLMResponseError
)
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager

from app.retrieval.retriever import build_index
from app.services.rag_service import ask_with_rag

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rag_index = await build_index()

    print(
        f"[RAG] Indexed "
        f"{len(app.state.rag_index)} documents"
    )

    yield

app = FastAPI(lifespan=lifespan)


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Question to send to the LLM"
    )


@app.get("/")
async def root():
    return {"message": "AI Systems Engineer API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/ask")
async def ask(request: AskRequest):

    try:

        answer = await ask_llm(
            request.question
        )

        return {
            "question": request.question,
            "answer": answer
        }

    except LLMConnectionError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc)
        )

    except LLMTimeoutError as exc:

        raise HTTPException(
            status_code=504,
            detail=str(exc)
        )

    except LLMResponseError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )

@app.post("/ask/stream")
async def ask_stream(request: AskRequest):
    return StreamingResponse(
        stream_llm(request.question),
        media_type="text/plain"
    )

@app.post("/ask/rag")
async def ask_rag(request: AskRequest):
    return await ask_with_rag(
        question=request.question,
        index=app.state.rag_index
    )
