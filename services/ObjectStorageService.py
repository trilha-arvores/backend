import mimetypes
import os

from minio import Minio
from minio.error import S3Error

from services import DirectoryService


class ObjectStorageService:
    bucket_name = "images"
    minio_client: Minio

    @classmethod
    def setup(cls):
        minio_client = Minio(
            "192.168.0.24:9000",  # TODO Change localhost to minio for Docker
            access_key="YEv9LUqnG9Q87TPj7cbI",
            secret_key="62ijOcUlbkIKs20jm0l8TiZUYtHC3ESDkcuOVErZ",
            secure=False
        )

        # Create bucket if it does not exist
        if not minio_client.bucket_exists(cls.bucket_name):
            minio_client.make_bucket(cls.bucket_name)

        cls.minio_client = minio_client

    @classmethod
    def upload_file(cls, file):
        file_name = file.filename
        tmp_dir = DirectoryService.absolute_path_from_project('tmp')
        file_path = os.path.join(tmp_dir, file_name)
        file.save(file_path)

        # Determine the file's content type
        content_type, _ = mimetypes.guess_type(file_name)

        try:
            # Upload the file with the correct content type
            cls.minio_client.fput_object(
                cls.bucket_name,
                file_name,
                file_path,
                content_type=content_type
            )

        except S3Error as e:
            return Exception(f"Failed to upload file: {e}")

    @classmethod
    def get_url(cls, file_name) -> str:
        url = cls.minio_client.presigned_get_object(cls.bucket_name, file_name)

        return url
