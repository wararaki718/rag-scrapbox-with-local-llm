import os
import time
import torch
from fastapi import FastAPI, HTTPException
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from loguru import logger

from .models import ChatCompletionRequest, ChatCompletionResponse, Choice, Message

app = FastAPI(title="Gemma 3 4B API")

MODEL_ID = os.getenv("MODEL_ID", "google/gemma-3-4b-it")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

logger.info(f"Loading model {MODEL_ID} on {DEVICE}...")

# モデルのロード (メモリ不足を考慮して4bit等の量子化を検討すべきだが、まずは標準)
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16 if DEVICE == "cuda" else torch.float32,
        device_map="auto" if DEVICE == "cuda" else None
    )
    if DEVICE == "cpu":
        model = model.to(DEVICE)
    
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    # コンテナ起動を止めないために例外をキャッチするが、その後のリクエストは失敗する
    pipe = None

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    if pipe is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # OpenAI互換形式のメッセージをGemma形式のプロンプトに変換
    # transformersのapply_chat_templateを使用
    try:
        prompt = tokenizer.apply_chat_template(
            request.messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        
        outputs = pipe(
            prompt,
            max_new_tokens=request.max_tokens,
            do_sample=request.temperature > 0,
            temperature=request.temperature if request.temperature > 0 else None,
            return_full_text=False
        )
        
        generated_text = outputs[0]["generated_text"]
        
        return ChatCompletionResponse(
            model=request.model,
            created=int(time.time()),
            choices=[
                Choice(
                    message=Message(role="assistant", content=generated_text)
                )
            ]
        )
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": pipe is not None}
