import os
import yaml


class File:

    def __init__(self, path: str, file_name: str):
        self.path = path
        self.file_name = file_name

    def exists(self) -> bool:
        return os.path.exists(f"{self.path}/{self.file_name}")

    def create(self, json_data) -> bool:
        if self.exists(): return False

        with open(f"{self.path}/{self.file_name}", 'w', encoding="utf-8") as file:
            yaml.safe_dump(json_data, file)

        return True

    def read(self) -> dict:
        if not self.exists(): return {"data": {}}
        with open(f"{self.path}/{self.file_name}", 'r') as file:
            data = yaml.safe_load(file) or {"data": {}}

        return data

    def write(self, json_data) -> None:
        if not self.exists(): return
        with open(f"{self.path}/{self.file_name}", 'w') as file:
            yaml.dump(json_data, file)

    def get_path(self) -> str:
        return self.path

    def get_file_name(self) -> str:
        return self.file_name