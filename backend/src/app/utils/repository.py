from abc import ABC

from sqlalchemy import insert, select, update, delete, literal_column
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.repositories.exceptions import DataBase404Exception


class AbstractRepository(ABC):
    pass


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(literal_column("*"))
        res = await self.session.execute(stmt)
        return res.mappings().first()

    async def edit_one(self, id: int, data: dict):
        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(id=id)
            .returning(literal_column("*"))
        )
        res = await self.session.execute(stmt)
        return res.mappings().first()

    async def edit_by_filter(self, filters: dict, data: dict) -> int:
        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(**filters)
            .returning(self.model.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_all(self) -> list:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0].get_schema() for row in res.all()]
        return res

    async def get_or_404(self, id: int):
        res = await self.session.get(self.model, id)
        if res is None:
            raise DataBase404Exception(self.model.__tablename__, id)
        return res

    async def get_all_with_filters(self, **filter_by) -> list:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = [row[0].get_schema() for row in res.all()]
        return res

    async def get_first_with_filters(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.first()

        return res[0]

    async def get_attrs_with_filters(self, *attrs, **filter_by) -> list:
        stmt = select(*attrs).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = [row[0] for row in res.all()]
        return res

    async def get_first(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = res.scalar_one().get_schema()
        return res

    async def get_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one().get_schema()
        return res

    async def delete(self, **filter_by) -> None:
        stmt = (
            delete(self.model)
            .filter_by(**filter_by)
            .returning(literal_column("*"))
        )
        res = await self.session.execute(stmt)
        return

    async def soft_delete(self, id: int) -> None:
        stmt = (
            update(self.model)
            .filter_by(id=id)
            .values(is_active=False)
            .returning(literal_column("*"))
        )
        res = await self.session.execute(stmt)
        return res

    async def get_by_id(self, id: int):
        return await self.session.get(self.model, id)

    async def get_count_by_param(self, **filter_by) -> int:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return len(res.all())
