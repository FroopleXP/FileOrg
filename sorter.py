import os, shutil
from pathlib import Path
from collections import deque
from enum import Enum
from datetime import date, datetime

FILES_TO_IGNORE = [".DS_Store"]
IMAGE_FILE_EXTS = [".jpeg", ".jpg", ".png", ".tiff", ".bmp"]
VIDEO_FILE_EXTS = [".mp4", ".wmv"]
AUDIO_FILE_EXTS = [".wav", ".mp3", ".wma"]
TEXT_FILE_EXTS = [".txt", ".pdf"]


class FileSorter:
    def __init__(self, input_dir, output_dir) -> None:
        self._input_dir = input_dir
        self._output_dir = output_dir

    # Recursive scan for all files in a directory, returns a list of all file paths
    def _flatten_directory(self, directory) -> list:
        file_paths = []
        directories = deque()

        directories.append(directory)

        while directories:
            for file in os.scandir(directories[0]):
                # If we're looking at a directory, add it to the front of the stack
                if file.is_dir():
                    directories.append(file.path)

                if file.is_file() and file.name not in FILES_TO_IGNORE:
                    file_paths.append(
                        {
                            "name": file.name,
                            "path": file.path,
                            "sorted_path": None,
                            "size_b": file.stat().st_size,
                            "date_modified_ms": file.stat().st_mtime,
                        }
                    )

            # Remove last (current) directory from stack
            directories.popleft()

        return file_paths

    # Returns a file type based on file extensions
    def _defer_file_type_from_name(self, name) -> str:
        extension = os.path.splitext(name)[1].lower()
        if extension in AUDIO_FILE_EXTS:
            return "audio"
        if extension in IMAGE_FILE_EXTS:
            return "image"
        if extension in VIDEO_FILE_EXTS:
            return "video"
        if extension in TEXT_FILE_EXTS:
            return "text"
        return "unknown"

    # Given a file path, create a sorted directory name
    def _generate_sorted_path(self, file) -> str:
        date_created = datetime.fromtimestamp(file["date_modified_ms"])

        # Folder structure: <Type>/<Year>/<Month>/<Day>/<File>
        sorted_path = self._defer_file_type_from_name(file["name"]) + "/"
        sorted_path += str(date_created.year) + "/"
        sorted_path += str(date_created.strftime("%B")) + "/"
        sorted_path += str(date_created.day)

        return sorted_path

    # Do recon before committing the sort
    def dorecon(self) -> tuple:
        total_size_bytes = 0
        files_to_sort = self._flatten_directory(self._input_dir)

        # Get the total size of all files to sort
        for file in files_to_sort:
            file["sorted_path"] = (
                self._output_dir + "/" + self._generate_sorted_path(file)
            )
            total_size_bytes += file["size_b"]

        return (files_to_sort, total_size_bytes * (1e-9))

    # Do the actual sort based on a recon report
    def dosort(self, recon) -> None:
        files = recon[0]

        for file in files:
            # Create output directory and copy over, retaining meta info.
            Path(file["sorted_path"]).mkdir(parents=True, exist_ok=True)
            shutil.copy2(file["path"], file["sorted_path"])

        print("Sorting complete.")
