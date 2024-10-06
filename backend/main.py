from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, UploadFile, Form, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from datetime import timedelta
import jwt

from utils.settings import current_settings
from utils.auth import authenticate_user, create_access_token, sign_compression_url, sign_image_url
from utils.image import create_and_store_user_image_compression, delete_user_image_compression_fs, delete_user_image_fs, store_user_image
from utils.types import Token, TokenData, User, UserImage, UserImageCompression
from utils.db import create_user_image_compression_db, create_user_image_db, delete_user_image_compression_db, delete_user_image_db, get_db, get_user_db, get_user_image_compression_count_db, get_user_image_compressions_db, get_user_image_db, get_user_image_compression_db, get_user_image_count_db, get_user_image_db, get_user_images_db

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
        payload = jwt.decode(token, current_settings.auth_secret_key, algorithms=[current_settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception

    dbJSON = get_db(current_settings.db_file_path)
    user = get_user_db(dbJSON, username=token_data.username)
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
    access_token_expires = timedelta(minutes=current_settings.access_token_expire_minutes)
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
async def get_user_images(current_user: Annotated[User, Depends(get_current_user)]):
    dbJSON = get_db(current_settings.db_file_path)
    images = get_user_images_db(dbJSON, current_user.id)
    for key in images:
        image = UserImage(**images[key])
        
        images[key]["num_compressions"] = get_user_image_compression_count_db(dbJSON, image.id)
        images[key]["signed_url"] = sign_image_url(image)

    return images

@app.get("/image/{image_id}")
async def get_image(current_user: Annotated[User, Depends(get_current_user)], image_id: str):
    dbJSON = get_db(current_settings.db_file_path)
    image = get_user_image_db(dbJSON, current_user.id, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")        

    image.signed_url = sign_image_url(image)

    return image
 
@app.get("/image")
async def get_image(signature: str):
    try:
        decoded = jwt.decode(signature, current_settings.signed_url_secret_key, algorithms=current_settings.algorithm)
        user_id = decoded["user_id"]
        image_id = decoded["image_id"]

        dbJSON = get_db(current_settings.db_file_path)
        image = get_user_image_db(dbJSON, user_id, image_id)
        if image is None:
            raise HTTPException(status_code=404, detail="Image not found")        

        return FileResponse(image.path)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Image link expired")        

@app.put("/image")
async def upload_image(current_user: Annotated[User, Depends(get_current_user)], file_name: Annotated[str, Form()], file: Annotated[UploadFile, Form()]):
    if len(file_name) < 3 or len(file_name) > 100:
        raise HTTPException(status_code=400, detail="Invalid file name")        

    if file.size > current_settings.max_file_size:
        raise HTTPException(status_code=400, detail="The uploaded image is too large")        

    split = file.content_type.split("/")
    file_extension = split[-1]

    if not (file_extension == 'jpeg' or file_extension == 'png' or file_extension == 'gif'):
        raise HTTPException(status_code=400, detail="Invalid image type")        

    dbJSON = get_db(current_settings.db_file_path)
    if get_user_image_count_db(dbJSON, current_user.id) > current_settings.max_user_images:
        raise HTTPException(status_code=400, detail="User has uploaded the maximum number of images")        

    image = store_user_image(current_settings.filestore_file_path, current_user, file_name, file, file_extension)
    create_user_image_db(current_settings.db_file_path, current_user.id, image)

    if image == None:
        return { "success": False }
    else:
        image.signed_url = sign_image_url(image)
        return { "file": image }

@app.delete("/image/{image_id}")
async def delete_image(current_user: Annotated[User, Depends(get_current_user)], image_id: str):
    dbJSON = get_db(current_settings.db_file_path)
    image = get_user_image_db(dbJSON, current_user.id, image_id)
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image for deletion")        
    
    delete_user_image_fs(image)
    delete_user_image_db(current_settings.db_file_path, image.user_id, image.id)

    return { "success": True }
 
@app.get("/image-compression")
async def get_image_compression(signature: str):
    try:
        decoded = jwt.decode(signature, current_settings.signed_url_secret_key, algorithms=current_settings.algorithm)
        image_id = decoded["image_id"]
        compression_id = decoded["compression_id"]

        dbJSON = get_db(current_settings.db_file_path)
        image = get_user_image_compression_db(dbJSON, image_id, compression_id)
        if image is None:
            raise HTTPException(status_code=404, detail="Image not found")        

        return FileResponse(image.path)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Image link expired")        

@app.get("/image/{image_id}/image-compressions")
async def image_compressions(current_user: Annotated[User, Depends(get_current_user)], image_id: str):
    dbJSON = get_db(current_settings.db_file_path)
    compressions = get_user_image_compressions_db(dbJSON, image_id)
    for key in compressions:
        compression = UserImageCompression(**compressions[key])
        
        compressions[key]["signed_url"] = sign_compression_url(compression)

    return compressions

@app.put("/image/{image_id}/image-compression")
async def image_compression(current_user: Annotated[User, Depends(get_current_user)], image_id: str, quality: Annotated[int, Form()], resize_width: Annotated[int, Form()]):
    if quality < 0 or quality > 100:
        raise HTTPException(status_code=400, detail="Invalid quality value")        

    if resize_width is not None and (resize_width <= 0 or resize_width > 3000):
        raise HTTPException(status_code=400, detail="Invalid quality value")        

    dbJSON = get_db(current_settings.db_file_path)
    image = get_user_image_db(dbJSON, current_user.id, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")        

    if get_user_image_compression_count_db(dbJSON, image.id) > current_settings.max_compressions_per_image:
        raise HTTPException(status_code=400, detail="User has created the maximum number of image compressions")        

    compression = create_and_store_user_image_compression(current_settings.filestore_file_path, current_user, image, quality, resize_width)
    create_user_image_compression_db(current_settings.db_file_path, compression)

    compression.signed_url = sign_compression_url(compression)
    return { "compression": compression }

@app.delete("/image/{image_id}/image-compression/{compression_id}")
async def delete_image_compression(current_user: Annotated[User, Depends(get_current_user)], image_id: str, compression_id: str):
    dbJSON = get_db(current_settings.db_file_path)
    image = get_user_image_db(dbJSON, current_user.id, image_id)
    if image is None:
        raise HTTPException(status_code=400, detail="Parent image does not exist")        
    
    compression = get_user_image_compression_db(dbJSON, image_id, compression_id)
    if compression is None:
        raise HTTPException(status_code=404, detail="Image compression not found")        

    delete_user_image_compression_fs(compression)
    delete_user_image_compression_db(current_settings.db_file_path, compression.image_id, compression.id)

    return { "success": True }

