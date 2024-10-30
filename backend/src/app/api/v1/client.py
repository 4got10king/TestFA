from fastapi import APIRouter, File, UploadFile, Form, status, HTTPException
from starlette.responses import JSONResponse, StreamingResponse
import io

from src.app.schemas.client import AuthResponse, ClientData
from src.app.schemas.enums import GenderEnum
from src.app.services.client import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post(
    "/create",
    response_model=ClientData,
    status_code=status.HTTP_201_CREATED,
    description="Создание модели участников",
)
async def register(
    name: str = Form(..., description="Имя"),
    surname: str = Form(..., description="Фамилия"),
    email: str = Form(..., description="Почта"),
    gender: GenderEnum = Form(..., description="Пол"),
    avatar: UploadFile = File(None),
    password: str = Form(..., description="Пароль"),
):
    avatar_content = await avatar.read() if avatar else None

    user = ClientData(
        name=name,
        surname=surname,
        email=email,
        gender=gender,
        avatar=avatar_content,
        password=password,
    )

    try:
        created_user = await ClientService.create(user)
        response_data = {
            "id": created_user["id"],
            "name": created_user["name"],
            "surname": created_user["surname"],
            "email": created_user["email"],
            "gender": created_user["gender"],
        }
        return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"An error occurred while creating the client: {str(e)}"
            },
        )


@router.get(
    "/avatar/{client_id}",
    status_code=status.HTTP_200_OK,
    description="Получить аватар пользователя",
)
async def get_avatar(client_id: int):
    avatar_content = await ClientService.get_avatar(client_id)
    return StreamingResponse(io.BytesIO(avatar_content), media_type="image/jpeg")


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    description="Аутентификация пользователя",
)
async def login(
    email: str = Form(..., description="Почта"),
    password: str = Form(..., description="Пароль"),
):
    try:
        user_info = await ClientService.authenticate(email, password)
        return JSONResponse(content=user_info, status_code=status.HTTP_200_OK)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"An error occurred during login: {str(e)}"},
        )
