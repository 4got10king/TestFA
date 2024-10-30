from src.app.utils.unitofwork import UnitOfWork
from src.app_config.config_db import TestDBSettings
from src.database.database_metadata import Base
from src.database.db_accessor import DatabaseAccessor

import pytest


@pytest.fixture
async def test_db_accessor():
    db_settings = TestDBSettings()
    db_accessor = DatabaseAccessor(db_settings)
    await db_accessor.run()
    await db_accessor.init_db(Base)
    return db_accessor


@pytest.fixture
def uow_(test_db_accessor):
    uow = UnitOfWork(database_accessor_p=test_db_accessor)
    return uow


@pytest.fixture
async def clean_database(uow_: UnitOfWork):
    async with uow_:
        await uow_.delete()
        await uow_.commit()
