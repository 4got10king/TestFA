from datetime import datetime

from sqlalchemy import func, select
from src.app.models.like import LikeORM
from src.app.utils.repository import SQLAlchemyRepository


class LikeRepository(SQLAlchemyRepository):
    model = LikeORM

    async def get_like(self, user_id: int, liked_user_id: int):
        return await self.get_first_with_filters(
            user_id=user_id, liked_user_id=liked_user_id
        )

    async def get_likes_by_user_id(self, user_id: int):
        return await self.get_all_with_filters(user_id=user_id)

    async def get_count_by_param(self, user_id: int, created_at: datetime) -> int:
        query = select(func.count()).where(
            LikeORM.user_id == user_id, LikeORM.created_at >= created_at
        )
        result = await self.session.execute(query)
        return result.scalar()
