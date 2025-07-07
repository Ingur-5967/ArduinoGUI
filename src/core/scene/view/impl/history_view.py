import flet

from src.core.exception.ModuleException import ModuleException
from src.core.scene.module.impl.board_module import BoardModule
from src.core.scene.module.impl.history_module import HistoryModule
from src.core.scene.scene import Scene
from src.core.scene.view.view import View


class HistoryView(View):

    def __init__(self):
        super().__init__("history_view")

    def load(self, scene: Scene, page: flet.Page) -> None:
        page.clean()

        scene.update(
            self,
            BoardModule(), HistoryModule()
        )

        history_component = next((module for module in scene.get_active_modules() if module.get_id() == "history_module"),
                              None)
        board_component = next((module for module in scene.get_active_modules() if module.get_id() == "board_module"),
                               None)

        if history_component is None or board_component is None:
            raise ModuleException("Invalid modules")

        page.add(flet.Row(controls=[board_component.init(page, scene), history_component.init(page, scene)], spacing=12))

        page.update()