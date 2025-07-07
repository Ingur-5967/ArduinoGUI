import datetime
import glob
import sys
import time

import flet
from flet.core.alignment import Alignment
from flet.core.icons import Icons
from flet.core.page import Page
from flet.core.text_style import TextStyle, TextDecoration
from flet.core.types import FontWeight

import serial.tools.list_ports


def main(page: Page):

    page.title = "Arduino receiver signals"
    page.window.width = 800
    page.window.height = 600

    page.window.max_width = 800
    page.window.max_height = 600

    text_field = flet.Text(
       value=f"Данные за {datetime.datetime.now()}",
        size = 17,
        weight=FontWeight.W_400
    )

    refresh_data_button = flet.IconButton(
        icon = Icons.REFRESH,

    )

    com_port_selector = flet.Dropdown(
        label="COM-Порты",
        width=250,
        options=[flet.DropdownOption(text=port) for port, desc, hwid in sorted(serial.tools.list_ports.comports())]

    )

    history_weather_logs = flet.IconButton(
        icon = Icons.HISTORY
    )

    temperature_bar_information = flet.Text(
        value="Температура 13℃",
    )
    cloud_bar_information = flet.Text(
        value="Влажность 13 г/м3",
    )

    page.add(
        com_port_selector,
        flet.Row(
            controls=[text_field, refresh_data_button, history_weather_logs]
        ),
        flet.Row(
            controls=[flet.Icon(name=Icons.SEVERE_COLD), temperature_bar_information]
        ),
        flet.Row(
            controls=[flet.Icon(name=Icons.CLOUD), cloud_bar_information]
        )
    )

    page.update()

flet.app(target=main)