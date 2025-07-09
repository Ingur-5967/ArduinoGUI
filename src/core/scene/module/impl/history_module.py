import datetime

import flet
from flet.core.colors import Colors
from flet.core.icons import Icons
from flet.core.text_style import TextStyle
from flet.core.types import FontWeight

from src.core.scene.module.scene_module import SceneModule
from src.core.scene.scene import Scene


class HistoryModule(SceneModule):

    def __init__(self):
        super().__init__("history_module", True)

    def init(self, page: flet.Page, scene: Scene) -> flet.Control:

        def handle_change(e):

            date_time_text.value = f"Текущая дата: {e.control.value.strftime('%m/%d/%Y')}"
            page.update()

        entries_counter_container = flet.Container(
            content=flet.Text(value="45 записей", color=Colors.WHITE, style=TextStyle(size=13, weight=FontWeight.W_400)),
            padding=flet.padding.all(5),
            border_radius=12,
            bgcolor=Colors.GREY
        )

        entries_title = flet.Row(
            controls=[
                flet.Text(value="Записи сбора данных", style=TextStyle(size=17, weight=FontWeight.W_500)),
                entries_counter_container
            ],
            spacing=12
        )

        data_choose_calendar = flet.DatePicker(
                    first_date=datetime.datetime(year=2000, month=10, day=1),
                    last_date=datetime.datetime(year=2025, month=10, day=1),
                    on_change=handle_change,
        )

        date_time_text = flet.Text(value="Текущая дата: Не выбранная дата")

        entries_list_view = flet.ListView(spacing=15, padding=20, width=500, height=150, controls=[
            flet.Text(value=f"Content-{i}", bgcolor=Colors.GREY) for i in range(10)]
        )

        return flet.Container(
            key="right_container",
            width=500, height=450,
            content=flet.Column(controls=[
                flet.Column(controls=[
                    entries_title,
                    flet.Row(controls=[date_time_text, data_choose_calendar], spacing=10),
                    flet.TextButton(text="Выбрать дату", icon=Icons.CALENDAR_TODAY, on_click=lambda e: page.open(data_choose_calendar))
                ]),
                entries_list_view
            ], spacing=25)
        )