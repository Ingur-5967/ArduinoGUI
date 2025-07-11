import datetime
import os.path

import flet
from flet.core.icons import Icons
from flet.core.text_style import TextStyle
from flet.core.types import FontWeight

from src.core.arduino_receiver import ArduinoReceiver
from src.core.container.file_storage import FileNaming
from src.core.exception.ArduinoStreamReaderException import ArduinoStreamReaderException
from src.core.port_provider import PortService
from src.core.scene.file_service import File
from src.core.scene.module.scene_module import SceneModule
from src.core.scene.scene import Scene
from src.core.setting_controller import SettingController, SettingConstSection


class HomeModule(SceneModule):

    def __init__(self):
        super().__init__("home_module", True)
        self.config = SettingController()

    def init(self, page: flet.Page, scene: Scene) -> flet.Control:
        def refresh_data_stream_reader(e):
            data_stream_reader_title.value = f"Полученные данные за {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            refresh_button.disabled = True
            page.update()

            try:
                updated_received_data = ArduinoReceiver().read_stream_data()
                temp_value, humidity_value = updated_received_data[0].get_value(), updated_received_data[1].get_value()
            except ArduinoStreamReaderException:
                temp_value, humidity_value = "Failed to read received data", "Failed to read received data"

            temperature_text.value = f"Температура: {temp_value}"
            humidity_text.value = f"Влажность: {humidity_value}"

            save_entry_button.disabled = temp_value.__contains__("Failed") or not humidity_value.__contains__("Failed")

            refresh_button.disabled = False

            page.update()

        def save_entry(e):
            data_config_path = self.config.get_parameter_by_key(SettingConstSection.DATA_DIRECTORY_STORAGE)

            if data_config_path.get_value_section() == 'None':
                print("Not found path (Empty)")
                return

            data_file = File(data_config_path.get_value_section(), FileNaming.DATA_FILE_NAME)

            if not data_file.exists():
                data_file.create("")

            lines = data_file.read()

            parsed_entry_date = data_stream_reader_title.value.split(" ")[3]
            parsed_entry_date_time = data_stream_reader_title.value.split(" ")[4]
            parsed_entry_temperature = temperature_text.value.split(" ")[1]
            parsed_entry_humidity = humidity_text.value.split(" ")[1]

            lines['data'][f'{parsed_entry_date} {parsed_entry_date_time}'] = {
                'temperature': parsed_entry_temperature,
                'humidity': parsed_entry_humidity
            }

            data_file.write(lines)

        warning_text = flet.Text(
            value="Невозможно открыть поток чтения данных, так как прослушиваемый порт Arduino не определился автоматически!\n\n"
                  "Возможно, у вас нет подключенных устройст или их больше одного\nПерейдите в настройки, чтобы принудительно изменить COM-порт"

        )

        data_stream_reader_title = flet.Text(
            value=f"Полученные данные за {datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}",
            style=TextStyle(size=15, weight=FontWeight.W_400)
        )

        temp_value = None
        humidity_value = None
        try:
            arduino_received_data = ArduinoReceiver().read_stream_data()
            temp_value, humidity_value = arduino_received_data[0].get_value(), arduino_received_data[1].get_value()
        except:
            temp_value, humidity_value = "Failed to read received data", "Failed to read received data"

        temperature_text = flet.Text(
            value=f"Температура: {temp_value}",
            style=TextStyle(size=17, weight=FontWeight.W_500)
        )
        humidity_text = flet.Text(
            value=f"Влажность: {humidity_value}",
            style=TextStyle(size=17, weight=FontWeight.W_500)
        )

        refresh_button = flet.IconButton(icon=Icons.REFRESH, on_click=refresh_data_stream_reader)

        save_entry_button = flet.TextButton(
            text="Сохранить запись",
            icon=Icons.SAVE,
            on_click=save_entry,
            disabled=temp_value.__contains__("Failed") or not humidity_value.__contains__("Failed")
        )

        reader_application_body = flet.Column(
            controls=[
                flet.Row(
                    controls=[
                        data_stream_reader_title, refresh_button,
                    ]
                ),
                flet.Column(
                    controls=[
                        flet.Row(
                            controls=[
                                flet.Icon(name=Icons.SEVERE_COLD),
                                temperature_text
                            ]
                        ),
                        flet.Row(
                            controls=[
                                flet.Icon(name=Icons.CLOUD),
                                humidity_text
                            ]
                        ),
                        flet.Row(
                            controls=[
                                save_entry_button
                            ]
                        )
                    ],
                    spacing=19
                )
            ],
            spacing=15,
        )

        information_body = flet.Column(
            controls=[
                flet.Text(
                    value=f"Прослушиваемый порт: {PortService().get_arduino_ports()[0].get_port_name() if len(PortService().get_arduino_ports()) != 0 else "Нет активного порта"}",
                    style=TextStyle(weight=FontWeight.W_500, size=16)
                ),
                reader_application_body if len(PortService().get_arduino_ports()) > 0 else warning_text

            ],
            spacing=25
        )

        return flet.Container(
            key="right_container",
            width=500, height=450,
            content=flet.Column(controls=[information_body]),
        )
