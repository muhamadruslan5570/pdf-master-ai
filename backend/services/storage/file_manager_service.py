# ==========================================================
# PDF MASTER AI
# File Manager Service
# ==========================================================

# ----------------------------------------------------------
# IMPORT
# ----------------------------------------------------------

import shutil

from pathlib import Path

from services.storage.local_storage_service import (
    LocalStorageService
)

# ----------------------------------------------------------
# FILE MANAGER SERVICE
# ----------------------------------------------------------

class FileManagerService(LocalStorageService):

    """
    File Manager Service.
    """

    # ------------------------------------------------------
    # CREATE DIRECTORY
    # ------------------------------------------------------

    def create_directory(

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

        directory: str,

        recursive: bool = False

    ) -> list[str]:

        path = Path(directory)

        if not path.exists():

            return []

        if recursive:

            return [

                str(file)

                for file in path.rglob("*")

                if file.is_file()

            ]

        return [

            str(file)

            for file in path.iterdir()

            if file.is_file()

        ]

    # ------------------------------------------------------
    # LIST DIRECTORIES
    # ------------------------------------------------------

    def list_directories(

        self,

        directory: str

    ) -> list[str]:

        path = Path(directory)

        if not path.exists():

            return []

        return [

            str(folder)

            for folder in path.iterdir()

            if folder.is_dir()

        ]

    # ------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------

    def search(

        self,

        directory: str,

        keyword: str

    ) -> list[str]:

        path = Path(directory)

        if not path.exists():

            return []

        return [

            str(file)

            for file in path.rglob("*")

            if keyword.lower() in file.name.lower()

        ]

    # ------------------------------------------------------
    # COPY
    # ------------------------------------------------------

    def copy(

        self,

        source: str,

        destination: str

    ) -> str:

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
    # MOVE
    # ------------------------------------------------------

    def move(

        self,

        source: str,

        destination: str

    ) -> str:

        destination = Path(destination)

        destination.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        shutil.move(

            source,

            destination

        )

        return str(destination)

    # ------------------------------------------------------
    # RENAME
    # ------------------------------------------------------

    def rename(

        self,

        source: str,

        new_name: str

    ) -> str:

        source = Path(source)

        destination = source.parent / new_name

        source.rename(

            destination

        )

        return str(destination)

    # ------------------------------------------------------
    # DIRECTORY SIZE
    # ------------------------------------------------------

    def directory_size(

        self,

        directory: str

    ) -> int:

        path = Path(directory)

        if not path.exists():

            return 0

        total = 0

        for file in path.rglob("*"):

            if file.is_file():

                total += file.stat().st_size

        return total

    # ------------------------------------------------------
    # FILE COUNT
    # ------------------------------------------------------

    def file_count(

        self,

        directory: str

    ) -> int:

        path = Path(directory)

        if not path.exists():

            return 0

        return len(

            [

                file

                for file in path.rglob("*")

                if file.is_file()

            ]

        )

    # ------------------------------------------------------
    # CLEAN DIRECTORY
    # ------------------------------------------------------

    def clean(

        self,

        directory: str

    ) -> int:

        path = Path(directory)

        if not path.exists():

            return 0

        deleted = 0

        for file in path.rglob("*"):

            if file.is_file():

                file.unlink()

                deleted += 1

        return deleted

    # ------------------------------------------------------
    # STORAGE INFO
    # ------------------------------------------------------

    def storage_info(

        self,

        directory: str

    ) -> dict:

        return {

            "directory": directory,

            "files": self.file_count(

                directory

            ),

            "size": self.directory_size(

                directory

            )

        }