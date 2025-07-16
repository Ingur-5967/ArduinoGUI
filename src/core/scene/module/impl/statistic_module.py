import datetime
import random

import flet
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from flet.core.icons import Icons
from flet.core.matplotlib_chart import MatplotlibChart
from flet.core.text_style import TextStyle
from flet.core.types import FontWeight

from src.core.container.file_storage import FileNaming
from src.core.scene.file_service import File
from src.core.scene.module.scene_module import SceneModule
from src.core.scene.scene import Scene
from src.core.setting_controller import SettingController, SettingConstSection
from src.core.tool.graph_tool import GraphTool


class StatisticModule(SceneModule):

    def __init__(self):
        super().__init__("statistic_module", True)

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

                file_steam_reader = data_file.read()

                sorted_date_time = list(map(lambda date: date.split(" ")[1], file_steam_reader["data"].keys()))

                start_date_time_chart, end_date_time_chart = sorted_date_time[0], sorted_date_time[-1]

                data_container = dict()

                for index, entry in enumerate(file_steam_reader["data"].keys()):

                    entry_date = entry.split(" ")[0]
                    entry_time = entry.split(" ")[1]

                    if entry_date != e.control.value.strftime('%m/%d/%Y'): continue

                    data_container[entry_time] = {
                        "temperature": file_steam_reader["data"][f'{entry_date} {entry_time}']['temperature'],
                        "humidity": file_steam_reader["data"][f'{entry_date} {entry_time}']['humidity'],
                    }

                parsed_temperature_values = [float(data_container[section]['temperature']) for section in
                                             data_container.keys()]
                parsed_humidity_values = [float(data_container[section]['humidity']) for section in data_container.keys()]

                start = pd.to_datetime(start_date_time_chart)
                end = pd.to_datetime(end_date_time_chart)

                if end <= start:
                    end += pd.Timedelta(days=1)

                graph_temperature_element = GraphTool(list(data_container.keys()),
                                                      parsed_temperature_values).build_graph(
                    "График изменения температуры", "Время замеров", "Температура (°C)", start, end, (7, 4))
                graph_humidity_element = GraphTool(list(data_container.keys()), parsed_humidity_values).build_graph(
                    "График изменения влажности", "Время замеров", "Влажность (%)", start, end, (7, 4))

                if len(entries_list_view.controls) > 0:
                    entries_list_view.controls.clear()
                    container_content.controls.remove(entries_list_view)

                entries_list_view.controls.append(graph_temperature_element)
                entries_list_view.controls.append(graph_humidity_element)
                container_content.controls.append(entries_list_view)

            page.update()

        entries_title = flet.Row(
            controls=[
                flet.Text(value="Статистика и графики", style=TextStyle(size=17, weight=FontWeight.W_500)),
            ],
            spacing=12
        )

        data_choose_calendar = flet.DatePicker(
            first_date=datetime.datetime(year=2000, month=10, day=1),
            last_date=datetime.datetime(year=2025, month=10, day=1),
            on_change=handle_change,
        )

        entries_list_view = flet.ListView(spacing=15, padding=10, width=500, height=300, controls=[])

        date_time_text = flet.Text(value="Текущая дата: Не выбранная дата")

        container_content = flet.Column(controls=[
            flet.Column(controls=[
                flet.Column(controls=[
                    entries_title,
                    flet.Row(controls=[date_time_text, data_choose_calendar], spacing=5),
                    flet.TextButton(text="Выбрать дату", icon=Icons.CALENDAR_TODAY,
                                    on_click=lambda e: page.open(data_choose_calendar))
                ]),
            ], spacing=15),
        ])

        return flet.Container(
            key="right_container",
            width=500, height=450,
            content=container_content
        )
