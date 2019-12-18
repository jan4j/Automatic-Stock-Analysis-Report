# -*- coding: utf-8 -*-
#####First we load the data from the Module Yahoo_scratcher by executing yahoo_data()
from yahoo_scratcher import yahoo_data


######We load all the modules from dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#######Modules for different Pages in Report
from pages import (overview,Movingaverage)
yahoo_data()

###### Function for App
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash-financial-report/Movingaverage":
        return Movingaverage.create_layout(app)
    else:
        return overview.create_layout(app)


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)
