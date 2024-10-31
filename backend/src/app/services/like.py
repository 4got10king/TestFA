from fastapi import HTTPException
from src.app.utils.unitofwork import IUnitOfWork, UnitOfWork
from datetime import datetime, timedelta


class LikeService:
    @classmethod
    async def check_daily_limit(
        cls, user_id: int, uow: IUnitOfWork = UnitOfWork()
    ) -> bool:
        async with uow:
            limit_time = datetime.utcnow() - timedelta(days=1)
            count = await uow.like.get_count_by_param(
                user_id=user_id, creation_date=limit_time
            )
            return count >= 5

    @classmethod
    async def create_like(
        cls, user_id: int, liked_user_id: int, uow: IUnitOfWork = UnitOfWork()
    ):
        async with uow:
            try:
                existing_like = await uow.like.get_first_with_filters(
                    user_id=user_id, liked_user_id=liked_user_id
                )
                if existing_like is not None:
                    raise HTTPException(status_code=400, detail="Вы уже лайкали.")

                like_data = {
                    "user_id": user_id,
                    "liked_user_id": liked_user_id,
                    "creation_date": datetime.utcnow(),
                }
                new_like = await uow.like.add_one(data=like_data)
                await uow.commit()

                return {
                    "user_id": new_like.user_id,
                    "liked_user_id": new_like.liked_user_id,
                    "creation_date": new_like.creation_date,
                }
            except Exception:
                raise HTTPException(
                    status_code=500, detail="Ошибка при создании лайка."
                )
