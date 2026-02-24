from http import HTTPStatus
import os
import uuid
import aiofiles
from fastapi import File, HTTPException, UploadFile
from sqlalchemy import exists

UPLOAD_ASF="uploads"

os.makedirs(UPLOAD_ASF, exist_ok=True)

async def store_file(file:UploadFile):
    if file.content_type not in ["image/jpeg","image/png","image/gif"]:
        raise HTTPException(status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    file_extention=file.filename.split(".")[-1]
    file_name=f"{uuid.uuid4()}.{file_extention}"
    file_path=os.path.join(UPLOAD_ASF, file_name)

    try:
        async with aiofiles.open(file_path, 'wb') as open_file:
            while chunks:= await file.read(1028):
                await open_file.write(chunks)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=e)
    finally:
        file.close()
    return file_path