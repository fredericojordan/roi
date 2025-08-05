import datetime

import dash
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

app = dash.Dash(__name__)
app.title = "ROI Calculator"


inputs = dmc.Paper(
    [
        dmc.Stack(
            [
                dmc.NumberInput(
                    label="Initial Investment ($)",
                    id="initial",
                    value=1000,
                    step=100,
                    min=0,
                ),
                dmc.NumberInput(
                    label="Monthly Return Rate (%)",
                    id="rate",
                    value=2,
                    step=0.1,
                ),
                dmc.NumberInput(
                    label="Monthly Contribution ($)",
                    id="contribution",
                    value=100,
                    step=50,
                    min=0,
                ),
                dmc.NumberInput(
                    label="Investment Duration (months)",
                    id="months",
                    value=12,
                    step=1,
                    min=1,
                ),
            ]
        )
    ],
    shadow="md",
    radius="md",
    p="md",
    withBorder=True,
    mb="xl",
)

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    children=dmc.Container(
        [
            dmc.Center(dmc.Title("ROI Calculator", order=1, my="md")),
            inputs,
            dash.dcc.Graph(id="roi-graph", config={"displayModeBar": False}),
            dmc.Center(dmc.Text(id="final-value", size="lg", mt="lg")),
        ]
    ),
)


def date_ranges(months: int) -> np.ndarray:
    now = datetime.datetime.now()
    return np.array([now + relativedelta(months=i) for i in range(months + 1)])


def calculate_balance(
    initial: float, months: int, rate: float, contribution: float
) -> np.ndarray:
    balance = [initial]
    for i in range(1, months + 1):
        new_value = balance[-1] * (1 + rate) + contribution
        balance.append(int(100 * new_value) / 100)
    return np.array(balance)


@app.callback(
    dash.Output("roi-graph", "figure"),
    dash.Output("final-value", "children"),
    dash.Input("initial", "value"),
    dash.Input("rate", "value"),
    dash.Input("contribution", "value"),
    dash.Input("months", "value"),
)
def update_graph(initial, rate, contribution, months):
    if not (initial and rate and contribution and months):
        return dash.no_update

    dates = date_ranges(months)
    balance = calculate_balance(initial, months, rate / 100, contribution)
    df = pd.DataFrame(
        {
            "Month": dates,
            "Value ($)": balance,
        }
    )
    figure = {
        "data": [
            {
                "x": df["Month"],
                "y": df["Value ($)"],
                "type": "line",
                "name": "Investment Growth",
            }
        ],
        "layout": {
            "title": {"text": "Investment Growth Over Time", "x": 0.5},
            "xaxis": {"title": "Month"},
            "yaxis": {"title": "Investment Value ($)"},
        },
    }

    final_text = (
        f"{datetime.datetime.strftime(dates[-1], '%B, %Y')}: ${balance[-1]:,.2f}"
    )
    return figure, final_text


if __name__ == "__main__":
    app.run(debug=True, dev_tools_hot_reload=True)
