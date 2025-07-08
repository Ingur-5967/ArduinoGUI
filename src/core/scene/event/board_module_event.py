import flet

from src.core.scene.event.event import ModuleEvent
from src.core.scene.scene import Scene
from src.core.scene.scene_service import SceneService


class BoardModuleEvent(ModuleEvent):

    def __init__(self):
        super().__init__("board_module_event")
        self.scene_service = SceneService()

    def route_to_home(self, scene: Scene, page: flet.Page):
        self.scene_service.load_view(scene, page, "home_view")

    def route_to_statistic(self, e):
        pass


    def route_to_settings(self, e):
        pass