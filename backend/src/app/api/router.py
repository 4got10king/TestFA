from fastapi import APIRouter

from src.app_config.config_api import settings

# from .v1.client import router as client


router = APIRouter(prefix=settings.APP_PREFIX)


# router.include_router(client)