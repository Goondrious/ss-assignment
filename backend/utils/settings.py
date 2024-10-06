import logging
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

backend_root = f"{Path(__file__).parent.parent.absolute()}"

class Settings(BaseSettings):
    log_level: int = logging.DEBUG
    max_file_size: int = 50 * 1000 * 1000
    max_user_images: int = 10
    max_compressions_per_image: int = 10
    auth_secret_key: str = "shhhh"
    signed_url_secret_key: str = "url_shhhh"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    signed_image_expiry_minutes: int = 2
    base_path: str = backend_root
    db_file_path: str =  f"{base_path}/db.json"
    filestore_file_path: str =  f"{base_path}/filestore"

current_settings = Settings()
