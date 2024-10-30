from sqlalchemy import select
from src.app.models.client import ClientORM
from sqlalchemy import exc
from src.app.utils.repository import SQLAlchemyRepository
import bcrypt


class ClientRepository(SQLAlchemyRepository):
    model = ClientORM

    async def get_by_email(self, email: str) -> ClientORM | None:
        stmt = select(self.model).where(self.model.email == email)
        try:
            res = (await self.session.execute(stmt)).scalar_one()
            return res
        except exc.NoResultFound:
            return None

    async def authenticate(self, email: str, password: str) -> ClientORM | None:
        client = await self.get_by_email(email)
        if client and bcrypt.checkpw(
            password.encode("utf-8"), client.password.encode("utf-8")
        ):
            return client
        return None
