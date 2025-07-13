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

                parsed_temperature_values = [int(data_container[section]['temperature']) for section in data_container.keys()]

                fig, ax = plt.subplots(figsize=(7, 4))

                start = pd.to_datetime(start_date_time_chart)
                end = pd.to_datetime(end_date_time_chart)

                if end <= start:
                    end += pd.Timedelta(days=1)

                plt.plot(list(data_container.keys()), parsed_temperature_values, linestyle='solid')

                ax.set_xlabel("Время замеров")
                ax.set_ylabel("Температура")
                ax.set_title("График изменения температуры")

                ax.grid(True)

                plt.xticks(rotation=45)

                fig.tight_layout()

                container_content.controls.append(MatplotlibChart(fig, expand=True))

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