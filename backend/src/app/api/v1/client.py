from fastapi import APIRouter, File, UploadFile, Form, status, HTTPException, Query
from starlette.responses import JSONResponse, StreamingResponse
import io

from src.app.schemas.client import AuthResponse, ClientData, ClientResponse
from src.app.schemas.enums import GenderEnum
from src.app.services.client import ClientService
from src.app.services.like import LikeService
from src.app.schemas.like import LikeResponse

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
    latitude: float = Form(..., description="Широта"),
    longitude: float = Form(..., description="Долгота"),
):
    avatar_content = await avatar.read() if avatar else None

    user = ClientData(
        name=name,
        surname=surname,
        email=email,
        gender=gender,
        avatar=avatar_content,
        password=password,
        latitude=latitude,
        longitude=longitude,
    )

    try:
        created_user = await ClientService.create(user)
        response_data = {
            "id": created_user["id"],
            "name": created_user["name"],
            "surname": created_user["surname"],
            "email": created_user["email"],
            "gender": created_user["gender"],
            "latitude": created_user["latitude"],
            "longitude": created_user["longitude"],
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
    description="Аутентефикация пользователя",
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


@router.post(
    "/{id}/match",
    response_model=LikeResponse,
    status_code=status.HTTP_200_OK,
    description="Оценивание участником другого участника",
)
async def match_participant(id: int, current_user_id: int = Form(...)):
    try:
        if await LikeService.check_daily_limit(current_user_id):
            raise HTTPException(status_code=400, detail="Лимит Лайков.")

        await LikeService.create_like(current_user_id, id)
        mutual_like = await ClientService.check_mutual_like(current_user_id, id)

        if mutual_like:
            other_participant = await ClientService.get_client_by_id(id)
            if other_participant:
                message = f"Вы понравились {other_participant.name}! Почта участника: {other_participant.email}"
                return JSONResponse(
                    content={"detail": message}, status_code=status.HTTP_200_OK
                )

        return JSONResponse(
            content={"detail": "Ваш лайк дошёл, взаимной симпатии пока нет."},
            status_code=status.HTTP_200_OK,
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        return JSONResponse(
            content={"detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get(
    "/list",
    response_model=list[ClientResponse],
    status_code=status.HTTP_200_OK,
    description="Получить список участников с возможностью фильтрации и сортировки",
)
async def list_clients(
    name: str = Query(None, description="Имя для фильтрации"),
    surname: str = Query(None, description="Фамилия для фильтрации"),
    gender: GenderEnum = Query(None, description="Пол для фильтрации"),
    sort_by: str = Query(
        "creation_date", description="Сортировка по полю (creation_date, name, surname)"
    ),
    sort_order: str = Query("asc", description="Порядок сортировки (asc, desc)"),
    latitude: float = Query(None, description="Широта для фильтрации"),
    longitude: float = Query(None, description="Долгота для фильтрации"),
    distance: float = Query(None, description="Максимальное расстояние в километрах"),
):
    user_location = (latitude, longitude) if latitude and longitude else None
    try:
        clients = await ClientService.get_all_clients(
            name=name,
            surname=surname,
            gender=gender,
            sort_by=sort_by,
            sort_order=sort_order,
            user_location=user_location,
            distance=distance,
        )
        return clients
    except Exception as e:
        return JSONResponse(
            content={"detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
