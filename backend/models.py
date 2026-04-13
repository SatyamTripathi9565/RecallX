from pydantic import BaseModel

class Memory(BaseModel):
    content: str
    summary: str
    embedding: str
    tags: str