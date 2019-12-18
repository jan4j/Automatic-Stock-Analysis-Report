# Import the standard modules
import pandas as pd
import pathlib

# Import the modules for the report pages
from pages.Header import Header, make_dash_table

# Import the dash modules
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# Get the path to relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

# Import the CSV data files created from yahoo module
df_fund_facts = pd.read_csv(DATA_PATH.joinpath("facts.csv"))
#df_fund_facts = pd.read_csv(DATA_PATH.joinpath("summary.csv"))
#df_graph = pd.read_csv(DATA_PATH.joinpath("df_graph.csv"))



# For the Facts table import the csv data file and round the values to three decimal places
df_facts = pd.read_csv(DATA_PATH.joinpath("facts.csv"), header=None).round(3)
df_facts
forwardPE=df_facts.loc[8,:]
forwardPEtwo=df_facts.iloc[8,:]

# Prepare the data for piechart
# Import the csv file with the enterprise value as pandas dataframe
df = pd.read_csv(DATA_PATH.joinpath("ev.csv"))
# Take the header of the pandas dataframe and define as variable label
labels = list(df)
labels.pop(0)
# Take the second row with the ev values without the first element of column and define as variable value
values = df.iloc[0,1:]

# The maximum and minimum enterprise value are determined, expressed in millions and stored in a string.
maxev=str(round(max(values/1000000),3))+" millions"
minev=str(round(min(values/1000000),3))+" millions"

# The ticker of the maximum and minimum enterprise value are determined with a loop. At first the first entry is determined as the maximum price.
# The for loop checks whether the following entries are higher resp. lower and if stores the highest resp. lowest value in a variable.
maxevticker=values.index[0]
for i in range(1, 3):
    if (values[i]>values[i-1]):
        maxevticker=values.index[i]
maxevticker=str(maxevticker)

minevticker=values.index[0]
for i in range(1, 3):
    if (values[i]<values[i-1]):
        minevticker=values.index[i]
minevticker=str(minevticker)

## Prepare the Bar plot with mean of monthly returns
df_summary = pd.read_csv(DATA_PATH.joinpath("summary.csv"))
labels1 = list(df_summary)
labels1.pop(0)
values1 = df_summary.iloc[1,1:]

# The mean minimum and maximum are determined, rounded on three decimal points and the according tickers are determined analogically to the enterprise value.
maxmean=round(max(values1),3)
minmean=round(min(values1),3)

maxmeanticker=values1.index[0]
for i in range(1, 3):
    if (values1[i]>values1[i-1]):
        maxmeanticker=values1.index[i]

minmeanticker=values1.index[0]
for i in range(1, 3):
    if (values1[i]<values1[i-1]):
        minmeanticker=values1.index[i]

minmaxmean=str(str(minmean) + " and " + str(maxmean))

# Prepare time series on bottom of page
df_graph = pd.read_csv(DATA_PATH.joinpath("prices.csv"))
labels2 = list(df_graph)
labels2.pop(0)
values2 = df_graph.iloc[1:,1:]

# Defintion of HTML layout
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
                                    This is an automatically generated report about individually selected stocks\
                                    The average monthly returns are between " + minmaxmean + " % (see barplot). \
                                    The firm with ticker " + maxevticker + " has the highest enterprise value, which is " + maxev +".\
                                    The firm " + minevticker + " has the lowest value (" + minev + "), which means it is the cheapest firm.\
                                    Warning: The ticker of the highest and lowest enterprise value can be wrong, if data is not complete.",

                                        style={"color": "#fffff"},
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
                                        ["Enterprise Value ($)"], className="subtitle padded"
                                    ),

                                    html.P([""], style={"color": "#7a7a7a"}),
                                    dcc.Graph(
                                        id="graph-5",
                                        figure={
                                            "data": [
                                                go.Pie(
                                                    # Input data of python program for pie diagam
                                                    labels=labels,
                                                    values=values,
                                                    # hole=.3,
                                                    # define the color for the pie chart
                                                    marker={'colors': ['rgb(95, 186, 143)',
                                                                       'rgb(38, 94, 186)',
                                                                       'rgb(76, 185, 173)',
                                                                       'rgb(162, 186, 92)',
                                                                       'rgb(130, 185, 170)',

                                                                       ]},
                                                )
                                            ],
                                            "layout": go.Layout(

                                                # Add plot sizes
                                                autosize=True,
                                                # legend_orientation="h",
                                                width=270,
                                                height=250,
                                                margin={
                                                    "r": 10,
                                                    "t": 10,
                                                    "b": 0,
                                                    "l": 50,
                                                },

                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),

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
                                                    x=labels1,
                                                    y=values1,
                                                    text=labels1,
                                                    textposition='auto',
                                                    showlegend=False,
                                                    marker={
                                                        "color": "#5fba8f",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2, }, },
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
                                                    "b": 15,
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
                        style={"margin-bottom": "5px"},
                    ),

                    # Row 4
                    html.Br([]),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Key Facts and Ratios"],
                                        className="subtitle padded",
                                    ),
                                    html.Table(
                                        make_dash_table(df_facts),
                                        className="row",
                                    ),
                                ],
                                className=" twelve columns",
                            )
                        ],
                        className="row ",
                    ),

                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Performance", className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph-4",
                                        figure={
                                            "data":[
                                            go.Scatter(x=df_graph['Date'], y=df_graph[labels2[0]],name=labels2[0]),
                                            go.Scatter(x=df_graph['Date'], y=df_graph[labels2[1]],name=labels2[1]),
                                            go.Scatter(x=df_graph['Date'], y=df_graph[labels2[2]],name=labels2[2]),
                                            go.Scatter(x=df_graph['Date'], y=df_graph[labels2[3]],name=labels2[3]),
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
                                                    "rangeslider": dict(visible=True),
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
