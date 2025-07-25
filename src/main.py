import asyncio
import datetime
from ctypes import *

import flet
from flet.core.page import Page

from src.core.arduino_receiver import ArduinoReceiver
from src.core.container.file_storage import FileNaming
from src.core.exception.ArduinoStreamReaderException import ArduinoStreamReaderException
from src.core.port_provider import PortService
from src.core.scene.file_service import File
from src.core.scene.scene import Scene
from src.core.scene.scene_service import load_view
from src.core.scene.view.impl.history_view import HistoryView
from src.core.scene.view.impl.main_view import HomeView
from src.core.scene.view.impl.settings_view import SettingsView
from src.core.scene.view.impl.start_view import StartView
from src.core.scene.view.impl.statistic_view import StatisticView
from src.core.setting_controller import SettingController, SettingConstSection


class Application:
    def __init__(self, scene: Scene):
        self.scene = scene
        self.scene.init_views(StartView(), HomeView(), SettingsView(), HistoryView(), StatisticView())
        self.ignore_notification = False
        self.audio_player = CDLL("core/arduinoDll.dll")
        self.audio_player.play_alarm.argtypes = [c_wchar_p]

    async def main(self, page: Page):
            page.title = "Метеостанция"

            setting_controller = SettingController()
            port_controller = PortService()

            com_port = "None"
            if len(port_controller.get_arduino_ports()) == 1:
                com_port = port_controller.get_arduino_ports()[0].get_port_name()

            setting_controller.set_parameter_and_save(
                SettingConstSection.SELECTED_LISTEN_COM_PORT,
                com_port
            )

            page.window.width = 800
            page.window.height = 600
            page.window.max_width = 800
            page.window.max_height = 600

            page.window.min_width = 800
            page.window.min_height = 600

            load_view(self.scene, page, "start_view")

            while True:
                cooldown = SettingController().get_parameter_by_key(SettingConstSection.COOLDOWN_STREAM_READER).get_value_section()
                active_port = SettingController().get_parameter_by_key(SettingConstSection.SELECTED_LISTEN_COM_PORT).get_value_section()
                arduino_receiver = ArduinoReceiver()
                def close_and_ignore_banner(e):
                    page.close(banner)
                    self.ignore_notification = True
                    self.opened_notification = False

                def close_banner(e):
                    page.close(banner)
                    self.opened_notification = False

                close_and_ignore_banner_button_style = flet.ButtonStyle(color=flet.Colors.RED)
                close_banner_button_style = flet.ButtonStyle(color=flet.Colors.BLUE)
                banner = flet.Banner(
                    bgcolor=flet.Colors.AMBER_100,
                    leading=flet.Icon(flet.Icons.WARNING_ROUNDED, color=flet.Colors.AMBER, size=40),
                    content=flet.Text(),
                    actions=[
                        flet.TextButton(
                            text="Ignore", style=close_and_ignore_banner_button_style, on_click=close_and_ignore_banner
                        ),
                        flet.TextButton(
                            text="Close", style=close_banner_button_style, on_click=close_banner
                        )
                    ]
                )
                if (cooldown is None or active_port is None) or len(port_controller.get_arduino_ports()) == 0 or not arduino_receiver._check_connection():
                    await asyncio.sleep(1)
                else:
                    try:
                        forced_received_arduino_data = ArduinoReceiver().read_stream_data()
                    except ArduinoStreamReaderException:
                        continue

                    file_stream_writer = File(setting_controller.get_parameter_by_key(SettingConstSection.DATA_DIRECTORY_STORAGE).get_value_section(), FileNaming.DATA_FILE_NAME)
                    file_lines = file_stream_writer.read()
                    received_temperature = forced_received_arduino_data[0].get_value()
                    received_humidity = forced_received_arduino_data[1].get_value()
                    timing = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                    file_lines['data'][f'{timing.split(" ")[0]} {timing.split(" ")[1]}'] = {
                        'temperature': received_temperature if received_temperature[-1].isdigit() else received_temperature[0:len(received_temperature) - 2],
                        'humidity': received_humidity if received_humidity[-1].isdigit() else received_humidity[0:len(received_humidity) - 1]
                    }

                    file_stream_writer.write(file_lines)

                    if not self.ignore_notification and int(received_temperature[:2]) >= 30:
                        self.audio_player.play_alarm("assets/doop.wav")
                        banner.content = flet.Text(
                            value="Зафиксирована пороговая температура (30). Рекомендуем переместиться ближе к водоемам"
                        )
                        page.add(banner)
                        page.open(banner)

                    await asyncio.sleep(float(cooldown) * 60)

    def get_scene_instance(self):
        return self.scene


application = Application(Scene())

flet.app(target=application.main)
