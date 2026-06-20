from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    description: str

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True