import json
import os
from typing import Union

from utils.types import User, UserImage, UserImageCompression
from utils.log_config import api_logger

def init_db(file_path: str, overwrite = True):
    if not os.path.exists(file_path) or overwrite:
        writeFile = open(file_path, "w+")
        freshDBJSON = { "users": {}, "images": {}, "compressions": {} }
        writeFile.write(json.dumps(freshDBJSON))
        writeFile.close()

def get_db(file_path: str):
   readFile = open(file_path, "r")

   dbText = readFile.read()
   dbJSON = {}
   if len(dbText) != 0:
        dbJSON = json.loads(dbText)

   readFile.close() 

   return dbJSON

def get_user_db(dbJSON: dict, username: str, with_password = False) -> Union[User, None]:
   if username in dbJSON["users"]:
        if not with_password:
            del dbJSON["users"][username]["password"]

        return User(**dbJSON["users"][username])
    
def get_user_images_db(dbJSON: dict, user_id: str):
   if user_id in dbJSON["images"]:
        return dbJSON["images"][user_id]

   return {} 

def get_user_image_count_db(dbJSON: dict, user_id: str):
   return len(get_user_images_db(dbJSON, user_id))

def get_user_image_db(dbJSON: dict, user_id: str, image_id: str):
   if user_id in dbJSON["images"]:
        if image_id in dbJSON["images"][user_id]:
            return UserImage(**dbJSON["images"][user_id][image_id])

def get_user_image_compressions_db(dbJSON: dict, image_id: str):
   if image_id in dbJSON["compressions"]:
        return dbJSON["compressions"][image_id]

   return {}

def get_user_image_compression_count_db(dbJSON: dict, image_id: str):
    return len(get_user_image_compressions_db(dbJSON, image_id))

def get_user_image_compression_db(dbJSON: dict, image_id: str, compression_id: str):
   if image_id in dbJSON["compressions"]:
        if compression_id in dbJSON["compressions"][image_id]:
            return UserImageCompression(**dbJSON["compressions"][image_id][compression_id])

def set_db(file_path: str, updateFunction):
   dbJSON = get_db(file_path)
   db_copy = get_db(file_path)
   # "w" 
   write_file = open(file_path, "w")

   try:
        result = updateFunction(dbJSON)
        write_file.write(json.dumps(result))
        return result
   except Exception as e:
        api_logger.info(f"Error writing to db json. Resetting db.")
        write_file.write(json.dumps(db_copy))
        raise e
   finally:
        write_file.close() 

def create_user_image_db(file_path: str, user_id: str, image: UserImage):
   def dbUpdate(dbJSON):
        if user_id in dbJSON["images"]:
            dbJSON["images"][user_id][image.id] = vars(image)
        else:
            user_dict = {}
            user_dict[image.id] = vars(image)
            dbJSON["images"][user_id] = user_dict
        return dbJSON

   return set_db(file_path, dbUpdate)
 
def delete_user_image_db(file_path: str, user_id: str, image_id: str):
   def dbUpdate(dbJSON):
        if user_id in dbJSON["images"]:
            if image_id in dbJSON["images"][user_id]:
                del dbJSON["images"][user_id][image_id]
                return dbJSON

   return set_db(file_path, dbUpdate)

def create_user_image_compression_db(file_path: str, compression: UserImageCompression):
   def dbUpdate(dbJSON):
        image_id = compression.image_id
        if image_id in dbJSON["compressions"]:
            dbJSON["compressions"][image_id][compression.id] = vars(compression) 
        else:
            image_dict = {}
            image_dict[compression.id] = vars(compression)
            dbJSON["compressions"][image_id] = image_dict

        return dbJSON

   return set_db(file_path, dbUpdate)
 
def delete_user_image_compression_db(file_path: str, image_id: str, compression_id: str):
   def dbUpdate(dbJSON):
        if image_id in dbJSON["compressions"]:
            if compression_id in dbJSON["compressions"][image_id]:
                del dbJSON["compressions"][image_id][compression_id]
                return dbJSON

   return set_db(file_path, dbUpdate)
 