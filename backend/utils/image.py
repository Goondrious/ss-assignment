from datetime import datetime
from os import mkdir, path
from pathlib import Path
from typing import Union
import uuid
from fastapi import UploadFile
from PIL import Image

from utils.db import create_user_image_compression, create_user_image_db, delete_user_image_compression_db, delete_user_image_db, get_user_image, get_user_image_compression
from utils.types import DATE_FORMAT, User, UserImage, UserImageCompression

base_path = Path(__file__).parent.parent.absolute() 
save_path = f"{base_path}/filestore/"

def get_subdirectory(sd):
		dir = path.join(save_path, f'{sd}')
		if not path.isdir(dir):
			mkdir(dir)
		return dir

def get_image_file(user_image: UserImage):
	image = Image.open(user_image.path)
	return image

def upload_user_image(user: User, file_name: str, upload_file: UploadFile, file_extension: str):
	output_path = f"{save_path}/{file_name}.{file_extension}"

	file_name_uuid = uuid.uuid4()
	file_id = uuid.uuid4()

	output_path = f"{get_subdirectory(user.id)}/{file_name}-{file_name_uuid}.{file_extension}"
	
	with Image.open(upload_file.file) as img:
		img.save(output_path, format=file_extension)
		date_string = datetime.now().strftime(DATE_FORMAT)
		image = UserImage(user_id = user.id, id = f"{file_id}", path = output_path, name=file_name, extension=file_extension, size=upload_file.size, uploaded_at=date_string)

		create_user_image_db(user.id, image)
		return image

def delete_user_image(image: UserImage):
	try:
		path = Path(image.path, missing_ok=True)
		path.unlink()
	except FileNotFoundError:
		print(f"Warning: attemped to delete non-existent file: {image.id}, {image.path}")

	delete_user_image_db(image.user_id, image.id)

	return True
	
def compress_image(user: User, user_image: UserImage, quality=85, resize_width: Union[None, int] = None):
	file_name = user_image.name
	file_name_uuid = uuid.uuid4()
	compression_id = uuid.uuid4()

	output_path = f"{get_subdirectory(f"{user.id}/compressions")}/{file_name}-{file_name_uuid}.{user_image.extension}"

	date_string = datetime.now().strftime(DATE_FORMAT)
	image_compression = UserImageCompression(id = f"{compression_id}", image_id =user_image.id, quality = quality, resize_width=resize_width, path=output_path, created_at=date_string)

	with Image.open(user_image.path) as img:
		final_image = img
		if resize_width is not None:
			w_percent = (resize_width / float(img.size[0]))
			h_size = int((float(img.size[1]) * float(w_percent)))
			final_image = img.resize((resize_width, h_size))

		if user_image.extension == 'jpeg':
			final_image.save(output_path, format='JPEG', quality=quality)
		elif user_image.extension == 'png':
			final_image.save(output_path, format='PNG', optimize=True)
		elif user_image.extension == 'gif':
			final_image.save(output_path, optimize=True)

		create_user_image_compression(image_compression)

		return image_compression

def delete_user_image_compression(compression: UserImageCompression):
	path = Path(compression.path, missing_ok=True)
	try:
		path.unlink()
	except FileNotFoundError:
		print(f"Warning: attemped to delete non-existent file: {compression.id}, {compression.path}")

	delete_user_image_compression_db(compression.image_id, compression.id)

	return True
 