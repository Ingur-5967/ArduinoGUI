import flet
from flet.core.buttons import ButtonStyle
from flet.core.colors import Colors
from flet.core.icons import Icons
from flet.core.text_style import TextStyle
from flet.core.types import FontWeight

from src.core.scene.module.scene_module import SceneModule
from src.core.scene.scene import Scene

class BoardModule(SceneModule):

    def __init__(self):
        super().__init__("board_module")

    def init(self, page: flet.Page, scene: Scene) -> flet.Control:

        home_button = flet.TextButton(
            key="home_navigation_button",
            text="Главная",
            icon=Icons.HOME,
            style=ButtonStyle(icon_size=25, text_style=TextStyle(size=17, weight=FontWeight.W_500)),
            width=150,
            on_click=lambda e: scene.get_view_by_id("home_view").load(scene, page)
        )

        statistic_button = flet.TextButton(
            key="statistic_navigation_button",
            text="Статистика",
            icon=Icons.QUERY_STATS,
            style=ButtonStyle(icon_size=25, text_style=TextStyle(size=17, weight=FontWeight.W_500)),
            width=150,
        )

        entries_button = flet.TextButton(
            key="entry_navigation_button",
            text="Записи",
            icon=Icons.EVENT,
            style=ButtonStyle(icon_size=25, text_style=TextStyle(size=17, weight=FontWeight.W_500)),
            width=150,
        )

        settings_button = flet.TextButton(
            key="home_navigation_button",
            text="Настройки",
            icon=Icons.SETTINGS,
            style=ButtonStyle(icon_size=25, text_style=TextStyle(size=17, weight=FontWeight.W_500)),
            width=150,
            on_click=lambda e: scene.get_view_by_id("settings_view").load(scene, page)
        )

        left_board_column = flet.Column(
            key="left_navigation_board_column",
            height=450,
            width=200,
            controls=[
                flet.Row(controls=[home_button]),
                flet.Row(controls=[statistic_button]),
                flet.Row(controls=[entries_button]),
                flet.Row(controls=[settings_button]),
            ],
            spacing=30
        )

        board_container = flet.Container(key="left_navigation_board_container", bgcolor=Colors.WHITE54,
                                                      content=left_board_column,
                                                      padding=flet.padding.only(left=15, top=25))

        return board_container