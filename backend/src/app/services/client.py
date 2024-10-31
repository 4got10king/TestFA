from fastapi import HTTPException
from src.app_config.config_redis import RedisRepository
from ..schemas.client import AuthResponse, ClientData, ClientFullData
from ..utils.unitofwork import IUnitOfWork, UnitOfWork
from ..utils.image_processor import ImageProcessor
import bcrypt
from sqlalchemy import select
from ..models.client import ClientORM
from ..schemas.client import GenderEnum
from geopy.distance import great_circle


class ClientService:
    redis_repo: RedisRepository = None

    @classmethod
    async def initialize(cls):
        cls.redis_repo = await RedisRepository.connect()

    @classmethod
    async def create(
        cls, model: ClientData, uow: IUnitOfWork = UnitOfWork()
    ) -> ClientFullData:
        async with uow:
            await cls.check_email_availability(model.email, uow)
            hashed_password = cls.hash_password(model.password)
            avatar_content = await cls.process_avatar(model.avatar)

            data = cls.prepare_client_data(model, hashed_password, avatar_content)
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
            return cls.build_auth_response(client)

    @classmethod
    async def get_avatar(cls, client_id: int, uow: IUnitOfWork = UnitOfWork()) -> bytes:
        async with uow:
            client = await uow.client.get_by_id(client_id)
            if client and client.avatar:
                return client.avatar
            raise HTTPException(
                status_code=404, detail="Не найдена аватарка или нет такого клиента."
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
            user_like = await uow.like.get_first_with_filters(
                user_id=user_id, liked_user_id=other_user_id
            )
            other_user_like = await uow.like.get_first_with_filters(
                user_id=other_user_id, liked_user_id=user_id
            )
            return user_like is not None and other_user_like is not None

    @classmethod
    async def get_all_clients(
        cls,
        name: str = None,
        surname: str = None,
        gender: GenderEnum = None,
        sort_by: str = "creation_date",
        sort_order: str = "asc",
        user_location: tuple = None,
        distance: float = None,
        uow: IUnitOfWork = UnitOfWork(),
    ) -> list[ClientData]:
        if cls.redis_repo is None:
            await cls.initialize()

        cache_key = cls.build_cache_key(
            name, surname, gender, sort_by, sort_order, user_location, distance
        )
        cached_result = await cls.redis_repo.get_one_obj(cache_key)
        if cached_result is not None:
            return cached_result

        async with uow:
            query = cls.build_query(name, surname, gender)
            result = await uow.session.execute(query)
            clients = result.scalars().all()

            if user_location and distance is not None:
                filtered_clients = cls.filter_clients_by_distance(
                    clients, user_location, distance
                )
                await cls.redis_repo.add_one_obj(cache_key, filtered_clients, ttl=300)
                return filtered_clients

            result_clients = cls.build_result_clients(clients)
            await cls.redis_repo.add_one_obj(cache_key, result_clients, ttl=300)
            return result_clients

    @staticmethod
    async def check_email_availability(email: str, uow: IUnitOfWork):
        existing_client = await uow.client.get_by_email(email)
        if existing_client:
            raise HTTPException(status_code=400, detail=f"Email '{email}' уже занят")

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    async def process_avatar(avatar_content):
        if avatar_content:
            return await ImageProcessor.process_avatar(avatar_content)
        return None

    @staticmethod
    def prepare_client_data(
        model: ClientData, hashed_password: str, avatar_content: bytes
    ) -> dict:
        return {
            "email": model.email,
            "avatar": avatar_content,
            "name": model.name,
            "surname": model.surname,
            "gender": model.gender,
            "password": hashed_password,
            "latitude": model.latitude,
            "longitude": model.longitude,
        }

    @staticmethod
    def build_auth_response(client) -> AuthResponse:
        return {
            "id": client.id,
            "name": client.name,
            "surname": client.surname,
            "email": client.email,
            "gender": client.gender,
        }

    @staticmethod
    def build_cache_key(
        name, surname, gender, sort_by, sort_order, user_location, distance
    ) -> str:
        return f"clients_{name}_{surname}_{gender}_{sort_by}_{sort_order}_{user_location}_{distance}"

    @staticmethod
    def build_query(name, surname, gender):
        query = select(ClientORM)
        if name:
            query = query.where(ClientORM.name.ilike(f"%{name}%"))
        if surname:
            query = query.where(ClientORM.surname.ilike(f"%{surname}%"))
        if gender:
            query = query.where(ClientORM.gender == gender)
        return query

    @staticmethod
    def filter_clients_by_distance(clients, user_location, distance):
        return [
            client
            for client in clients
            if great_circle(user_location, (client.latitude, client.longitude)).km
            <= distance
        ]

    @staticmethod
    def build_result_clients(clients) -> list:
        return [
            {
                "id": client.id,
                "name": client.name,
                "surname": client.surname,
                "email": client.email,
                "gender": client.gender,
                "latitude": client.latitude,
                "longitude": client.longitude,
            }
            for client in clients
        ]
