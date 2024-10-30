from pydantic import BaseModel
from datetime import datetime


class LikeResponse(BaseModel):
    id: int
    user_id: int
    liked_user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
