import flet

from src.core.exception.ModuleException import ModuleException
from src.core.scene.module.impl.board_module import BoardModule
from src.core.scene.module.impl.home_module import HomeModule
from src.core.scene.scene import Scene
from src.core.scene.view.view import View

class HomeView(View):

    def __init__(self):
        super().__init__("home_view")

    def load(self, scene: Scene, page: flet.Page):
        page.clean()

        scene.update(
            self,
            BoardModule(), HomeModule()
        )

        home_component = next((module for module in scene.get_active_modules() if module.get_id() == "home_module"), None)
        board_component = next((module for module in scene.get_active_modules() if module.get_id() == "board_module"), None)

        if home_component is None or board_component is None:
            raise ModuleException("Invalid modules")

        page.add(flet.Row(controls=[board_component.init(page, scene), home_component.init(page, scene)]))

        page.update()