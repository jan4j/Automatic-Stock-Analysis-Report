import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from utils import Header, make_dash_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()


df_fund_facts = pd.read_csv(DATA_PATH.joinpath("facts.csv"))
#df_fund_facts = pd.read_csv(DATA_PATH.joinpath("summary.csv"))
df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))
df_current_prices = pd.read_csv(DATA_PATH.joinpath("df_current_prices.csv"))
df_hist_prices = pd.read_csv(DATA_PATH.joinpath("df_hist_prices.csv"))
df_avg_returns = pd.read_csv(DATA_PATH.joinpath("df_avg_returns.csv"))
df_after_tax = pd.read_csv(DATA_PATH.joinpath("df_after_tax.csv"))
df_recent_returns = pd.read_csv(DATA_PATH.joinpath("df_recent_returns.csv"))
#df_graph = pd.read_csv(DATA_PATH.joinpath("df_graph.csv"))





#for piechart
#data for overview
df = pd.read_csv(DATA_PATH.joinpath("summary.csv"))
#take the header of the pandasdataframe
labels = list(df)
labels.pop(0)
#takes the second row of df and from this row starts with second dolumn
values = df.iloc[1,1:]

df_graph = pd.read_csv(DATA_PATH.joinpath("prices.csv"))
labels2 = list(df_graph)
labels2.pop(0)
values2 = df_graph.iloc[1:,1:]




def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 2
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Summary"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    In your Portfolio are the following stocks... \
                                    the Calibre Index Fund is a low-cost way to gain diversified exposure \
                                    to the U.S. equity market. The fund offers exposure to 500 of the \
                                    largest U.S. companies, which span many different industries and \
                                    account for about three-fourths of the U.S. stock market’s value. \
                                    The key risk for the fund is the volatility that comes with its full \
                                    exposure to the stock market. Because the Calibre Index Fund is broadly \
                                    diversified within the large-capitalization market, it may be \
                                    considered a core equity holding in a portfolio.",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),

                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Asset Facts"], className="subtitle padded"
                                    ),
                                    html.Table(make_dash_table(df_fund_facts)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Average Monthly Returns",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-1",
                                        figure={
                                            "data": [
                                                go.Bar(
                                                    x=labels,
                                                    y=values,
                                                    text=labels,
                                                    textposition='auto',
                                                    showlegend=False,
                                                    marker={
                                                        "color": "#97151c",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,},},
                                                ),

                                            ],
                                            "layout": go.Layout(
                                                autosize=False,
                                                bargap=0.35,
                                                font={"family": "Raleway", "size": 10},
                                                height=200,
                                                hovermode="closest",
                                                legend={
                                                    "x": -0.0228945952895,
                                                    "y": -0.189563896463,
                                                    "orientation": "h",
                                                    "yanchor": "top",
                                                },
                                                margin={
                                                    "r": 0,
                                                    "t": 25,
                                                    "b": 20,
                                                    "l": 15,
                                                },
                                                showlegend=True,
                                                title="",
                                                width=330,
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [-0.5, 4.5],
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "category",
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [0, 22.9789473684],
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "60px"},
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Performance", className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph-4",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    #test this is the date line
                                                    x=df_graph["Date"],
                                                    #this is the closing prices
                                                    y=df_graph["AAPL"],
                                                    line={"color": "#97151c"},
                                                    mode="lines",
                                                    name="AAPL",
                                                ),
                                                go.Scatter(
                                                    x=df_graph["Date"],
                                                    #second graph with opening price
                                                    y=df_graph["GOOG"],
                                                    line={"color": "#b5b5b5"},
                                                    mode="lines",
                                                    name="GOOG",
                                                ),
                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                width=720,
                                                height=300,
                                                font={"family": "Raleway", "size": 10},
                                                margin={
                                                    "r": 30,
                                                    "t": 30,
                                                    "b": 30,
                                                    "l": 30,
                                                },
                                                showlegend=True,
                                                titlefont={
                                                    "family": "Raleway",
                                                    "size": 10,
                                                },
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [
                                                        "2007-12-31",
                                                        "2018-03-06",
                                                    ],
                                                    "rangeselector": {
                                                        "buttons": [
                                                            {
                                                                "count": 1,
                                                                "label": "1Y",
                                                                "step": "year",
                                                                "stepmode": "backward",
                                                            },
                                                            {
                                                                "count": 3,
                                                                "label": "3Y",
                                                                "step": "year",
                                                                "stepmode": "backward",
                                                            },
                                                            {
                                                                "count": 5,
                                                                "label": "5Y",
                                                                "step": "year",
                                                            },
                                                            {
                                                                "count": 10,
                                                                "label": "10Y",
                                                                "step": "year",
                                                                "stepmode": "backward",
                                                            },
                                                            {
                                                                "label": "All",
                                                                "step": "all",
                                                            },
                                                        ]
                                                    },
                                                    "showline": True,
                                                    "type": "date",
                                                    "zeroline": False,
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [
                                                        18.6880162434,
                                                        278.431996757,
                                                    ],
                                                    "showline": True,
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",

                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
