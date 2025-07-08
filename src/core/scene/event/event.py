import flet

from src.core.scene.scene import Scene


class ModuleEvent:

    def __init__(self, event_id: str):
        self.event_id = event_id

    def invoke(self, method_name, scene: Scene, page: flet.Page):
        self.__class__.__call__(method_name, scene, page)

    def get_event_id(self) -> str:
        return self.event_id

class EventStorage:
    def __init__(self):
        self.event_storage = list[ModuleEvent]()

    def store_event(self, event: ModuleEvent):
        self.event_storage.append(event)

    def get_event(self, event_id: str) -> ModuleEvent:
        for event in self.event_storage:
            if event.get_event_id() != event_id: continue
            return event
