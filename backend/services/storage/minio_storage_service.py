# ==========================================================
# PDF MASTER AI
# MinIO Storage Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pathlib import Path

from minio import Minio
from minio.error import S3Error

from services.storage.base_storage_service import (
    BaseStorageService
)

# ----------------------------------------------------------
# MINIO STORAGE SERVICE
# ----------------------------------------------------------

class MinioStorageService(BaseStorageService):

    """
    MinIO Storage Service.
    """

    def __init__(

        self,

        db,

        endpoint: str,

        access_key: str,

        secret_key: str,

        bucket: str,

        secure: bool = False

    ):

        super().__init__(db)

        self.bucket = bucket

        self.client = Minio(

            endpoint,

            access_key=access_key,

            secret_key=secret_key,

            secure=secure

        )

    # ------------------------------------------------------
    # CREATE BUCKET
    # ------------------------------------------------------

    def create_bucket(self):

        if not self.client.bucket_exists(

            self.bucket

        ):

            self.client.make_bucket(

                self.bucket

            )

    # ------------------------------------------------------
    # UPLOAD FILE
    # ------------------------------------------------------

    def upload_file(

        self,

        local_file: str,

        object_name: str | None = None

    ) -> str:

        if object_name is None:

            object_name = Path(

                local_file

            ).name

        self.client.fput_object(

            self.bucket,

            object_name,

            local_file

        )

        return object_name

    # ------------------------------------------------------
    # UPLOAD BYTES
    # ------------------------------------------------------

    def upload_bytes(

        self,

        data: bytes,

        object_name: str,

        content_type: str = "application/octet-stream"

    ):

        from io import BytesIO

        stream = BytesIO(data)

        self.client.put_object(

            self.bucket,

            object_name,

            stream,

            length=len(data),

            content_type=content_type

        )

    # ------------------------------------------------------
    # DOWNLOAD FILE
    # ------------------------------------------------------

    def download_file(

        self,

        object_name: str,

        destination: str

    ) -> str:

        self.client.fget_object(

            self.bucket,

            object_name,

            destination

        )

        return destination

    # ------------------------------------------------------
    # DELETE FILE
    # ------------------------------------------------------

    def delete_file(

        self,

        object_name: str

    ):

        self.client.remove_object(

            self.bucket,

            object_name

        )

    # ------------------------------------------------------
    # FILE EXISTS
    # ------------------------------------------------------

    def file_exists(

        self,

        object_name: str

    ) -> bool:

        try:

            self.client.stat_object(

                self.bucket,

                object_name

            )

            return True

        except S3Error:

            return False

    # ------------------------------------------------------
    # LIST FILES
    # ------------------------------------------------------

    def list_files(

        self,

        prefix: str = ""

    ) -> list[str]:

        return [

            obj.object_name

            for obj in self.client.list_objects(

                self.bucket,

                prefix=prefix,

                recursive=True

            )

        ]

    # ------------------------------------------------------
    # GET METADATA
    # ------------------------------------------------------

    def get_metadata(

        self,

        object_name: str

    ):

        return self.client.stat_object(

            self.bucket,

            object_name

        )

    # ------------------------------------------------------
    # COPY FILE
    # ------------------------------------------------------

    def copy_file(

        self,

        source: str,

        destination: str

    ):

        from minio.commonconfig import CopySource

        self.client.copy_object(

            self.bucket,

            destination,

            CopySource(

                self.bucket,

                source

            )

        )

    # ------------------------------------------------------
    # MOVE FILE
    # ------------------------------------------------------

    def move_file(

        self,

        source: str,

        destination: str

    ):

        self.copy_file(

            source,

            destination

        )

        self.delete_file(

            source

        )

    # ------------------------------------------------------
    # PRESIGNED URL
    # ------------------------------------------------------

    def generate_presigned_url(

        self,

        object_name: str,

        expires: int = 3600

    ):

        from datetime import timedelta

        return self.client.presigned_get_object(

            self.bucket,

            object_name,

            expires=timedelta(

                seconds=expires

            )

        )