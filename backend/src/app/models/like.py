from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.app.models.mixin import CreationDateMixin
from src.database.database_metadata import Base


class LikeORM(Base, CreationDateMixin):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    liked_user_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    user = relationship("ClientORM", foreign_keys=[user_id])
    liked_user = relationship("ClientORM", foreign_keys=[liked_user_id])

    def get_schema(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "liked_user_id": self.liked_user_id,
            "creation_date": self.created_at.isoformat() if self.created_at else None,
        }
