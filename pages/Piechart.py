import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from utils import Header, make_dash_table
import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

#data for overview
df = pd.read_csv(DATA_PATH.joinpath("summary.csv"))
#take the header of the pandasdataframe
labels = list(df)

#takes the second row of df
values = df.iloc[1]

#labels = ['Oxygen', 'Hydrogen', 'Carbon_Dioxide', 'Nitrogen', 'Test', 'Test1']
#values = [4500, 2500, 1053, 500, 500, 234]

def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 4
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.P([""], style={"color": "#7a7a7a"}),
                            dcc.Graph(
                                id="graph-5",
                                figure={
                                    "data": [
                                        go.Pie(
                                        #Input data of python program for pie diagam
                                        labels=labels,
                                        values=values,
                                        #hole=.3,
                                            #define the color for the pie chart
                                        marker= {'colors': ['rgb(33, 75, 99)',
                                                            'rgb(79, 129, 102)',
                                                            'rgb(151, 179, 100)',
                                                            'rgb(175, 49, 35)',
                                                            'rgb(79, 129, 102)',
                                                            'rgb(151, 179, 100)',
                                                            'rgb(175, 49, 35)',
                                                            'rgb(79, 129, 102)',
                                                            'rgb(151, 179, 100)',
                                                            'rgb(175, 49, 35)',
                                                            'rgb(79, 129, 102)',
                                                            'rgb(151, 179, 100)',
                                                            'rgb(175, 49, 35)',
                                                            'rgb(79, 129, 102)',
                                                            'rgb(151, 179, 100)',
                                                            'rgb(175, 49, 35)',
                                                            'rgb(36, 73, 147)'

                                                            ]},
                                        )
                                    ],
                                    "layout": go.Layout(
                                        #Add title for plot
                                        title=" Portfolio Overview",

                                        #Add plot sizes
                                        autosize=False,
                                        width=700,
                                        height=700,
                                        margin={
                                            "r": 100,
                                            "t": 100,
                                            "b": 100,
                                            "l": 100,
                                        },

                                    ),
                                },
                                config={"displayModeBar": False},
                            ),
                        ],

                        className="row",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
