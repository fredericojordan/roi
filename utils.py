__all__ = (
    "add_tax_ranges",
    "annual2monthly",
    "calculate_balances",
    "monthly_date_range",
    "monthly2annual",
)

import datetime

import numpy as np
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go


def monthly2annual(rate: float) -> float:
    monthly_rate = 1 + rate / 100
    annual_rate = monthly_rate**12
    return (annual_rate - 1) * 100


def annual2monthly(rate: float) -> float:
    annual_rate = 1 + rate / 100
    monthly_rate = annual_rate ** (1 / 12)
    return (monthly_rate - 1) * 100


def add_tax_ranges(figure: go.Figure, dates: list[datetime.datetime]) -> None:
    colors = ["red", "darkorange", "yellow", "green"]
    opacity = 0.1
    t0, t_final = dates[0], dates[-1]
    t1 = t0 + datetime.timedelta(days=180)
    t2 = t0 + datetime.timedelta(days=360)
    t3 = t0 + datetime.timedelta(days=720)
    total_days = (t_final - t0).days

    figure.add_vrect(
        x0=t0,
        x1=t_final if total_days < 180 else t1,
        line_width=0,
        fillcolor=colors[0],
        opacity=opacity,
    )
    if total_days < 180:
        return

    figure.add_vrect(
        x0=t1,
        x1=t_final if total_days < 360 else t2,
        line_width=0,
        fillcolor=colors[1],
        opacity=opacity,
    )
    if total_days < 360:
        return

    figure.add_vrect(
        x0=t2,
        x1=t_final if total_days < 720 else t3,
        line_width=0,
        fillcolor=colors[2],
        opacity=opacity,
    )

    if total_days > 720:
        figure.add_vrect(
            x0=t3, x1=t_final, line_width=0, fillcolor=colors[3], opacity=opacity
        )


def monthly_date_range(months: int) -> np.ndarray:
    now = datetime.datetime.now()
    return np.array([now + relativedelta(months=i) for i in range(months + 1)])


def calculate_balances(
    initial: int | float, months: int, rate: float, contribution: int | float
) -> np.ndarray:
    """
    <180 days -> 22.5%
    181-360 days -> 20%
    361-720 days -> 17.5%
    >720 days -> 15%
    """
    balance = [initial]
    for i in range(1, months + 1):
        new_value = balance[-1] * (1 + rate) + contribution
        balance.append(int(100 * new_value) / 100)
    return np.array(balance), np.array(balance)
