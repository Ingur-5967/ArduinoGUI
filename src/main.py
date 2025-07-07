import flet
from flet.core.buttons import ButtonStyle
from flet.core.colors import Colors
from flet.core.icons import Icons
from flet.core.page import Page
from flet.core.text_style import TextStyle
from flet.core.types import FontWeight

from src.src.port_provider import PortService

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
        right_board_container.content = flet.Column(
            controls=[
                flet.Text(
                    value=f"Прослушиваемый порт: {PortService().get_arduino_ports()[0] if len(PortService().get_arduino_ports()) > 1 else "Нет активного порта"}",
                    style=TextStyle(weight=FontWeight.W_500, size=16)
                )
            ]
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
        page.clean()
        right_board_container.content = flet.Column(
            controls=[
                flet.Text("Вы перешли на настройки!"),
                flet.Text("Вы перешли на настройки!"),
                flet.Text("Вы перешли на настройки!"),
                flet.Text("Вы перешли на настройки!")
            ]
        )
        page.add(flet.Row(controls=[application_body]))
        page.update()


    home_button = flet.TextButton(
                    key="home_navigation_button",
                    text="Главная",
                    icon=Icons.HOME,
                    style=ButtonStyle(icon_size=25, text_style=TextStyle(size=17, weight=FontWeight.W_500)),
                    on_click=route_to_home,
    )

    statistic_button = flet.TextButton(
                    key="statistic_navigation_button",
                    text="Статистика",
                    icon=Icons.QUERY_STATS,
                    style=ButtonStyle(icon_size=25, text_style=TextStyle(size=17, weight=FontWeight.W_500)),
                    on_click=route_to_statistic,
    )

    settings_button = flet.TextButton(
                    key="home_navigation_button",
                    text="Настройки",
                    icon=Icons.SETTINGS,
                    style=ButtonStyle(icon_size=25, text_style=TextStyle(size=17, weight=FontWeight.W_500)),
                    on_click=route_to_settings,
    )

    left_board_column = flet.Column(
        key="left_navigation_board_column",
        height=450,
        width=200,
        controls=[
            flet.Row(controls=[home_button]),
            flet.Row(controls=[statistic_button]),
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