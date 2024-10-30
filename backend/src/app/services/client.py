from fastapi import HTTPException
from ..schemas.client import ClientFullData
from ..utils.unitofwork import IUnitOfWork, UnitOfWork


class ClientService:
    @classmethod
    async def create(
        cls, model: ClientFullData, uow: IUnitOfWork = UnitOfWork()
    ) -> ClientFullData:
        try:
            async with uow:
                client = await uow.client.get_by_email(model.email)
                if client:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Email '{model.email}' is already taken.",
                    )

                data = {
                    "email": model.email,
                    "avatar": model.avatar,
                    "name": model.name,
                    "surname": model.surname,
                    "gender": model.gender,
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
