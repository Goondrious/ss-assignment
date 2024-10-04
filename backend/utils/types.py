from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    id: str
    username: str
    password: Optional[str] = None

class UserImage(BaseModel):
  id: str
  user_id: str
  path: str
  name: str
  extension: str
  size: int
  uploaded_at: str
  num_compressions: Optional[int] = 0
  signed_url: Optional[str] = "" 

class UserImageCompression(BaseModel):
  id: str
  image_id: str
  path: str
  quality: int
  resize_width: Optional[int] = 0
  created_at: str
  signed_url: Optional[str] = "" 


DATE_FORMAT = '%Y-%m-%d %H:%M:%S%z'