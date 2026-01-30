from pydantic import BaseModel, Field

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "gemma3-4b"
    messages: list[Message]
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1)

class Choice(BaseModel):
    message: Message
    finish_reason: str = "stop"
    index: int = 0

class ChatCompletionResponse(BaseModel):
    id: str = "chatcmpl-default"
    object: str = "chat.completion"
    created: int = 0
    model: str
    choices: list[Choice]
