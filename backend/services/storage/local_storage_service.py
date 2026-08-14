# ==========================================================
# PDF MASTER AI
# Local Storage Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import shutil

from pathlib import Path

from fastapi import UploadFile

from services.storage.base_storage_service import BaseStorageService

# ----------------------------------------------------------
# LOCAL STORAGE SERVICE
# ----------------------------------------------------------

class LocalStorageService(BaseStorageService):

    """
    Local Storage Service.
    """

    # ------------------------------------------------------
    # SAVE FILE
    # ------------------------------------------------------

    def save(

        self,

        upload_file: UploadFile,

        destination: str

    ) -> str:

        destination = Path(destination)

        destination.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        with destination.open("wb") as buffer:

            shutil.copyfileobj(

                upload_file.file,

                buffer

            )

        return str(destination)

    # ------------------------------------------------------
    # COPY FILE
    # ------------------------------------------------------

    def copy(

        self,

        source: str,

        destination: str

    ) -> str:

        source = Path(source)

        destination = Path(destination)

        destination.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        shutil.copy2(

            source,

            destination

        )

        return str(destination)

    # ------------------------------------------------------
    # MOVE FILE
    # ------------------------------------------------------

    def move(

        self,

        source: str,

        destination: str

    ) -> str:

        source = Path(source)

        destination = Path(destination)

        destination.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        shutil.move(

            str(source),

            str(destination)

        )

        return str(destination)

    # ------------------------------------------------------
    # RENAME FILE
    # ------------------------------------------------------

    def rename(

        self,

        source: str,

        new_name: str

    ) -> str:

        source = Path(source)

        destination = source.parent / new_name

        source.rename(destination)

        return str(destination)

    # ------------------------------------------------------
    # DELETE FILE
    # ------------------------------------------------------

    def remove(

        self,

        path: str

    ) -> bool:

        file = Path(path)

        if file.exists():

            file.unlink()

            return True

        return False

    # ------------------------------------------------------
    # CREATE DIRECTORY
    # ------------------------------------------------------

    def create_folder(

        self,

        directory: str

    ) -> str:

        path = Path(directory)

        path.mkdir(

            parents=True,

            exist_ok=True

        )

        return str(path)

    # ------------------------------------------------------
    # LIST FILES
    # ------------------------------------------------------

    def list_files(

        self,

        directory: str

    ) -> list[str]:

        directory = Path(directory)

        if not directory.exists():

            return []

        return [

            str(file)

            for file in directory.iterdir()

            if file.is_file()

        ]

    # ------------------------------------------------------
    # FILE INFO
    # ------------------------------------------------------

    def info(

        self,

        path: str

    ) -> dict:

        file = Path(path)

        stat = file.stat()

        return {

            "filename": file.name,

            "extension": file.suffix,

            "directory": str(file.parent),

            "size": stat.st_size,

            "created": stat.st_ctime,

            "modified": stat.st_mtime

        }