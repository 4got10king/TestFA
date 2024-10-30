from typing import Optional
from fastapi import (
    APIRouter,
    File,
    UploadFile,
    Form,
    status,
)
from starlette.responses import JSONResponse
from starlette.responses import StreamingResponse
import io

from src.app.schemas.client import ClientData, ClientFullData
from src.app.schemas.enums import GenderEnum
from src.app.services.client import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post(
    "/create",
    response_model=ClientFullData,
    status_code=status.HTTP_201_CREATED,
    description="Создание модели участников",
)
async def register(
    name: str = Form(...),
    surname: str = Form(...),
    email: str = Form(...),
    gender: GenderEnum = Form(...),
    avatar: Optional[UploadFile] = File(None),
):
    if avatar:
        avatar_content = await avatar.read()
    else:
        avatar_content = None

    user = ClientData(
        name=name, surname=surname, email=email, gender=gender, avatar=avatar_content
    )

    created_user = await ClientService.create(user)

    response_data = {
        "id": created_user["id"],
        "name": created_user["name"],
        "surname": created_user["surname"],
        "email": created_user["email"],
        "gender": created_user["gender"],
    }

    return JSONResponse(content=response_data)


@router.get("/avatar/{client_id}")
async def get_avatar(client_id: int):
    avatar_content = await ClientService.get_avatar(client_id)

    return StreamingResponse(io.BytesIO(avatar_content), media_type="image/jpeg")
