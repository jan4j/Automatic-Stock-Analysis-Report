import plotly.graph_objects as go
import pandas as pd
import datetime
import pandas_datareader.data as web
import dash_core_components as dcc
import dash_html_components as html

from datetime import timedelta, date
from pages.Header import Header, make_dash_table

# As the moving average analysis is done with only one variable, the user is asked to specify this.
# With the while and try function the code will ask the user to enter the ticker again in case if there was an error.
# The variable var2 is first set on 1 an changed to 0 as soon as entering the input was successful.
var2=1
while (var2==1):
    try:
        stockmov = input("Which stock would you like to use for the moving average analysis?: ")
        var2=0
    except:
        print("Something went wrong. Enter again the stock: ")
        var2=1

# The start and end date of the moving average are set.
start = datetime.datetime(2010, 1, 1)
end = datetime.datetime.now().date()

# The webreader imports the date from yahoo.com.
df = web.DataReader(stockmov, 'yahoo', start, end)
close_px = df['Adj Close']

# The first and second simple moving average are inserted with a window of 100 resp. 200.
mavg = close_px.rolling(window=100).mean()
mavg2 = close_px.rolling(window=200).mean()

# The index is substituted with a dateindex.
df = df.reset_index()
dateindex = pd.to_datetime(df.Date, format='%Y-%m-%d')

# This part of the code checks whether there has been a minimum or a maximum in the last 20 days. Firstly, the minimum resp. maximum in this period of time are determined.
min20 = min(mavg[-20:-1])
minminusone = mavg[-21]
minplusone = mavg[-19]
max20 = max(mavg[-20:-1])
maxminusone = mavg[-19]
maxplusone = mavg[-21]

# Afterwards, it is controlled whether the entries one day before and after have been higher or lower. This excludes that the minimum or maximum ar just the the first or last entry in the period of time.
# The latest entry cannot be included in the calculation because otherwise, the determination of the day after would not be possible. Only the first moving average is used for calculation.
if (minminusone > min20 and minplusone > min20):
    xx="There has been a minimum in the shorter moving average in the last 20 days. \
       According to a 'buy low  sell high' strategy, its a good moment to buy."
elif (maxminusone < max20 and maxplusone > max20):
    xx="There has been a maximum in the shorter moving average in the last 20 days. \
       According to a 'buy low sell high' strategy, its a good moment to sell."
else:
    xx="There has neither bean a minimum nor a maximum in the moving average in the last 20 days. \
       According to a 'buy low sell high' strategy, you are adviced to hold your position."

# An nummerical index is created for the two moving averages.
mavgthree = mavg.reset_index()
mavgfour = mavg2.reset_index()

# An approximation to an intersection point is calculated. If the absolute difference between mavg2 and mavg is smaller than the indicated value, it is assumed that the two functions cross.
aa = abs(mavgthree.loc[-100:, 'Adj Close'] - mavgfour.loc[-100:, 'Adj Close'])<0.1

# The code checks, whether there has been an intersection point in the last 100 days. If there has been one, its intersection point is appended to a list.
mylist = []
for i in range(1, 100):
    if (aa[len(aa) - i] == True):
        mylist.append(aa.index[len(aa) - i])

# If the list is not empty, the most recent intersection point is determined. It is excluded that this index is the the most recent resp. the first index. Otherwise, the following calculation of one day after resp. one before the entry would not work.
# The day after the intersection point is calculated. The according closing price is determined and rounded on two decimal points. In addition, the date is stored in a variable.
# It is counted how many days have passed since the intersection point and the day of the execution of the code by calculating the difference between the two dates.
# If the short moving average is than higher one day after the intersection than the longer moving average, it is assume that the price is actually increasing faster than according to the longer average.
# Therefore, it is recommended two buy the stock. Should the day one day after the intersection point contain a short moving average which is lower than the long one, it is assumed that the price is actually decreasing faster
# than in the longer moving average and that the stock therefore should be sold.
if (mylist != []):
    aaa = max(mylist)

    if (aaa != 0 and aaa != len(aa) - 1):
        aaaplusone = aaa + 1

        maxclose = round(mavgthree.loc[aaa, 'Adj Close'],2)
        maxdate = mavgthree.loc[aaa, 'Date']
        maxdate = maxdate.strftime("%Y-%m-%d")

        date1 = mavgthree.loc[aaa, 'Date']
        date2 = mavgthree.loc[len(aa) - 1, 'Date']
        diffdates = date2 - date1
        days = diffdates.days

        if (mavgthree.loc[aaaplusone, 'Adj Close'] < mavgfour.loc[aaaplusone, 'Adj Close']):
            bb= "It's a good moment to sell. There has been a short point according to moving average intercetion theory in the last 100 days on: " + str(maxdate) + " This has been: %s days from now." % (days) + "The value was: " + str(maxclose)

        if (mavgthree.loc[aaaplusone, 'Adj Close'] > mavgfour.loc[aaaplusone, 'Adj Close']):
                bb = "It's a good moment to buy. There has been a long point according to moving average intercetion theory in the last 100 days on: " + str(maxdate) + " This has been: %s days from now." % (days) + "The value was: " + str(maxclose)
else:
    bb="There hasn't been an intersection according to moving average theory in the last 100 days. Therefore, you're adviced to hold your position."


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
                                    html.H5("Investment Advice"),
                                    html.Br([]),
                                    html.P(xx,
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                    html.P(bb,
                                           style={"color": "#ffffff"},
                                           className="row",
                                           ),

                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),

                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Moving average", className="subtitle padded"),

                                    dcc.Graph(
                                        id="graph-4",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    #test this is the date line
                                                    x=dateindex,
                                                    #this is the closing prices
                                                    y=close_px,
                                                    line={"color": "#151C97"},
                                                    mode="lines",
                                                    name=stockmov,
                                                ),
                                                go.Scatter(
                                                    x=dateindex,
                                                    #second graph with opening price
                                                    y=mavg,
                                                    line={"color": "#b5b5b5"},
                                                    mode="lines",
                                                    name="Mavg",
                                                ),
                                                go.Scatter(
                                                    x=dateindex,
                                                    # third graph with opening price
                                                    y=mavg2,
                                                    line={"color": "#555555"},
                                                    mode="lines",
                                                    name="Mavg2",
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
