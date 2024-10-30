from src.app_config.config_redis import RedisRepository


async def get_redis_repo() -> RedisRepository:
    return await RedisRepository.connect()
