import logging
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    log_level: str = logging.INFO
    max_file_size: int = 50 * 1000 * 1000
    max_user_images: int = 10
    max_compressions_per_image: int = 10
    auth_secret_key = "shhhh"
    signed_url_secret_key = "url_shhhh"
    algorithm = "HS256"
    access_token_expire_minutes = 30
    signed_image_expiry_minutes = 2
