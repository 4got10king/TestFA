from typing import Any
from fastapi import HTTPException, status


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
