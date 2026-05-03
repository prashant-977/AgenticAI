from typing import Any, Literal
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str
    user_role: Literal['sales_rep', 'manager', 'admin'] = 'sales_rep'

class SourceChunk(BaseModel):
    source: str
    page: int | None = None
    text: str
    score: float | None = None

class AskResponse(BaseModel):
    route: Literal['sql', 'rag', 'hybrid', 'blocked', 'review']
    answer: str
    sql_executed: str | None = None
    rows: list[dict[str, Any]] = Field(default_factory=list)
    sources: list[SourceChunk] = Field(default_factory=list)
    confidence: float = 0.75
    review_required: bool = False
    message: str | None = None
