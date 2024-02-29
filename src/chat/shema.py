from pydantic import BaseModel, Field

class MessageShema(BaseModel):
    id: int
    message: str