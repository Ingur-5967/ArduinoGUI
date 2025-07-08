import os

import flet
from flet.core.icons import Icons
from flet.core.text_style import TextStyle
from flet.core.types import FontWeight

from src.core.port_provider import PortService
from src.core.scene.module.scene_module import SceneModule
from src.core.scene.scene import Scene
from src.core.setting_controller import SettingConstSection, SettingController


class SettingsModule(SceneModule):

    def __init__(self):
        super().__init__("settings_module", True)

    def init(self, page: flet.Page, scene: Scene) -> flet.Control:

        def select_category(e):
            setting_controller = SettingController()

            def on_dir_selected(e: flet.FilePickerResultEvent):
                if e.path:
                    path_selector.value = f"{e.path}"

                page.update()

            def save_changes(e):
                section = setting_options[select_category_setting.value]

                if not os.path.isdir(path_selector.value):
                    pass
                else:
                    with open(setting_controller.get_config_file_path(), 'r') as file:
                        data = file.read()
                        data = data.replace(setting_controller.get_parameter_line_by_key(section),
                                            f"{section}: {path_selector.value}")

                    with open(setting_controller.get_config_file_path(), 'w') as file:
                        file.write(data)

            def com_port_select(e):
                if dropdown_selector.value.startswith("<") and dropdown_selector.value.endswith(">"):
                    dropdown_selector.key = "Select"
                    dropdown_selector.value = ""
                    dropdown_selector.update()

                page.update()

            file_picker = flet.FilePicker(on_result=on_dir_selected)
            page.overlay.append(file_picker)
            page.update()

            field_category_container.clean()

            dropdown_selector = flet.Dropdown(
                width=200,
                options=[
                    flet.DropdownOption(port.get_port_name()) for port in PortService().get_arduino_ports()
                ],
                on_change=com_port_select
            )

            if len(PortService().get_arduino_ports()) == 0:
                dropdown_selector.options = [flet.DropdownOption("<Нет активных портов>")]

            path_selector = flet.TextField(
                value=(dialog_options[select_category_setting.value] if setting_controller.get_parameter_by_key(
                    setting_options[
                        select_category_setting.value]).get_value_section() == "None" else setting_controller.get_parameter_by_key(
                    setting_options[select_category_setting.value]).get_value_section()),
                read_only=True
            )
            field_category_container.content = flet.Column(controls=[
                flet.Row(controls=[
                    path_selector,
                    flet.ElevatedButton(text="Выбрать папку", icon=Icons.EDIT,
                                        on_click=lambda _: file_picker.get_directory_path())
                ]),
                flet.TextButton(text="Сохранить изменения", on_click=save_changes)
            ]) \
                if select_category_setting.value != "Arduino" else flet.Column(
                controls=[
                    dropdown_selector,
                    flet.TextButton(text="Сохранить изменения", on_click=save_changes)
                ],

            )

            page.update()

        page.clean()

        dialog_options = {
            "Логи": "Директория для логов",
            "Данные": "Директория для данных",
            "Arduino": "Промежуток обращения к Arduino (MIN)",
        }

        setting_options = {
            "Логи": SettingConstSection.LOG_DIRECTORY_STORAGE,
            "Данные": SettingConstSection.DATA_DIRECTORY_STORAGE,
            "Arduino": SettingConstSection.COOLDOWN_STREAM_READER,
            "Data types": SettingConstSection.DATA_VIEW_TYPE,
        }

        select_category_setting = flet.Dropdown(
            value="Выберите категорию",
            options=[flet.DropdownOption(key) for key, value in setting_options.items()],
            width=130,
            on_change=select_category
        )

        field_category_container = flet.Container()

        setting_body = flet.Column(
            controls=[
                flet.Text("Настройки приложения", style=TextStyle(weight=FontWeight.W_500, size=16)),
                flet.Column(
                    controls=[
                        flet.Column(controls=[
                            select_category_setting,
                            field_category_container
                        ], spacing=20)
                    ],
                )
            ]
        )

        return flet.Container(
            key="right_container",
            width=500, height=450,
            content=flet.Column(controls=[setting_body]),
        )