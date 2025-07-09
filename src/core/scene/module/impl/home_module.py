import datetime

import flet
from flet.core.icons import Icons
from flet.core.text_style import TextStyle
from flet.core.types import FontWeight

from src.core.arduino_receiver import ArduinoReceiver
from src.core.port_provider import PortService
from src.core.scene.module.scene_module import SceneModule
from src.core.scene.scene import Scene


class HomeModule(SceneModule):

    def __init__(self):
        super().__init__("home_module", True)

    def init(self, page: flet.Page, scene: Scene) -> flet.Control:
        def refresh_data_stream_reader(e):
            data_stream_reader_title.value = f"Полученные данные за {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            refresh_button.disabled = True
            page.update()

            updated_received_data = ArduinoReceiver().read_stream_data()

            temperature_text.value = f"Температура: {
                updated_received_data[0].get_value() if arduino_received_data[0] is not None else 'Runtime error'
            }"
            humidity_text.value = f"Влажность: {
                updated_received_data[1].get_value() if arduino_received_data[0] is not None else 'Runtime error'
            }"

            refresh_button.disabled = False

            page.update()

        warning_text = flet.Text(
            value="Невозможно открыть поток чтения данных, так как у вас не назначен прослушиваемый порт Arduino!\n\n"
                  "Перейдите в настройки, чтобы изменить COM-порт"
        )

        data_stream_reader_title = flet.Text(
                            value=f"Полученные данные за {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                            style=TextStyle(size=15, weight=FontWeight.W_400)
        )

        arduino_received_data = ArduinoReceiver().read_stream_data()

        temperature_text = flet.Text(
            value=f"Температура: {arduino_received_data[0].get_value() if not arduino_received_data.__contains__(None) else "{Runtime error}"}",
            style=TextStyle(size=17, weight=FontWeight.W_500)
        )
        humidity_text = flet.Text(value=f"Влажность: {arduino_received_data[1].get_value() if not arduino_received_data.__contains__(None) else "{Runtime error}"}", style=TextStyle(size=17, weight=FontWeight.W_500))

        refresh_button = flet.IconButton(icon=Icons.REFRESH, on_click=refresh_data_stream_reader)

        reader_application_body = flet.Column(
            controls=[
                flet.Row(
                    controls=[
                        data_stream_reader_title, refresh_button
                        flet.IconButton(icon=Icons.REFRESH, on_click=refresh_data_stream_reader)
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
                                flet.TextButton(text="Сохранить запись", icon=Icons.SAVE)
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