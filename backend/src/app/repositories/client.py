from sqlalchemy import select
from src.app.models.client import ClientORM
from sqlalchemy import exc
from src.app.utils.repository import SQLAlchemyRepository


class ClientRepository(SQLAlchemyRepository):
    model = ClientORM

    async def get_by_email(self, email: str) -> ClientORM | None:
        stmt = select(self.model).where(self.model.email == email)
        try:
            res = (await self.session.execute(stmt)).scalar_one()
        except exc.NoResultFound:
            res = None
        return res
