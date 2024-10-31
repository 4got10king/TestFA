from pydantic_settings import BaseSettings, SettingsConfigDict
from redis import asyncio as aioredis
from typing import Dict, Optional, List, Any
import pickle


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_prefix="REDIS_",
    )
    endpoint: str


class RedisRepository:
    def __init__(self, redis: aioredis.Redis) -> None:
        self.redis = redis

    @classmethod
    async def connect(cls) -> "RedisRepository":
        redis_settings = RedisSettings()
        redis_endpoint = redis_settings.endpoint
        try:
            redis = await aioredis.from_url(redis_endpoint)
            if not await redis.ping():
                raise ValueError("Redis connection failed")
            return cls(redis)
        except aioredis.RedisError as e:
            print(e)
            return e

    async def add_one(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        if ttl:
            await self.redis.set(key, value, ttl)
        else:
            await self.redis.set(key, value)

    async def add_one_obj(
        self,
        key_obj: str,
        obj_value: Any,
        ttl: Optional[int] = None,
    ) -> None:
        serialized_obj = pickle.dumps(obj_value)
        if ttl:
            await self.redis.set(key_obj, serialized_obj, ex=ttl)
        else:
            await self.redis.set(key_obj, serialized_obj)

    async def get_one(self, key: str) -> Optional[str]:
        return await self.redis.get(key)

    async def get_one_obj(self, key_obj: str) -> Optional[Any]:
        serialized_obj = await self.redis.get(key_obj)
        if serialized_obj:
            obj = pickle.loads(serialized_obj)
            return obj
        else:
            return None

    async def get_all_by_prefix(self, prefix: str) -> Dict[str, Optional[str]]:
        keys: List[str] = await self.redis.keys(f"{prefix}*")
        values: Dict[str, Optional[str]] = {
            key: await self.redis.get(key) for key in keys
        }
        return values

    async def get_all_obj_by_prefix(self, prefix: str) -> Dict[str, Optional[Any]]:
        keys: List[str] = await self.redis.keys(f"{prefix}*")
        values: Dict[str, Optional[Any]] = {}
        for key in keys:
            serialized_obj = await self.redis.get(key)
            if serialized_obj:
                obj = pickle.loads(serialized_obj)
                values[key] = obj
            else:
                values[key] = None
        return values

    async def remove_by_key(self, key: str) -> int:
        return await self.redis.delete(key)

    async def disconnect(self):
        self.redis.close()
        await self.redis.wait_closed()

    async def clean_all(self):
        keys = await self.redis.keys("*")
        for key in keys:
            await self.redis.delete(key)
