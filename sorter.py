import os
from collections import deque

FILES_TO_IGNORE = [".DS_Store"]


class FileSorter:
    def __init__(self, input_dir, output_dir) -> None:
        self._input_dir = input_dir
        self._output_dir = output_dir

    # Recursive scan for all files, returns a list of all file paths
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
                    file_paths.append(file.path)

            # Remove last (current) directory from stack
            directories.popleft()

        return file_paths

    def sort(self) -> None:
        file_paths = self._flatten_directory(self._input_dir)
        for path in file_paths:
            print(path)
