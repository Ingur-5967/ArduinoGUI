import flet
import pandas as pd
import matplotlib.pyplot as plt

from flet.core.matplotlib_chart import MatplotlibChart


class GraphTool:
    def __init__(self, x_values: list, y_values: list, ):

        if len(x_values) != len(y_values):
            raise ValueError("x_values and y_values must have same length")

        self.x_values = x_values
        self.y_values = y_values

    def build_graph(self, title, x_text, y_text, start_time_x, end_time_x, size_fig) -> MatplotlibChart:

        fig, ax = plt.subplots(figsize=size_fig)

        start = pd.to_datetime(start_time_x)
        end = pd.to_datetime(end_time_x)

        if end <= start:
            end += pd.Timedelta(days=1)

        plt.plot(self.x_values, self.y_values, linestyle='solid')

        ax.set_xlabel(x_text)
        ax.set_ylabel(y_text)
        ax.set_title(title)

        ax.grid(True)

        plt.xticks(rotation=45)

        fig.tight_layout()

        return MatplotlibChart(fig, ax)