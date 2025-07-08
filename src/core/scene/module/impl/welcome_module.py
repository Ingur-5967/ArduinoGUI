import flet
from flet.core.text_style import TextStyle
from flet.core.types import FontWeight

from src.core.scene.module.scene_module import SceneModule
from src.core.scene.scene import Scene


class WelcomeModule(SceneModule):

    def __init__(self):
        super().__init__("welcome_module", True)

    def init(self, page: flet.Page, scene: Scene) -> flet.Control:
        return flet.Container(
            key="right_navigation_board_container",
            width=500, height=450,
            content=flet.Column(controls=[
                flet.Text("Добро пожаловать!", style=TextStyle(weight=FontWeight.W_500)),
                flet.Text("Программа читает данные с Arduino и строит по ним статистику"),
                flet.Text("Перед началом выберите желаемый прослушиваемый COM-порт в настройках"),
                flet.Text(
                    "Вы можете сохранять собранные данные в виде файлов, строить графики по выбранным периодам из доступных, просматривать логи работы программы"),
                flet.Text(
                    "По умолчанию задержка между обращением к Arduino - 5min, но это можно изменить в настройках программы"),
            ]),
        )