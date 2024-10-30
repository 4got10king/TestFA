import io
import asyncio
from PIL import Image


class ImageProcessor:
    @staticmethod
    async def add_watermark_async(
        original_image: Image.Image, watermark_image: Image.Image, position=(0, 0)
    ) -> Image.Image:
        return await asyncio.to_thread(
            ImageProcessor._add_watermark, original_image, watermark_image, position
        )

    @staticmethod
    def _add_watermark(
        original_image: Image.Image, watermark_image: Image.Image, position=(0, 0)
    ) -> Image.Image:
        original_copy = original_image.copy()
        original_copy.paste(watermark_image, position, watermark_image)
        return original_copy

    @staticmethod
    async def process_avatar(avatar_content: bytes) -> bytes:
        """Обрабатывает аватар, добавляя водяной знак."""
        original_image = Image.open(io.BytesIO(avatar_content)).convert("RGBA")
        watermark_image = Image.open("watermark/water.jpg").convert("RGBA")

        watermarked_image = await ImageProcessor.add_watermark_async(
            original_image, watermark_image
        )

        img_byte_arr = io.BytesIO()
        watermarked_image.save(img_byte_arr, format="PNG")
        return img_byte_arr.getvalue()
