from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        description="Natural-language procurement question."
    )


class ChatResponse(BaseModel):
    answer: str