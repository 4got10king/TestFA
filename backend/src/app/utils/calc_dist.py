from math import radians, sin, cos, sqrt, atan2
from concurrent.futures import ProcessPoolExecutor
import asyncio


class DistanceCalculator:
    def __init__(self):
        self.R = 6371.0  # Радиус Земли в км

    def calculate_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """Метод для вычисления расстояния между двумя точками на Земле."""
        # Градус в рад
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        # Разн коорд
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        # Формула круга
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return self.R * c

    async def calculate_distances(self, locations):
        """Асинхронный метод для вычисления расстояний между множеством точек."""
        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor() as executor:
            futures = [
                loop.run_in_executor(executor, self.calculate_distance, *loc)
                for loc in locations
            ]
            return await asyncio.gather(*futures)


distance_calculator = DistanceCalculator()
