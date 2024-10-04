import json
import os
from pathlib import Path
from typing import Union
from fastapi import UploadFile
from PIL import Image

base_path = Path(__file__).parent.absolute() 
save_path = f"{base_path}/filestore/"
DB_FILE_PATH = './db.json'

# SS-TODO
# per-user directories
# unique file ids

def compress_image(uploadFile: UploadFile, quality=85, resizeWidth: Union[None, int] = None):
    file_name = uploadFile.filename
    output_path = save_path+file_name
    print(f"Uploading image: {file_name}")

    if not (file_name.lower().endswith('.jpg') or file_name.lower().endswith('.jpeg') or file_name.lower().endswith('.png') or file_name.lower().endswith('.gif')):
        print("Unsupported file format.")
        return None

    with Image.open(uploadFile.file) as img:
            split = output_path.split(".")
            output_path = split[0] + "-compressed." + split[1]
            
            final_image = img
            if resizeWidth is not None:
                w_percent = (resizeWidth / float(img.size[0]))
                h_size = int((float(img.size[1]) * float(w_percent)))
                final_image = img.resize((resizeWidth, h_size))

            if file_name.lower().endswith('.jpg') or file_name.lower().endswith('.jpeg'):
                final_image.save(output_path, format='JPEG', quality=quality)
            elif file_name.lower().endswith('.png'):
                final_image.save(output_path, format='PNG', optimize=True)
            elif file_name.lower().endswith('.gif'):
                final_image.save(output_path, optimize=True)

            return output_path
        

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

def get_user(userId: str):
   dbJSON = get_db()

   return dbJSON.users[userId]

def get_user_images(userId: str):
   dbJSON = get_db(userId)

   return dbJSON.images[userId]

def get_image_file(userId: str, image_id: str):
   dbJSON = get_db(userId)
   image = dbJSON.images[userId][image_id]

   if image is None:
        image_file = 

   return 

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
