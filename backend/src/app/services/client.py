from fastapi import HTTPException
from ..schemas.client import ClientData, ClientFullData
from ..utils.unitofwork import IUnitOfWork, UnitOfWork
from ..utils.image_processor import ImageProcessor
import bcrypt


class ClientService:
    @classmethod
    async def create(
        cls, model: ClientData, uow: IUnitOfWork = UnitOfWork()
    ) -> ClientFullData:
        try:
            async with uow:
                existing_client = await uow.client.get_by_email(model.email)
                if existing_client:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Email '{model.email}' is already taken.",
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

                res = await uow.client.add_one(data=data)
                await uow.commit()
                return res

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while creating the client: {str(e)}",
            )

    @classmethod
    async def authenticate(
        cls, email: str, password: str, uow: IUnitOfWork = UnitOfWork()
    ) -> dict | None:
        try:
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

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Произошла ошибка при аутентификации: {str(e)}",
            )

    @classmethod
    async def get_avatar(cls, client_id: int, uow: IUnitOfWork = UnitOfWork()) -> bytes:
        try:
            async with uow:
                client = await uow.client.get_by_id(client_id)
                if client and client.avatar:
                    return client.avatar
                else:
                    raise HTTPException(
                        status_code=404,
                        detail="Avatar not found for the given client ID.",
                    )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while retrieving the avatar: {str(e)}",
            )
