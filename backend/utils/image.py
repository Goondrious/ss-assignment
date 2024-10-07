from datetime import datetime
from os import mkdir, path
import os
from pathlib import Path
from typing import Union
import uuid
from fastapi import UploadFile
from PIL import Image

from utils.settings import current_settings
from utils.db import create_user_image_compression_db, create_user_image_db, delete_user_image_compression_db, delete_user_image_db
from utils.types import DATE_FORMAT, User, UserImage, UserImageCompression
from utils.log_config import api_logger

def validate_nested_subdirectory(full_path: str):
	dirs = full_path.split("/")
	current_path = "/"
	for dir in dirs:
		if len(dir):
			current_path = path.join(current_path, dir)
			if not path.isdir(current_path):
				mkdir(current_path)

	return current_path

def store_user_image(filestore_path: str, user: User, file_name: str, upload_file: UploadFile, file_extension: str):
	file_name_uuid = uuid.uuid4()
	file_id = uuid.uuid4()

	full_name = f"{file_name}-{file_name_uuid}.{file_extension}"
	output_path = f"{filestore_path}/{user.id}"
	validate_nested_subdirectory(output_path)
	save_path = f"{output_path}/{full_name}"
	
	api_logger.debug(f"Saving new user image to: {output_path}")
	
	with Image.open(upload_file.file) as img:
		img.save(save_path, format=file_extension)
		date_string = datetime.now().strftime(DATE_FORMAT)
		image = UserImage(user_id = user.id, id = f"{file_id}", path = save_path, name=file_name, extension=file_extension, size=upload_file.size, uploaded_at=date_string)
		return image

def delete_user_image_fs(image: UserImage):
	api_logger.debug(f"Deleting image at {image.path}")
	try:
		path = Path(image.path, missing_ok=True)
		path.unlink()
	except FileNotFoundError:
		print(f"Warning: attemped to delete non-existent file: {image.id}, {image.path}")
	
def create_and_store_user_image_compression(filestore_dir: str, user: User, user_image: UserImage, quality=85, resize_width: Union[None, int] = None):
	file_name = user_image.name
	file_name_uuid = uuid.uuid4()
	compression_id = uuid.uuid4()

	full_name = f"{file_name}-{file_name_uuid}.{user_image.extension}"
	output_path = f"{filestore_dir}/{user.id}/compressions/"
	validate_nested_subdirectory(output_path)
	save_path = f"/{output_path}/{full_name}"

	date_string = datetime.now().strftime(DATE_FORMAT)
	image_compression = UserImageCompression(id = f"{compression_id}", image_id =user_image.id, quality = quality, resize_width=resize_width, path=save_path, created_at=date_string)

	with Image.open(user_image.path) as img:
		final_image = img
		if resize_width is not None:
			w_percent = (resize_width / float(img.size[0]))
			h_size = int((float(img.size[1]) * float(w_percent)))
			final_image = img.resize((resize_width, h_size))

		if user_image.extension == 'jpeg':
			final_image.save(save_path, format='JPEG', quality=quality, optimize=True)
		elif user_image.extension == 'png':
			final_image.save(save_path, format='PNG', optimize=True)
		elif user_image.extension == 'gif':
			final_image.save(save_path, optimize=True)


		image_compression.size = os.stat(save_path).st_size

		return image_compression

def delete_user_image_compression_fs(compression: UserImageCompression):
	path = Path(compression.path, missing_ok=True)
	try:
		path.unlink()
	except FileNotFoundError:
		print(f"Warning: attemped to delete non-existent file: {compression.id}, {compression.path}")


	return True
 