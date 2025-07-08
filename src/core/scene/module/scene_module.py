import abc
from abc import ABC

import flet

from src.core.scene.scene import Scene


class SceneModule(ABC):

    def __init__(self, module_id: str, forced_clean: bool = False):
        self.module_id = module_id
        self.forced_clean = forced_clean

    @abc.abstractmethod
    def init(self, page: flet.Page, scene: Scene) -> flet.Control:
        pass

    def get_id(self) -> str:
        return self.module_id

    def is_forced_clean(self) -> bool:
        return self.forced_clean