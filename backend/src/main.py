from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from starlette import status

from .app.api.router import router as api_router
from src.app_config.app_settings import app_settings
from src.database.database import database_accessor
from src.app_config.config_redis import RedisRepository
from .redisrepo.dependencies import get_redis_repo
from .app.api.logging import setup_logger
from .app.api.logging import log_middleware


def bind_exceptions(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_error(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(exc)},
        )


def bind_events(app: FastAPI) -> None:
    @app.on_event("startup")
    async def set_engine():
        db = database_accessor
        await db.run()
        app.state.db = db
        get_redis_repo.redis_repo = await RedisRepository.connect()

    @app.on_event("shutdown")
    async def close_engine():
        await app.state.db.stop()


def get_app() -> FastAPI:
    app = FastAPI(
        title="smile_ai",
        version="0.1.0",
        description="Test api",
        docs_url="/swagger",
        openapi_url="/api/test",
    )

    bind_events(app)
    bind_exceptions(app)
    app.include_router(api_router)

    setup_logger("apiLogger", "log.log")
    app.state.settings = app_settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods="*",
        allow_headers="*",
    )
    app.middleware("http")(log_middleware)
    return app


app = get_app()

"""
Nginx.conf

server {
listen 443 ssl;
server_name smileaiapi.ru www.smileaiapi.ru;

location / {
proxy_pass http://localhost:8081;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
# add_header Access-Control-Allow-Headers "*" always;
# add_header Access-Control-Allow-Methods "*" always;
# add_header Access-Control-Allow-Origin "*" always;
}
# ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

ssl_certificate /etc/ssl/smileaiapi.ru.crt; # managed by Certbot
ssl_certificate_key /etc/ssl/smileaiapi.ru.key; # managed by Certbot
# include /etc/ssl/;
#ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

"""
