from __future__ import annotations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def create_df() -> (pd.Series | pd.DataFrame):
    with open(os.path.dirname(__file__) + "/../../fiis.json", "r") as json:
        return pd.read_json(
            json
        ).transpose()  # invert columns and rows


def plot_scatter(df, x_axis, y_axis):

    fig, ax = plt.subplots()

    df.plot(
        kind="scatter",
        x=x_axis,
        y=y_axis,
        title=f"{x_axis} X {y_axis}",
        ax=ax

    )

    ax.set_xlim(0, 1.5)
    ax.set_ylim(0, 100)

    plt.show()


if __name__ == '__main__':
    plot_scatter(create_df(), "lastdividend", "price")
