from pydantic import BaseModel, Field


class WSMessageIn(BaseModel):
    message: str = Field(..., description="Message to send to all connected users via ws")


class WSMessageOut(BaseModel):
    status_code: int
    message: str