from src.core.exception.FileException import FileException
from src.core.scene.file_service import File

class FileNaming:
    LOG_FILE_NAME = "log.yml"
    DATA_FILE_NAME = "data.yml"

class SystemFileStorage:

    def __init__(self, path: str, file_name: str):
        self.file = File(path, file_name)

        if not self.file.exists():
            raise FileNotFoundError("File {} not exists".format(f"{path}/{file_name}"))

    def get_parsed_data(self, date: str) -> tuple[str, str, str]:
        lines = self.file.read()

        if not lines.__contains__(date):
            raise FileException("Section with Date {} not exists".format(date))

        return lines['data'][date]['time'], lines['data'][date]['temperature'], lines['data'][date]['humidity']