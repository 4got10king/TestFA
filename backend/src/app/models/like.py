from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database.database_metadata import Base


class LikeORM(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    liked_user_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("ClientORM", foreign_keys=[user_id])
    liked_user = relationship("ClientORM", foreign_keys=[liked_user_id])

    def get_schema(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "liked_user_id": self.liked_user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
