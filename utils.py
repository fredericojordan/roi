__all__ = (
    "annual2monthly",
    "calculate_balance",
    "date_ranges",
    "monthly2annual",
)

import datetime

import numpy as np
from dateutil.relativedelta import relativedelta


def monthly2annual(rate: float) -> float:
    monthly_rate = 1 + rate / 100
    annual_rate = monthly_rate**12
    return (annual_rate - 1) * 100


def annual2monthly(rate: float) -> float:
    annual_rate = 1 + rate / 100
    monthly_rate = annual_rate ** (1 / 12)
    return (monthly_rate - 1) * 100


def date_ranges(months: int) -> np.ndarray:
    now = datetime.datetime.now()
    return np.array([now + relativedelta(months=i) for i in range(months + 1)])


def calculate_balance(
    initial: int | float, months: int, rate: float, contribution: int | float
) -> np.ndarray:
    balance = [initial]
    for i in range(1, months + 1):
        new_value = balance[-1] * (1 + rate) + contribution
        balance.append(int(100 * new_value) / 100)
    return np.array(balance)
