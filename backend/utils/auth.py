from datetime import datetime, timedelta, timezone
from typing import Union
import jwt
from passlib.context import CryptContext

from utils.settings import Settings
from utils.types import UserImage, UserImageCompression
from utils.db import get_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    user = get_user(username, True)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings.auth_secret_key, algorithm=Settings.algorithm)
    return encoded_jwt

def sign_image_url(image: UserImage):
   to_encode = { "user_id": image.user_id, "image_id": image.id }
   expire = datetime.now(timezone.utc) + timedelta(minutes=Settings.signed_image_expiry_minutes)
   to_encode.update({"exp": expire})
   signature = jwt.encode(to_encode, Settings.signed_url_secret_key, Settings.algorithm)
   return f"/image?signature={signature}" 

def sign_compression_url(compression: UserImageCompression):
   to_encode = { "image_id": compression.image_id, "compression_id": compression.id }
   expire = datetime.now(timezone.utc) + timedelta(minutes=Settings.signed_image_expiry_minutes)
   to_encode.update({"exp": expire})
   signature = jwt.encode(to_encode, Settings.signed_url_secret_key, algorithm=Settings.algorithm)
   return f"/image-compression?signature={signature}" 

