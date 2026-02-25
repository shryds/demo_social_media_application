from http import HTTPStatus
import os
import uuid
import aiofiles
import boto3
from fastapi import File, HTTPException, UploadFile
from sqlalchemy import exists
from dotenv import load_dotenv

load_dotenv()

AWS_REGION=os.environ.get("AWS_REGION")
AWS_BUCKET_NAME=os.environ.get("S3_BUCKET")
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
)

def build_s3_url(bucket: str, region: str, key: str) -> str:
    if region == "us-east-1":
        return f"https://{bucket}.s3.amazonaws.com/{key}"
    return f"https://{bucket}.s3.{region}.amazonaws.com/{key}"

async def store_file(file:UploadFile):
    if file.content_type not in ["image/jpeg","image/png","image/gif"]:
        raise HTTPException(status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    file_extention=file.filename.split(".")[-1]
    file_name=f"{uuid.uuid4()}.{file_extention}"
    

    try:
       await file.seek(0)
       s3.upload_fileobj(
            Fileobj=file.file,
            Bucket=AWS_BUCKET_NAME,
            Key=file_name,
            ExtraArgs={
                "ContentType": file.content_type,
                #"ACL": "public-read"
            },
        )
        
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=e)
    finally:
        await file.close()
    return build_s3_url(AWS_BUCKET_NAME, AWS_REGION, file_name)