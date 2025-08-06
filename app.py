import datetime
import enum

import dash
import dash_mantine_components as dmc
import pandas as pd

import utils

app = dash.Dash(__name__)
app.title = "ROI Calculator"


class Duration(enum.StrEnum):
    MONTHS = enum.auto()
    YEARS = enum.auto()


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
                dmc.Group(
                    [
                        dmc.NumberInput(
                            label="Monthly Return Rate (%)",
                            id="monthly-rate",
                            value=1.6,
                            step=0.1,
                        ),
                        dmc.NumberInput(
                            label="Annual Return Rate (%)",
                            id="annual-rate",
                            value=utils.monthly2annual(1.6),
                            step=1,
                        ),
                    ]
                ),
                dmc.NumberInput(
                    label="Monthly Contribution ($)",
                    id="contribution",
                    value=100,
                    step=50,
                    min=0,
                ),
                dmc.Group(
                    [
                        dmc.NumberInput(
                            label="Investment Duration",
                            id="duration_value",
                            value=12,
                            step=1,
                            min=1,
                        ),
                        dmc.Select(
                            id="duration_period",
                            data=list(Duration),
                            value=Duration.MONTHS,
                        ),
                    ],
                    align="end",
                ),
            ]
        )
    ],
    shadow="md",
    radius="md",
    p="md",
    withBorder=True,
)

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    children=dmc.Container(
        [
            dmc.Center(dmc.Title("ROI Calculator", order=1, my="md")),
            inputs,
            dash.dcc.Graph(id="roi-graph", config={"displayModeBar": False}),
            dmc.Center(dmc.Text(id="final-value", size="lg")),
        ]
    ),
)


@app.callback(
    dash.Output("monthly-rate", "value"),
    dash.Output("annual-rate", "value"),
    dash.Input("monthly-rate", "value"),
    dash.Input("annual-rate", "value"),
    prevent_initial_callback=True,
)
def update_equivalent_rate(monthly_rate, annual_rate):
    match dash.ctx.triggered_id:
        case "monthly-rate":
            return dash.no_update, utils.monthly2annual(monthly_rate)
        case "annual-rate":
            return utils.annual2monthly(annual_rate), dash.no_update
        case _:
            return dash.no_update, dash.no_update


@app.callback(
    dash.Output("roi-graph", "figure"),
    dash.Output("final-value", "children"),
    dash.Input("initial", "value"),
    dash.Input("monthly-rate", "value"),
    dash.Input("contribution", "value"),
    dash.Input("duration_value", "value"),
    dash.Input("duration_period", "value"),
)
def update_graph(initial, rate, contribution, duration, duration_period):
    if "" in [initial, rate, contribution, duration]:
        return dash.no_update

    months = 12 * duration if duration_period == Duration.YEARS else duration
    dates = utils.date_ranges(months)
    balance = utils.calculate_balance(initial, months, rate / 100, contribution)
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
            # "title": {"text": "Investment Growth Over Time", "x": 0.5},
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
