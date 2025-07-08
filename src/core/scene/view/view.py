import abc
from abc import ABC

import flet

from src.core.scene.scene import Scene


class View(ABC):

    def __init__(self, view_id: str):
        self.view_id = view_id

    @abc.abstractmethod
    def load(self, scene: Scene, page: flet.Page):
        pass

    def get_view_id(self) -> str:
        return self.view_id