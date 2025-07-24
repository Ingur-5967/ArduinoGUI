import datetime

import flet
import pandas as pd
from flet.core.icons import Icons
<<<<<<< HEAD
=======
from flet.core.list_view import ListView
from flet.core.matplotlib_chart import MatplotlibChart
>>>>>>> 7ab033462ac10b281c8cd3e6c998dfe93ec76dd7
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

    def get_graphs(self, selected_time: str, temperature_symbol: str, temperature_value_converter=None) -> (MatplotlibChart, MatplotlibChart):

        setting_controller = SettingController()

        data_directory_path = setting_controller.get_parameter_by_key(SettingConstSection.DATA_DIRECTORY_STORAGE)

        if data_directory_path is None:
            pass

        data_file = File(data_directory_path.get_value_section(), FileNaming.DATA_FILE_NAME)

        if len(data_file.read()) == 0: pass

        file_steam_reader = data_file.read()

        sorted_date_time = list(map(lambda date: date.split(" ")[1], file_steam_reader["data"].keys()))

        start_date_time_chart, end_date_time_chart = sorted_date_time[0], sorted_date_time[-1]

        data_container = dict()

        for index, entry in enumerate(file_steam_reader["data"].keys()):

            entry_date = entry.split(" ")[0]
            entry_time = entry.split(" ")[1]

            if entry_date != selected_time: continue

            data_container[entry_time] = {
                "temperature": file_steam_reader["data"][f'{entry_date} {entry_time}']['temperature'],
                "humidity": file_steam_reader["data"][f'{entry_date} {entry_time}']['humidity'],
            }

        parsed_temperature_values = [
            float(data_container[section]['temperature']) if temperature_value_converter is None else float(
                temperature_value_converter(data_container[section]['temperature'])) for section in
            data_container.keys()]
        parsed_humidity_values = [float(data_container[section]['humidity']) for section in data_container.keys()]

        start = pd.to_datetime(start_date_time_chart)
        end = pd.to_datetime(end_date_time_chart)

        if end <= start:
            end += pd.Timedelta(days=1)

        graph_temperature_element = GraphTool(list(data_container.keys()),
                                              parsed_temperature_values).build_graph(
            "График изменения температуры", "Время замеров", f"Температура ({temperature_symbol})", start, end, (7, 4))
        graph_humidity_element = GraphTool(list(data_container.keys()), parsed_humidity_values).build_graph(
            "График изменения влажности", "Время замеров", "Влажность (%)", start, end, (7, 4))

        return graph_temperature_element, graph_humidity_element

    def init(self, page: flet.Page, scene: Scene) -> flet.Control:

        link_data_view_type = {
            "Цельсии": "Фаренгейты",
            "Фаренгейты": "Цельсии"
        }

        table_data_convertor = {
            "Цельсии": lambda temperature: float(temperature),
            "Фаренгейты": lambda temperature: float(float(temperature) * 9/5 + 32)
        }

        table_data_symbols = {
            "Цельсии": "C",
            "Фаренгейты": "F"
        }

        def change_view_type_data(e):
            variant_view_data.text = f"Вариант отображения: {link_data_view_type[e.control.text.split(" ")[-1]]}"

            variant_view_data.disabled = True
            page.update()

            entries_list_view.controls.clear()

            graph_temperature, graph_humidity = self.get_graphs(
                date_time_text.value.split(" ")[-1],
                table_data_symbols[e.control.text.split(" ")[-1]],
                table_data_convertor[e.control.text.split(" ")[-1]]
            )

            entries_list_view.controls.append(graph_temperature)
            entries_list_view.controls.append(graph_humidity)

            variant_view_data.disabled = False
            page.update()

        def handle_change(e):
            date_time_text.value = f"Текущая дата: {e.control.value.strftime('%m/%d/%Y')}"

            graph_temperature, graph_humidity = self.get_graphs(
                e.control.value.strftime('%m/%d/%Y'),
                table_data_symbols[variant_view_data.text.split(" ")[-1]],
                table_data_convertor[variant_view_data.text.split(" ")[-1]]
            )

            if len(entries_list_view.controls) > 0:
                entries_list_view.controls.clear()
                container_content.controls.remove(entries_list_view)

            entries_list_view.controls.append(graph_temperature)
            entries_list_view.controls.append(graph_humidity)
            container_content.controls.append(variant_view_data)
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

        variant_view_data = flet.TextButton(text="Тип отображения: Цельсии", icon=Icons.CHANGE_CIRCLE,
                                            on_click=change_view_type_data)

        container_content = flet.Column(controls=[
            flet.Column(controls=[
                flet.Column(controls=[
                    entries_title,
                    flet.Row(controls=[date_time_text, data_choose_calendar], spacing=5),
                    flet.TextButton(
                        text="Выбрать дату",
                        icon=Icons.CALENDAR_TODAY,
                        on_click=lambda e: page.open(data_choose_calendar)
                    )
                ]),
            ], spacing=15),
        ])

        return flet.Container(
            key="right_container",
            width=500, height=450,
            content=container_content
        )
