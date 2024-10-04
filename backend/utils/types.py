from datetime import datetime
from typing import Union
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    id: str
    username: str
    password: str

class UserImage(BaseModel):
  id: str
  user_id: str
  path: str
  name: str
  uploaded_at: datetime
  num_compressions: int

