import aioboto3
from aiobotocore.client import AioBaseClient
from botocore.exceptions import ClientError, NoCredentialsError

from src.core.config import settings
from src.core.exeption_handlers import S3BucketException


class S3BucketManager:
    def __init__(self):
        self.session = aioboto3.Session()

    def _get_s3_client(self) -> AioBaseClient:
        """create and return new S3 client"""
        try:
            client: AioBaseClient = self.session.client(
                service_name="s3",
                endpoint_url=settings.s3_bucket.s3_endpoint,
                region_name=settings.s3_bucket.s3_region,
                aws_access_key_id=settings.s3_bucket.aws_access_key_id,
                aws_secret_access_key=settings.s3_bucket.aws_secret_access_key,
            )
        except ClientError:
            raise S3BucketException("Error creating S3 bucket")
        return client

    async def create_bucket(self, bucket_name: str):
        """
        Create new bucket in S3

        Args:
            bucket_name (str): name of the bucket

        Exceptions:
        - S3BucketException: Occurs when a bucket creation error occurs
        """
        async with self._get_s3_client() as s3_client:
            try:
                await s3_client.create_bucket(Bucket=bucket_name)
            except ClientError:
                raise S3BucketException("Error creating S3 bucket")

    async def upload_file(self, bucket_name: str, file_name: str, body: bytes):
        """
        Loads the file into the specified S3 bucket

        Args:
            bucket_name (str): name of the bucket
            file_name (str): name of the file
            body (bytes): file content

        Exceptions:
        - S3BucketException: Occurs when a file upload error occurs
        """
        async with self._get_s3_client() as s3_client:
            try:
                await s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=body)
            except NoCredentialsError:
                raise S3BucketException(detail="Error uploading file to bucket")
            except ClientError:
                raise S3BucketException("Failed to upload file")
