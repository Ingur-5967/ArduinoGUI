import flet
import yaml
from flet.core.icons import Icons

from src.core.container.file_storage import FileNaming
from src.core.scene.file_service import File
from src.core.setting_controller import SettingController, SettingConstSection


def main(page: flet.Page):

    config = SettingController()
    def save_file(e):
        data_config_path = config.get_parameter_by_key(SettingConstSection.DATA_DIRECTORY_STORAGE)

        if data_config_path.get_value_section() == 'None':
            print("Not found path (Empty)")
            return

        data_file = File(data_config_path.get_value_section(), FileNaming.DATA_FILE_NAME)

        if not data_file.exists():
            data_file.create("")

        lines = data_file.read()

        lines['data']['033/31/032'] = {
            'temperature': '28',
            'humidity': '55'
        }

        data_file.write(lines)

    test_b = flet.IconButton(icon=Icons.APPS, on_click=save_file)

    page.add(test_b)

flet.app(target=main)