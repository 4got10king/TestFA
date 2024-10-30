from loguru import logger
from fastapi import Request
from starlette.types import ASGIApp, Send
from configparser import ConfigParser

config = ConfigParser()
config.read("src/app/api/config.ini")

files_read = config.read("config.ini")

format_str = config.get("Logger", "format")
rotation_value = config.get("Logger", "rotation")
loki_url = config.get("Handler", "loki_url")
accepted_codes_str = config.get("AcceptedStatusCodes", "codes")
accepted_status_codes = {int(code) for code in accepted_codes_str.split(",")}


def setup_logger(logger_name: str, log_file: str, level: str = "INFO"):
    logger.remove()

    logger.add(
        log_file,
        rotation=rotation_value,
        level=level,
        format=format_str,
    )

    return logger


async def log_middleware(request: Request, call_next: ASGIApp) -> Send:
    response = await call_next(request)
    try:
        log_data = {
            "method": request.method,
            "url": request.url,
            "status_code": response.status_code,
        }
        if response.status_code not in accepted_status_codes:
            log_data["status_text"] = response.raw.status_line
            logger.warning(log_data)
        else:
            logger.info(log_data)
    except Exception as e:
        log_data["error"] = str(e)
        logger.error(log_data)
    return response
