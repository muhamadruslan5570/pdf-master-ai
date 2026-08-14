# ==========================================================
# PDF MASTER AI
# Amazon S3 Storage Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

from pathlib import Path

import boto3

from botocore.exceptions import ClientError

from services.storage.base_storage_service import (
    BaseStorageService
)

# ----------------------------------------------------------
# S3 STORAGE SERVICE
# ----------------------------------------------------------

class S3StorageService(BaseStorageService):

    """
    Amazon S3 Storage Service.
    """

    def __init__(

        self,

        db,

        bucket: str,

        region: str,

        access_key: str,

        secret_key: str

    ):

        super().__init__(db)

        self.bucket = bucket

        self.client = boto3.client(

            "s3",

            region_name=region,

            aws_access_key_id=access_key,

            aws_secret_access_key=secret_key

        )

    # ------------------------------------------------------
    # CREATE BUCKET
    # ------------------------------------------------------

    def create_bucket(self):

        try:

            self.client.head_bucket(

                Bucket=self.bucket

            )

        except ClientError:

            self.client.create_bucket(

                Bucket=self.bucket

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

            object_name = Path(local_file).name

        self.client.upload_file(

            local_file,

            self.bucket,

            object_name

        )

        return object_name

    # ------------------------------------------------------
    # UPLOAD BYTES
    # ------------------------------------------------------

    def upload_bytes(

        self,

        data: bytes,

        object_name: str

    ):

        self.client.put_object(

            Bucket=self.bucket,

            Key=object_name,

            Body=data

        )

    # ------------------------------------------------------
    # DOWNLOAD FILE
    # ------------------------------------------------------

    def download_file(

        self,

        object_name: str,

        destination: str

    ):

        self.client.download_file(

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

        self.client.delete_object(

            Bucket=self.bucket,

            Key=object_name

        )

    # ------------------------------------------------------
    # FILE EXISTS
    # ------------------------------------------------------

    def file_exists(

        self,

        object_name: str

    ) -> bool:

        try:

            self.client.head_object(

                Bucket=self.bucket,

                Key=object_name

            )

            return True

        except ClientError:

            return False

    # ------------------------------------------------------
    # LIST FILES
    # ------------------------------------------------------

    def list_files(

        self,

        prefix: str = ""

    ) -> list:

        response = self.client.list_objects_v2(

            Bucket=self.bucket,

            Prefix=prefix

        )

        return [

            obj["Key"]

            for obj in response.get(

                "Contents",

                []

            )

        ]

    # ------------------------------------------------------
    # METADATA
    # ------------------------------------------------------

    def get_metadata(

        self,

        object_name: str

    ):

        return self.client.head_object(

            Bucket=self.bucket,

            Key=object_name

        )

    # ------------------------------------------------------
    # COPY
    # ------------------------------------------------------

    def copy_file(

        self,

        source: str,

        destination: str

    ):

        self.client.copy_object(

            Bucket=self.bucket,

            CopySource=f"{self.bucket}/{source}",

            Key=destination

        )

    # ------------------------------------------------------
    # MOVE
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

    ) -> str:

        return self.client.generate_presigned_url(

            "get_object",

            Params={

                "Bucket": self.bucket,

                "Key": object_name

            },

            ExpiresIn=expires

        )