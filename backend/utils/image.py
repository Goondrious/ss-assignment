from pathlib import Path
from typing import Union
from fastapi import UploadFile
from PIL import Image

base_path = Path(__file__).parent.absolute() 
save_path = f"{base_path}/filestore/"

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
 