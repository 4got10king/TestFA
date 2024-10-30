from fastapi import HTTPException
from ..schemas.client import AuthResponse, ClientData, ClientFullData
from ..utils.unitofwork import IUnitOfWork, UnitOfWork
from ..utils.image_processor import ImageProcessor
import bcrypt


class ClientService:
    @classmethod
    async def create(
        cls, model: ClientData, uow: IUnitOfWork = UnitOfWork()
    ) -> ClientFullData:
        async with uow:
            existing_client = await uow.client.get_by_email(model.email)
            if existing_client:
                raise HTTPException(
                    status_code=400,
                    detail=f"Email '{model.email}' уже знанят",
                )

            hashed_password = bcrypt.hashpw(
                model.password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

            avatar_content = model.avatar
            if avatar_content:
                avatar_content = await ImageProcessor.process_avatar(avatar_content)

            data = {
                "email": model.email,
                "avatar": avatar_content,
                "name": model.name,
                "surname": model.surname,
                "gender": model.gender,
                "password": hashed_password,
            }

            new_client = await uow.client.add_one(data=data)
            await uow.commit()
            return new_client

    @classmethod
    async def authenticate(
        cls, email: str, password: str, uow: IUnitOfWork = UnitOfWork()
    ) -> AuthResponse | None:
        async with uow:
            client = await uow.client.authenticate(email, password)
            if not client:
                raise HTTPException(
                    status_code=400,
                    detail="Неверный адрес электронной почты или пароль.",
                )

            return {
                "id": client.id,
                "name": client.name,
                "surname": client.surname,
                "email": client.email,
                "gender": client.gender,
            }

    @classmethod
    async def get_avatar(cls, client_id: int, uow: IUnitOfWork = UnitOfWork()) -> bytes:
        async with uow:
            client = await uow.client.get_by_id(client_id)
            if client and client.avatar:
                return client.avatar
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Не найдена аватарка или нет такого клиента.",
                )

    @classmethod
    async def get_client_by_id(
        cls, client_id: int, uow: IUnitOfWork = UnitOfWork()
    ) -> ClientData:
        async with uow:
            client = await uow.client.get_by_id(client_id)
            if client is None:
                raise HTTPException(status_code=404, detail="Клиент не найден")
            return client

    @classmethod
    async def check_mutual_like(
        cls, user_id: int, other_user_id: int, uow: IUnitOfWork = UnitOfWork()
    ) -> bool:
        async with uow:
            try:
                user_like = await uow.like.get_first_with_filters(
                    user_id=user_id, liked_user_id=other_user_id
                )
                other_user_like = await uow.like.get_first_with_filters(
                    user_id=other_user_id, liked_user_id=user_id
                )
                return user_like is not None and other_user_like is not None
            except Exception:
                raise HTTPException(
                    status_code=500, detail="Ошибка при проверке взаимного лайка."
                )
