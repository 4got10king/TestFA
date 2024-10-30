

from ..schemas.client import ClientFullData
from ..utils.unitofwork import IUnitOfWork, UnitOfWork


class ClientService:
    @classmethod
    async def create(
        cls, model: ClientFullData, uow: IUnitOfWork = UnitOfWork()
    ) -> ClientFullData:
        async with uow:
            client = await uow.client.get_by_email(model.email)
            if client:
                return client.get_schema()

            # Сохранение аватарки в BLOB
            data = {
                "email": model.email,
                "avatar": model.avatar,  # Сохраняем бинарные данные аватарки
                "name": model.name,
                "surname": model.surname,
                "gender": model.gender,
                # Добавьте другие поля, если необходимо
            }
            res = await uow.client.add_one(data=data)

            await uow.commit()
            return res
