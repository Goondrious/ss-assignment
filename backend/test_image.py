import pytest
from os import path, rmdir
from pathlib import Path
from fastapi import UploadFile

from utils.types import User
from utils.image import create_and_store_user_image_compression, delete_user_image_compression_fs, delete_user_image_fs, store_user_image, validate_nested_subdirectory
from utils.settings import current_settings

test_filestore_dir = f"{current_settings.base_path}/filestore-test"
test_user_id = "123"

@pytest.fixture(scope='function')
def fs_resource(request):
    validate_nested_subdirectory(test_filestore_dir)

    def fs_teardown():
        file = Path(test_filestore_dir)
        file.rmdir()

    request.addfinalizer(fs_teardown)

    return

def test_validate_nested_subdirectory():
    validate_nested_subdirectory(test_filestore_dir)

    assert path.isdir(test_filestore_dir)

    file = Path(test_filestore_dir, missing_ok=True)
    file.rmdir()


def test_store_user_image(fs_resource):
    test_user = User(
       id = test_user_id,
       username = "test-user" 
    )

    with open('./test-image.png', mode='rb') as file:
        upload_file = UploadFile(file)
        upload_file.size = 100
        file_name = 'test-image'
        file_extension = 'png'

        image = store_user_image(test_filestore_dir, test_user, file_name, upload_file, file_extension)

        assert image.user_id == test_user.id
        assert image.name == file_name

        assert path.exists(image.path)

        file = Path(image.path)
        file.unlink()
        user_dir = Path(f"{test_filestore_dir}/{test_user.id}")
        user_dir.rmdir()




def test_delete_user_image_from_fs():
    test_user = User(
       id = test_user_id,
       username = "test-user" 
    )

    with open('./test-image.png', 'rb') as file:
        upload_file = UploadFile(file)
        upload_file.size = 100
        file_name = 'test-image'
        file_extension = 'png'

        image = store_user_image(test_filestore_dir, test_user, file_name, upload_file, file_extension)
        delete_user_image_fs(image)

        assert not path.exists(image.path)

        user_dir = Path(f"{test_filestore_dir}/{test_user.id}")
        user_dir.rmdir()


def test_store_user_image_compression():
    test_user = User(
       id = test_user_id,
       username = "test-user" 
    )

    with open('./test-image.png', 'rb') as file:
        upload_file = UploadFile(file)
        upload_file.size = 100
        file_name = 'test-image'
        file_extension = 'png'

        image = store_user_image(test_filestore_dir, test_user, file_name, upload_file, file_extension)
        image_compression = create_and_store_user_image_compression(test_filestore_dir, test_user, image, quality=85, resize_width = 20)

        assert path.exists(image_compression.path)

        image_file = Path(image.path, missing_ok=True)
        image_file.unlink()
        file = Path(image_compression.path, missing_ok=True)
        file.unlink()
        compression_dir = Path(f"{test_filestore_dir}/{test_user.id}/compressions", missing_ok=True)
        compression_dir.rmdir()
        user_dir = Path(f"{test_filestore_dir}/{test_user.id}", missing_ok=True)
        user_dir.rmdir()

def test_delete_user_image_compression_from_fs():
    test_user = User(
       id = test_user_id,
       username = "test-user" 
    )

    with open('./test-image.png', 'rb') as file:
        upload_file = UploadFile(file)
        upload_file.size = 100
        file_name = 'test-image'
        file_extension = 'png'

        image = store_user_image(test_filestore_dir, test_user, file_name, upload_file, file_extension)
        image_compression = create_and_store_user_image_compression(test_filestore_dir, test_user, image, quality=85, resize_width = 20)
        delete_user_image_compression_fs(image_compression)

        assert not path.exists(f"{test_filestore_dir}/{image_compression.path}")

        image_file = Path(image.path, missing_ok=True)
        image_file.unlink()
        compression_dir = Path(f"{test_filestore_dir}/{test_user.id}/compressions", missing_ok=True)
        compression_dir.rmdir()
        user_dir = Path(f"{test_filestore_dir}/{test_user.id}", missing_ok=True)
        user_dir.rmdir()
