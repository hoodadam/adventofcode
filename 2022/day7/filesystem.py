from dataclasses import dataclass

from typing import List


@dataclass(frozen=True)
class File:
    name: str
    size: int


class Folder:
    def __init__(self, name: str):
        self.folders: List[Folder] = []
        self.files: List[File] = []
        self.name = name

    def add_file(self, file: File):
        self.files.append(file)

    def add_folder(self, folder: 'Folder'):
        self.folders.append(folder)

    @property
    def size(self) -> int:
        return sum(file.size for file in self.files) + sum(folder.size for folder in self.folders)

    def sum_folders_no_bigger_than(self, size: int) -> int:
        result = 0
        if self.size <= size:
            result += self.size
        for folder in self.folders:
            result += folder.sum_folders_no_bigger_than(size)
        return result

    def __str__(self):
        return f'{self.name} (size: {self.size})'

    def __repr__(self):
        return f'{self.name} (size: {self.size})'