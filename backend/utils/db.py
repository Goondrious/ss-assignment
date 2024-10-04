import json
import os
from pathlib import Path
from typing import Union
from fastapi import UploadFile

from utils.types import User

DB_FILE_PATH = './db.json'

# SS-TODO
# per-user directories
# unique file ids
       

def init_db(overwrite = True):
    if not os.path.exists(DB_FILE_PATH) or overwrite:
        writeFile = open(DB_FILE_PATH, "w+")
        freshDBJSON = { "users": {}, "images": {}, "imageCompressions": {} }
        writeFile.write(json.dumps(freshDBJSON))
        writeFile.close()


def get_db():
   readFile = open(DB_FILE_PATH, "r")

   dbText = readFile.read()
   dbJSON = {}
   if len(dbText) != 0:
        dbJSON = json.loads(dbText)

   readFile.close() 

   return dbJSON

def get_user(username: str) -> Union[User, None]:
   dbJSON = get_db()

   if username in dbJSON["users"]:
        return dbJSON["users"][username]
    

def get_user_images(userId: str):
   dbJSON = get_db(userId)

   return dbJSON.images[userId]

# def get_image_file(userId: str, image_id: str):
#    dbJSON = get_db(userId)
#    image = dbJSON.images[userId][image_id]

#    if image is None:
#        raise FileNotFoundError


#     if not os.path.exists("/filestore/{userId}/images/{image_id}/"):
#        raise FileNotFoundError
       
#     with Image.open(uploadFile.file) as img:
#         image_file = 
#         return image_file

def get_image_compressions(imageId: str):
   dbJSON = get_db()

   return dbJSON.image_compressions[imageId]

def set_db(updateFunction):
   dbJSON = get_db()
   writeFile = open(DB_FILE_PATH, "w")

   writeFile.write(json.dumps(updateFunction(dbJSON)))
   writeFile.close() 
   return True

def updateUser(userId: str, value: str):
    def dbUpdate(dbJSON):
        dbJSON[userId] = value
        return dbJSON

    return set_db(dbUpdate)

# SS-TODO = update username
# SS-TODO = add image
# SS-TODO = remove image
# SS-TODO = add image compression
# SS-TODO = remove image compression
