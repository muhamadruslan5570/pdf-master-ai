# ==========================================================
# PDF MASTER AI
# Cloudflare R2 Storage Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import boto3

from botocore.client import Config

from services.storage.base_storage_service import BaseStorageService

# ----------------------------------------------------------
# R2 STORAGE SERVICE
# ----------------------------------------------------------

class R2StorageService(BaseStorageService):

    """
    Cloudflare R2 Storage Service.
    """

    def __init__(

        self,

        db,

        endpoint_url: str,

        access_key: str,

        secret_key: str,

        bucket_name: str

    ):

        super().__init__(db)

        self.bucket = bucket_name

        self.client = boto3.client(

            "s3",

            endpoint_url=endpoint_url,

            aws_access_key_id=access_key,

            aws_secret_access_key=secret_key,

            config=Config(

                signature_version="s3v4"

            )

        )

    # ------------------------------------------------------
    # UPLOAD
    # ------------------------------------------------------

    def upload(

        self,

        local_file: str,

        object_name: str

    ):

        self.client.upload_file(

            local_file,

            self.bucket,

            object_name

        )

        return object_name

    # ------------------------------------------------------
    # DOWNLOAD
    # ------------------------------------------------------

    def download(

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
    # DELETE
    # ------------------------------------------------------

    def delete(

        self,

        object_name: str

    ):

        self.client.delete_object(

            Bucket=self.bucket,

            Key=object_name

        )

    # ------------------------------------------------------
    # URL
    # ------------------------------------------------------

    def url(

        self,

        object_name: str

    ):

        return f"{self.bucket}/{object_name}"