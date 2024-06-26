from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import UploadFile

from src.core.config import settings
from src.core.exeption_handlers import S3BucketException
from src.managers.s3_bucket_manager import S3BucketManager


class S3BucketService:
    def __init__(self):
        self.s3_manager = S3BucketManager()

    async def upload_user_photo(self, user_photo: UploadFile, username: str) -> str:
        """
        Uploads the user's photo to S3 and returns the URL to the image

        Args:
            user_photo (UploadFile): user's photo
            username (str): user's username

        Exceptions:
        - S3BucketException: Occurs when a file upload error occurs
        """
        max_file_size = 10 * 1024 * 1024

        if user_photo.content_type not in ["image/png", "image/jpeg"]:
            raise S3BucketException(detail="Invalid file type. Only PNG and JPEG are allowed")

        data: bytes = await user_photo.read()
        if len(data) > max_file_size:
            raise S3BucketException(detail="File size exceeds the limit of 10 MB")

        file_name_to_s3 = f"{username}_{user_photo.filename}"

        try:
            await self.s3_manager.create_bucket(bucket_name=settings.s3_bucket.s3_bucket_name)
            await self.s3_manager.upload_file(
                bucket_name=settings.s3_bucket.s3_bucket_name,
                file_name=file_name_to_s3,
                body=data,
            )
        except (NoCredentialsError, ClientError):
            raise S3BucketException(detail="failed to connect to S3")

        return f"https://{settings.s3_bucket.s3_bucket_name}.{settings.s3_bucket.s3_endpoint}/{file_name_to_s3}"
