import httpx
from typing import Optional, Tuple


class GeocodingService:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"

    async def get_coordinates(self, city: str) -> Optional[Tuple[float, float]]:
        """Получение координат города по названию с использованием Nominatim API."""
        params = {
            "q": city,
            "format": "json",
            "limit": 1,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            if response.status_code == 200 and response.json():
                data = response.json()[0]
                latitude = float(data["lat"])
                longitude = float(data["lon"])
                return latitude, longitude
        raise ValueError("Координаты не найдены для указанного города.")


geocoding_service = GeocodingService()
