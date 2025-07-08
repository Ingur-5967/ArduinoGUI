import datetime
import os.path

import flet
from flet.core.buttons import ButtonStyle
from flet.core.colors import Colors
from flet.core.icons import Icons
from flet.core.page import Page
from flet.core.text_style import TextStyle
from flet.core.types import FontWeight

from src.port_provider import PortService
from src.setting_controller import SettingConstSection, SettingController


def main(page: Page):

    page.title = "Arduino receiver signals"
    page.window.width = 800
    page.window.height = 600

    page.window.max_width = 800
    page.window.max_height = 600

    page.window.min_width = 800
    page.window.min_height = 600

    def route_to_home(e):
        page.clean()

        def refresh_data_stream_reader(e):
            data_stream_reader_title.value = f"Полученные данные за {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            page.update()

        warning_text = flet.Text(
            value="Невозможно открыть поток чтения данных, так как у вас не назначен прослушиваемый порт Arduino!\n\n"
                  "Перейдите в настройки, чтобы изменить COM-порт"
        )

        data_stream_reader_title = flet.Text(
                            value=f"Полученные данные за {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                            style=TextStyle(size=15, weight=FontWeight.W_400)
        )

        reader_application_body = flet.Column(
            controls=[
                flet.Row(
                    controls=[
                        data_stream_reader_title,
                        flet.IconButton(icon=Icons.REFRESH, on_click=refresh_data_stream_reader)
                    ]
                ),
                flet.Column(
                    controls=[
                        flet.Row(
                            controls=[
                                flet.Icon(name=Icons.SEVERE_COLD),
                                flet.Text(value=f"Температура: 123", style=TextStyle(size=17, weight=FontWeight.W_500))
                            ]
                        ),
                        flet.Row(
                            controls=[
                                flet.Icon(name=Icons.CLOUD),
                                flet.Text(value=f"Влажность: 12%", style=TextStyle(size=17, weight=FontWeight.W_500))
                            ]
                        )
                    ],
                    spacing=19
                )
            ],
            spacing=15,
        )

        right_board_container.content = flet.Column(
            controls=[
                flet.Text(
                    value=f"Прослушиваемый порт: {PortService().get_arduino_ports()[0] if len(PortService().get_arduino_ports()) > 1 else "Нет активного порта"}",
                    style=TextStyle(weight=FontWeight.W_500, size=16)
                ),
                reader_application_body

            ],
            spacing=25
        )

        page.add(flet.Row(controls=[application_body]))
        page.update()

    def route_to_statistic(e):
        page.clean()
        right_board_container.content = flet.Column(
            controls=[
                flet.Text("Вы перешли на cтатистику!"),
                flet.Text("Вы перешли на статистику!"),
                flet.Text("Вы перешли на статистику!"),
                flet.Text("Вы перешли на статистику!")
            ]
        )
        page.add(flet.Row(controls=[application_body]))
        page.update()

    def route_to_settings(e):

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
                        data = data.replace(setting_controller.get_parameter_line_by_key(section), f"{section}: {path_selector.value}")

                    with open(setting_controller.get_config_file_path(), 'w') as file:
                        file.write(data)

            file_picker = flet.FilePicker(on_result=on_dir_selected)
            page.overlay.append(file_picker)
            page.update()

            field_category_container.clean()
            path_selector = flet.TextField(
                value=(dialog_options[select_category_setting.value] if setting_controller.get_parameter_by_key(setting_options[select_category_setting.value]).get_value_section() == "None" else setting_controller.get_parameter_by_key(setting_options[select_category_setting.value]).get_value_section()),
                read_only=True
            )
            field_category_container.content = flet.Column(controls=[
                flet.Row(controls=[
                    path_selector,
                    flet.ElevatedButton(text="Выбрать папку", icon=Icons.EDIT, on_click=lambda _: file_picker.get_directory_path())
                ]),
                flet.TextButton(text="Сохранить изменения", on_click=save_changes)
            ])
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
                        ])
                    ]
                )
            ]
        )

        right_board_container.content = setting_body
        page.add(flet.Row(controls=[application_body]))
        page.update()


    home_button = flet.TextButton(
                    key="home_navigation_button",
                    text="Главная",
                    icon=Icons.HOME,
                    style=ButtonStyle(icon_size=25, text_style=TextStyle(size=17, weight=FontWeight.W_500)),
                    width=150,
                    on_click=route_to_home
    )

    statistic_button = flet.TextButton(
                    key="statistic_navigation_button",
                    text="Статистика",
                    icon=Icons.QUERY_STATS,
                    style=ButtonStyle(icon_size=25, text_style=TextStyle(size=17, weight=FontWeight.W_500)),
                    width=150,
                    on_click=route_to_statistic
    )

    entries_button = flet.TextButton(
                    key="entry_navigation_button",
                    text="Записи",
                    icon=Icons.EVENT,
                    style=ButtonStyle(icon_size=25, text_style=TextStyle(size=17, weight=FontWeight.W_500)),
                    width=150,
                    on_click=route_to_statistic
    )

    settings_button = flet.TextButton(
                    key="home_navigation_button",
                    text="Настройки",
                    icon=Icons.SETTINGS,
                    style=ButtonStyle(icon_size=25, text_style=TextStyle(size=17, weight=FontWeight.W_500)),
                    width=150,
                    on_click=route_to_settings
    )

    left_board_column = flet.Column(
        key="left_navigation_board_column",
        height=450,
        width=200,
        controls=[
            flet.Row(controls=[home_button]),
            flet.Row(controls=[statistic_button]),
            flet.Row(controls=[entries_button]),
            flet.Row(controls=[settings_button]),
        ],
        spacing=30
    )

    wrapper_left_board_container = flet.Container(key="left_navigation_board_container", bgcolor=Colors.WHITE54, content=left_board_column, padding=flet.padding.only(left=15, top=25))
    right_board_container = flet.Container(
        key="right_navigation_board_container",
        width=500, height=450,
        content=flet.Column(controls=[
            flet.Text("Добро пожаловать!", style=TextStyle(weight=FontWeight.W_500)),
            flet.Text("Программа читает данные с Arduino и строит по ним статистику"),
            flet.Text("Перед началом выберите желаемый прослушиваемый COM-порт в настройках"),
            flet.Text("Вы можете сохранять собранные данные в виде файлов, строить графики по выбранным периодам из доступных, просматривать логи работы программы"),
            flet.Text("По умолчанию задержка между обращением к Arduino - 5min, но это можно изменить в настройках программы"),
        ]),
    )

    application_body = flet.Row(controls=[wrapper_left_board_container, right_board_container], spacing=25)

    page.add(application_body)

    page.update()

flet.app(target=main)