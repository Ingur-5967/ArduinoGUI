import flet

from src.core.exception.ModuleException import ModuleException
from src.core.scene.module.scene_module import SceneModule
from src.core.scene.scene import Scene


class SceneStorage:

    def __init__(self):
        self.scenes = list[SceneModule]()

    def put_module(self, module: SceneModule) -> None:
        self.scenes.append(module)

    def get_module_by_id(self, module_id: str) -> SceneModule | None:
        return list(filter(lambda module: module.get_id() == module_id, self.scenes))[0]

    def get_modules(self) -> list[SceneModule]:
        return self.scenes

def load_view(scene: Scene, page: flet.Page, view_id: str) -> None:
    scene.clean_active_modules()
    try:
        scene.get_view_by_id(view_id).load(scene, page)
    except ModuleException:
        page.add(flet.Text(value="Modules not loaded because of exception!"))