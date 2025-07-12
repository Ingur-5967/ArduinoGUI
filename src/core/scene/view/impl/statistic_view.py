import flet

from src.core.exception.ModuleException import ModuleException
from src.core.scene.module.impl.board_module import BoardModule
from src.core.scene.module.impl.statistic_module import StatisticModule
from src.core.scene.scene import Scene
from src.core.scene.view.view import View


class StatisticView(View):

    def __init__(self):
        super().__init__("statistic_view")

    def load(self, scene: Scene, page: flet.Page) -> None:
        page.clean()

        scene.update(
            self,
            BoardModule(),
            StatisticModule()
        )

        statistic_module = next((module for module in scene.get_active_modules() if module.get_id() == "statistic_module"), None)
        board_component = next((module for module in scene.get_active_modules() if module.get_id() == "board_module"), None)

        if board_component is None or statistic_module is None:
            raise ModuleException("Invalid modules")

        page.add(flet.Row(controls=[board_component.init(page, scene), statistic_module.init(page, scene)]))

        page.update()