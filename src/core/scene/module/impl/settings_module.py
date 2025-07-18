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
                    uneditable_text_field.value = f"{e.path}"

                page.update()

            def save_changes(e):
                section = setting_options[select_category_setting.value]

                if select_category_setting.value == "Arduino":
                    if not editable_text_field.value.isdigit() or not dropdown_selector.value.startswith("COM"): return
                    with open(setting_controller.get_config_file_path(), 'r') as file:
                        data = file.read()
                        data = data.replace(
                            setting_controller.get_parameter_line_by_key(section[0]),f"{section[0]}: {dropdown_selector.value}"
                        ).replace(
                            setting_controller.get_parameter_line_by_key(section[1]),f"{section[1]}: {editable_text_field.value}"
                        )

                else:
                    if not os.path.isdir(uneditable_text_field.value):
                        pass
                    else:
                        with open(setting_controller.get_config_file_path(), 'r') as file:
                            data = file.read()
                            data = data.replace(setting_controller.get_parameter_line_by_key(section),
                                                f"{section}: {uneditable_text_field.value}")
                            print(data)

                with open(setting_controller.get_config_file_path(), 'w') as file:
                    file.write(data)
                    file.flush()


            def com_port_select(e):
                if dropdown_selector.value.startswith("<") and dropdown_selector.value.endswith(">"):
                    dropdown_selector.key = "Select"
                    dropdown_selector.value = ""
                    dropdown_selector.update()

                print(e.control.value)

                page.update()

            def open_saved_directory(e):

                if len(uneditable_text_field.value) == 0 or not os.path.isdir(uneditable_text_field.value):
                    return

                os.startfile(uneditable_text_field.value)

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
            else:
                dropdown_selector.value = PortService().get_arduino_ports()[0].get_port_name()


            editable_text_field = flet.TextField()
            uneditable_text_field = flet.TextField(
                read_only=True
            )

            if select_category_setting.value == "Arduino":
                print(123)
                insert_field_value_dropdown = setting_controller.get_parameter_by_key(setting_options[select_category_setting.value][0])
                insert_field_value_field = setting_controller.get_parameter_by_key(setting_options[select_category_setting.value][1])

                editable_text_field.value = insert_field_value_field.get_value_section() if insert_field_value_field.get_value_section() != "None" else ""
                dropdown_selector.value = insert_field_value_dropdown.get_value_section() if insert_field_value_dropdown.get_value_section() != "None" else ""
            elif select_category_setting != "Остальное":
                insert_field_value = setting_controller.get_parameter_by_key(
                    setting_options[select_category_setting.value])
                uneditable_text_field = flet.TextField(
                    value=(insert_field_value.get_value_section() if insert_field_value.get_value_section() != "None" else "123"),
                    read_only=True
                )

            field_category_container.content = flet.Column(controls=[
                flet.Row(controls=[
                    uneditable_text_field,
                    flet.ElevatedButton(text="Выбрать папку", icon=Icons.EDIT,
                                        on_click=lambda _: file_picker.get_directory_path())

                ]),
                flet.Row(controls=[
                        flet.TextButton(text="Сохранить изменения", on_click=save_changes),
                        flet.TextButton(text="Открыть папку", on_click=open_saved_directory)
                    ]
                )
            ]) \
                if select_category_setting.value != "Arduino" else flet.Column(
                controls=[
                    dropdown_selector,
                    flet.Column(controls=[
                        editable_text_field,
                        flet.Text(
                            value="Примечание: Значение конвертируются в минуты",
                            style=TextStyle(size=13)
                        )
                    ]),
                    flet.TextButton(text="Сохранить изменения", on_click=save_changes)
                ]
            ) if select_category_setting.value != "Остальное" else flet.Column(
                controls=[
                    dropdown_selector,
                    flet.Column(controls=[
                        editable_text_field,
                        flet.Text(
                            value="Формат ввода: 7:11-19:00 (Начало-Конец)",
                            style=TextStyle(size=13)
                        )
                    ]),
                    flet.TextButton(text="Сохранить изменения", on_click=save_changes)
                ]
            )

            page.update()

        page.clean()

        setting_options = {
            "Логи": SettingConstSection.LOG_DIRECTORY_STORAGE,
            "Данные": SettingConstSection.DATA_DIRECTORY_STORAGE,
            "Arduino": [SettingConstSection.SELECTED_LISTEN_COM_PORT, SettingConstSection.COOLDOWN_STREAM_READER],
            "Остальное": SettingConstSection.WORK_TIME
        }

        select_category_setting = flet.Dropdown(
            value="Выберите категорию",
            options=[flet.DropdownOption(key) for key, value in setting_options.items()],
            width=150,
            on_change=select_category
        )

        field_category_container = flet.Container()

        settings_body = flet.Column(
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
            content=flet.Column(controls=[settings_body]),
        )