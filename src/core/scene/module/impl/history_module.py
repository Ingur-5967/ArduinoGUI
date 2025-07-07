import flet
from flet.core.colors import Colors
from flet.core.text_style import TextStyle
from flet.core.types import FontWeight

from src.core.scene.module.scene_module import SceneModule
from src.core.scene.scene import Scene


class HistoryModule(SceneModule):

    def __init__(self):
        super().__init__("history_module", True)

    def init(self, page: flet.Page, scene: Scene) -> flet.Control:

        entries_counter_container = flet.Container(
            content=flet.Text(value="45 записей", color=Colors.WHITE, style=TextStyle(size=13, weight=FontWeight.W_400)),
            padding=flet.padding.all(5),
            border_radius=12,
            bgcolor=Colors.GREY
        )

        entries_title = flet.Row(
            controls=[
                flet.Text(value="Записи сбора данных", style=TextStyle(size=17, weight=FontWeight.W_500)),
                entries_counter_container
            ],
            spacing=12
        )

        return flet.Container(
            key="right_container",
            width=500, height=450,
            content=flet.Column(controls=[entries_title]),
        )