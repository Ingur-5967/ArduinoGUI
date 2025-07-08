
class Scene:
    def __init__(self):
        self.active_modules = list()
        self.views = []
        self.active_view = None


    def update(self, view, *modules):
        self.active_view = view

        if view not in self.views:
            self.views.append(view)

        for module in modules:
            self.active_modules.append(module)

    def delete_module(self, module):
        self.active_modules.remove(module)

    def get_active_modules(self) -> list:
        return self.active_modules

    def get_views(self):
        return self.views

    def get_view_by_id(self, view_id: str):
        return next((view for view in self.views if view.get_view_id() == view_id), None)

    def clean_active_modules(self):
        self.active_modules.clear()

    def get_active_view(self):
        return self.active_view