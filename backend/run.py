import uvicorn
from src.app_config.app_settings import app_settings
import warnings

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    uvicorn.run(
        "src.main:app",
        host=app_settings.HOST,
        port=app_settings.PORT,
        workers=app_settings.WORKERS,
    )