import datetime

import flet
from flet.core.colors import Colors
from flet.core.icons import Icons
from flet.core.text_style import TextStyle
from flet.core.types import FontWeight

from src.core.container.file_storage import FileNaming
from src.core.scene.file_service import File
from src.core.scene.module.scene_module import SceneModule
from src.core.scene.scene import Scene
from src.core.setting_controller import SettingController, SettingConstSection


class HistoryModule(SceneModule):

    def __init__(self):
        super().__init__("history_module", True)

    def init(self, page: flet.Page, scene: Scene) -> flet.Control:
        setting_controller = SettingController()
        def handle_change(e):
            date_time_text.value = f"Текущая дата: {e.control.value.strftime('%m/%d/%Y')}"

            data_directory_path = setting_controller.get_parameter_by_key(SettingConstSection.DATA_DIRECTORY_STORAGE)

            if data_directory_path is None:
                pass
            else:

                data_file = File(data_directory_path.get_value_section(), FileNaming.DATA_FILE_NAME)

                if len(data_file.read()) == 0: pass

                data_containers = []

                file_steam_reader = data_file.read()



                for index, entry in enumerate(file_steam_reader["data"].keys()):

                    entry_date = entry.split(" ")[0]
                    entry_time = entry.split(" ")[1]

                    if entry_date != e.control.value.strftime('%m/%d/%Y'): continue

                    data_containers.append(
                        flet.Container(
                            content=flet.Column(controls=[
                            flet.Text(value=f"Данные за {entry_date} {entry_time}"),
                            flet.Row(controls=[
                                flet.Icon(name=Icons.SEVERE_COLD),
                                flet.Text(
                                    value=f"Температура: {file_steam_reader["data"][f"{entry_date} {entry_time}"]["temperature"]}",
                                    style=TextStyle(size=15, weight=FontWeight.W_500)
                                )], spacing=5
                            ),
                            flet.Row(controls=[
                                flet.Icon(name=Icons.CLOUD),
                                flet.Text(
                                    value=f"Влажность: {file_steam_reader["data"][f"{entry_date} {entry_time}"]["humidity"]}",
                                    style=TextStyle(size=15, weight=FontWeight.W_500)
                                )], spacing=5
                            ),
                            flet.Container(height=1, bgcolor=Colors.GREY)
                        ], spacing=10), height=90, bgcolor=Colors.GREY_50)
                    )

                if len(data_containers) > 0:
                    entries_counter_text.value = f"Обнаружено записей: {len(data_containers)}"
                    entries_counter_text.visible = True

                    for container in data_containers:
                        entries_list_view.controls.append(container)

                    container_content.controls.append(entries_list_view)
                else:
                    entries_counter_text.value = f"За выбранный период {e.control.value.strftime('%m/%d/%Y')} не найдено ни одной записи, полученной с Arduino"
                    entries_counter_text.visible = True

                    if container_content.controls.__contains__(entries_list_view):
                        container_content.controls.remove(entries_list_view)

                    entries_list_view.controls.clear()

            page.update()

        entries_title = flet.Row(
            controls=[
                flet.Text(value="Записи сбора данных", style=TextStyle(size=17, weight=FontWeight.W_500)),
            ],
            spacing=12
        )

        data_choose_calendar = flet.DatePicker(
                    first_date=datetime.datetime(year=2000, month=10, day=1),
                    last_date=datetime.datetime(year=2025, month=10, day=1),
                    on_change=handle_change,
        )

        date_time_text = flet.Text(value="Текущая дата: Не выбранная дата")

        entries_list_view = flet.ListView(spacing=15, padding=10, width=500, height=270, controls=[])

        entries_counter_text = flet.Text(visible=False, style=TextStyle(size=16, weight=FontWeight.W_500))


        warning_text_title = flet.Text(
            value="Warning!",
            color=Colors.RED,
            style=TextStyle(size=15, weight=FontWeight.W_700)
        )
        warning_text_body = flet.Text(
            value="Обнаружена аномально высокая температура (33) в течении N минут\nСоветуем переместиться ближе к водоемам",
            color=Colors.BLACK, style=TextStyle(size=13, weight=FontWeight.W_400)
        )

        warning_container = flet.Container(
            content=flet.Column(
                controls=[
                    warning_text_title,
                    warning_text_body,
                    flet.TextButton(text="Постановление Роспотребнадзора", icon=Icons.WARNING)
                ], spacing=5)
        )

        container_content = flet.Column(controls=[
                flet.Column(controls=[
                    entries_title,
                    flet.Row(controls=[date_time_text, data_choose_calendar], spacing=5),
                    flet.TextButton(text="Выбрать дату", icon=Icons.CALENDAR_TODAY, on_click=lambda e: page.open(data_choose_calendar)),
                ]),
                entries_counter_text
            ], spacing=15 if len(entries_list_view.controls) > 0 else 8
        )

        return flet.Container(
            key="right_container",
            width=500, height=450,
            content=container_content
        )