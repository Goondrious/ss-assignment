import json
import os
from typing import Union

from utils.types import User, UserImage, UserImageCompression

DB_FILE_PATH = './db.json'

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

def get_user(username: str, with_password = False) -> Union[User, None]:
   dbJSON = get_db()

   if username in dbJSON["users"]:
        if not with_password:
            del dbJSON["users"][username]["password"]

        return User(**dbJSON["users"][username])
    
def get_user_images(user_id: str):
   dbJSON = get_db()

   if user_id in dbJSON["images"]:
        return dbJSON["images"][user_id]

   return {} 

def get_user_image_count(user_id: str):
   return len(get_user_images(user_id))

def get_user_image(user_id: str, image_id: str):
   dbJSON = get_db()

   if user_id in dbJSON["images"]:
        if image_id in dbJSON["images"][user_id]:
            return UserImage(**dbJSON["images"][user_id][image_id])

def get_image_compressions(image_id: str):
   dbJSON = get_db()

   if image_id in dbJSON["compressions"]:
        return dbJSON["compressions"][image_id]

   return {}

def get_image_compression_count(image_id: str):
    return len(get_image_compressions(image_id))

def get_user_image_compression(image_id: str, compression_id: str):
   dbJSON = get_db()

   if image_id in dbJSON["compressions"]:
        if compression_id in dbJSON["compressions"][image_id]:
            return UserImageCompression(**dbJSON["compressions"][image_id][compression_id])

def set_db(updateFunction):
   dbJSON = get_db()
   writeFile = open(DB_FILE_PATH, "w")

   try:
        result = updateFunction(dbJSON)
        writeFile.write(json.dumps(result))
        return result
   except Exception as e:
        writeFile.write(json.dumps(dbJSON))
        raise e
   finally:
        writeFile.close() 

def updateUser(user_id: str, value: str):
    def dbUpdate(dbJSON):
        dbJSON[user_id] = value
        return dbJSON

    return set_db(dbUpdate)

def create_user_image_db(user_id: str, image: UserImage):
   def dbUpdate(dbJSON):
        if user_id in dbJSON["images"]:
            dbJSON["images"][user_id][image.id] = vars(image)
        else:
            user_dict = {}
            user_dict[image.id] = vars(image)
            dbJSON["images"][user_id] = user_dict
        return dbJSON

   return set_db(dbUpdate)
 
def delete_user_image_db(user_id: str, image_id: str):
   def dbUpdate(dbJSON):
        if user_id in dbJSON["images"]:
            if image_id in dbJSON["images"][user_id]:
                del dbJSON["images"][user_id][image_id]
                return dbJSON

   return set_db(dbUpdate)

def create_user_image_compression(compression: UserImageCompression):
   def dbUpdate(dbJSON):
        image_id = compression.image_id
        if image_id in dbJSON["compressions"]:
            dbJSON["compressions"][image_id][compression.id] = vars(compression) 
        else:
            image_dict = {}
            image_dict[compression.id] = vars(compression)
            dbJSON["compressions"][image_id] = image_dict

        return dbJSON

   return set_db(dbUpdate)
 
def delete_user_image_compression_db(image_id: str, compression_id: str):
   def dbUpdate(dbJSON):
        if image_id in dbJSON["compressions"]:
            if compression_id in dbJSON["compressions"][image_id]:
                del dbJSON["compressions"][image_id][compression_id]
                return dbJSON

   return set_db(dbUpdate)
 