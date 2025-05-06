import uuid

from pydantic import BaseModel

class Prompt(BaseModel):
    id: uuid.UUID
    difficulty: str
    text: str
    language: str
    is_active: bool