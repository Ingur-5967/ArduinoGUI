import flet
from flet.core.page import Page

from src.core.scene.scene import Scene
from src.core.scene.scene_service import load_view
from src.core.scene.view.impl.history_view import HistoryView
from src.core.scene.view.impl.main_view import HomeView
from src.core.scene.view.impl.settings_view import SettingsView
from src.core.scene.view.impl.start_view import StartView


class Application:
    def __init__(self, scene: Scene):
        self.scene = scene
        self.scene.init_views(StartView(), HomeView(), SettingsView(), HistoryView())

    def main(self, page: Page):
        page.title = "Метеостанция"

        page.window.width = 800
        page.window.height = 600
        page.window.max_width = 800
        page.window.max_height = 600

        page.window.min_width = 800
        page.window.min_height = 600

        load_view(self.scene, page, "start_view")

    def get_scene_instance(self):
        return self.scene

application = Application(Scene())

flet.app(target=application.main)