from sqlalchemy import Integer, LargeBinary, String
from src.app.schemas.enums import GenderEnum
from src.app.models.mixin import IsActiveMixin
from src.database.database_metadata import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLAlchemyEnum
from typing import Optional


class ClientORM(Base, IsActiveMixin):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    avatar: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    gender: Mapped[Optional[GenderEnum]] = mapped_column(SQLAlchemyEnum(GenderEnum))
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[Optional[str]] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)

    def get_schema(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "gender": self.gender,
            "avatar": self.avatar,
        }
