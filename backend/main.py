import json
from typing import Union, Annotated

from fastapi import FastAPI, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from utils import compress_image, get_db, set_db, updateUser

from fastapi.middleware.cors import CORSMiddleware

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

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

def say_hello(name: Annotated[str, "this is just metadata"]) -> str:
    return f"Hello {name}"

@app.get("/hello/{name}")
def say_hello_get(name: str):
    return say_hello(name)

# SS-TAG end tutorial
app.mount("/static", StaticFiles(directory="filestore"), name="static")

@app.post("/upload-image/")
async def upload_image(file: Annotated[UploadFile, Form()], quality: Annotated[int, Form()], resizeWidth: Annotated[int, Form()]):
    # SS-TODO auth, image validation
    output_file = compress_image(file, quality, resizeWidth)
    if output_file == None:
        return { "success": False }
    else:
        return { "success": True }
