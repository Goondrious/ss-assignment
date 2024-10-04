from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, UploadFile, Form, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from datetime import timedelta
import jwt

from utils.settings import Settings
from utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, authenticate_user, create_access_token, get_password_hash, sign_compression_url, sign_image_url
from utils.image import compress_image, delete_user_image, delete_user_image_compression, upload_user_image
from utils.types import Token, TokenData, User, UserImage, UserImageCompression
from utils.db import get_image_compression_count, get_image_compressions, get_user, get_user_image, get_user_image_compression, get_user_image_count, get_user_images

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")

@app.get("/user/{user_id}")
async def get_image(user_id: str, current_user: Annotated[User, Depends(get_current_user)]):
    if user_id == "me":
        return current_user
        
    if current_user.id != user_id:
        raise HTTPException(status_code=401, detail="You do not have permissions to access this user")        

    return current_user

@app.get("/images")
async def get_images(current_user: Annotated[User, Depends(get_current_user)]):
    images = get_user_images(current_user.id)
    for key in images:
        image = UserImage(**images[key])
        
        images[key]["signed_url"] = sign_image_url(image)

    return images

@app.get("/image/{image_id}")
async def get_image(current_user: Annotated[User, Depends(get_current_user)], image_id: str):
    image = get_user_image(current_user.id, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")        

    image.signed_url = sign_image_url(image)

    return image
 
@app.get("/image")
async def get_image(signature: str):
    try:
        decoded = jwt.decode(signature, SECRET_KEY, algorithms=ALGORITHM)
        user_id = decoded["user_id"]
        image_id = decoded["image_id"]

        image = get_user_image(user_id, image_id)
        if image is None:
            raise HTTPException(status_code=404, detail="Image not found")        

        return FileResponse(image.path)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Image link expired")        

@app.put("/image")
async def upload_image(current_user: Annotated[User, Depends(get_current_user)], file_name: Annotated[str, Form()], file: Annotated[UploadFile, Form()]):
    if len(file_name) < 3 or len(file_name) > 100:
        raise HTTPException(status_code=400, detail="Invalid file name")        

    if file.size > Settings.max_file_size:
        raise HTTPException(status_code=400, detail="The uploaded image is too large")        

    split = file.content_type.split("/")
    file_extension = split[-1]

    if not (file_extension == 'jpeg' or file_extension == 'png' or file_extension == 'gif'):
        raise HTTPException(status_code=400, detail="Invalid image type")        

    if get_user_image_count(current_user.id) > Settings.max_user_images:
        raise HTTPException(status_code=400, detail="User has uploaded the maximum number of images")        

    image = upload_user_image(current_user, file_name, file, file_extension)
    if image == None:
        return { "success": False }
    else:
        image.signed_url = sign_image_url(image)
        return { "file": image }

@app.delete("/image/{image_id}")
async def delete_image(current_user: Annotated[User, Depends(get_current_user)], image_id: str):
    image = get_user_image(current_user.id, image_id)
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image for deletion")        
    
    deleted = delete_user_image(image)
    if deleted == None:
        return { "success": False }
    else:
        return { "success": True }

@app.get("/image/{image_id}/image-compressions")
async def image_compressions(current_user: Annotated[User, Depends(get_current_user)], image_id: str):
    compressions = get_image_compressions(image_id)
    for key in compressions:
        compression = UserImageCompression(**compressions[key])
        
        compressions[key]["signed_url"] = sign_compression_url(compression)

    return compressions

@app.put("/image/{image_id}/image-compression")
async def image_compression(current_user: Annotated[User, Depends(get_current_user)], image_id: str, quality: Annotated[int, Form()], resize_width: Annotated[int, Form()]):
    if quality < 0 or quality > 100:
        raise HTTPException(status_code=400, detail="Invalid quality value")        

    if resize_width is not None and (resize_width < 0 or resize_width > 3000):
        raise HTTPException(status_code=400, detail="Invalid quality value")        

    image = get_user_image(current_user.id, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")        

    if get_image_compression_count(image.id) > Settings.max_compressions_per_image:
        raise HTTPException(status_code=400, detail="User has created the maximum number of image compressions")        

    compression = compress_image(current_user, image, quality, resize_width)
    compression.signed_url = sign_compression_url(compression)
    return { "compression": compression }

@app.delete("/image/{image_id}/image-compression/{compression_id}")
async def delete_image_compression(current_user: Annotated[User, Depends(get_current_user)], image_id: str, compression_id: str):
    image = get_user_image(current_user.id, image_id)
    if image is None:
        raise HTTPException(status_code=400, detail="Parent image does not exist")        
    
    compression = get_user_image_compression(image_id, compression_id)
    if compression is None:
        raise HTTPException(status_code=404, detail="Image compression not found")        

    delete_user_image_compression(compression)
    return { "success": True }

