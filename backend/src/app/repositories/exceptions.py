from typing import Any
from fastapi import HTTPException, status
from starlette.responses import JSONResponse


class ExceptionHandler:
    @staticmethod
    async def handle_exception(e: Exception):
        if isinstance(e, HTTPException):
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        return JSONResponse(status_code=500, content={"detail": str(e)})


class DataBase404Exception(HTTPException):
    def __init__(self, base: Any, value: Any) -> None:
        detail = f"Not found in {base} data with primary key = {value}"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DataBase409Exception(HTTPException):
    def __init__(self, message: Any) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=message)


class DataBaseException(HTTPException):
    def __init__(self, message: Any) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class UnavailableEmailException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="email is not available",
        )
