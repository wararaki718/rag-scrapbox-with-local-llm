import os
import time

import ollama
from fastapi import FastAPI, HTTPException
from loguru import logger

from .models import ChatCompletionRequest, ChatCompletionResponse, Choice, Message

app = FastAPI(title="Gemma 3 4B API (Ollama Python)")

MODEL_NAME = os.getenv("MODEL_NAME", "gemma3:4b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")

client = ollama.AsyncClient(host=OLLAMA_HOST)

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    try:
        response = await client.chat(
            model=MODEL_NAME,
            messages=[{"role": m.role, "content": m.content} for m in request.messages],
            options={
                "temperature": request.temperature,
            }
        )
        
        return ChatCompletionResponse(
            model=MODEL_NAME,
            created=int(time.time()),
            choices=[
                Choice(
                    message=Message(
                        role=response['message']['role'],
                        content=response['message']['content']
                    )
                )
            ]
        )
    except Exception as e:
        logger.error(f"Ollama error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.get("/health")
async def health():
    try:
        await client.list()
        return {"status": "ok", "ollama_connected": True}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "error", "ollama_connected": False}
