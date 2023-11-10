from pydantic import BaseModel, Field


class WSMessageAllIn(BaseModel):
    message: str = Field(..., description="Message to send to all connected users via ws")


class WSMessageAllOut(BaseModel):
    status_code: int
    message: str


class WSMessageOnlyIn(WSMessageAllIn):
    user_id: str = Field(..., description="ID of the user to send the message")


class WSMessageOnlyOut(BaseModel):
    status_code: int
    message: str