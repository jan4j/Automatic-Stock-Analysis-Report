# Financial Stock Analysis Report

## Getting Started

### Running the app locally

First create a virtual environment and clone the git repo.
Then install the requirements with pip

```

git clone https://github.com/jan4j/Automatic-Stock-Analysis-Report.git
cd Automatic-Stock-Analysis-Report
pip3 install -r requirements.txt

```

Run the app

```

python3 app.py

```

If this does not work you can otherwise download the repository and install the modules manually. Having done that you can use Pycharm or Spyder to execute the app.py

## About the app

This is an interactive, multi-page report which displays a number of tables and interactive plots in a report format. The app automatically loads the data from yahoo finance.

Please find the exact description of the report in the file **description**.

When you execute the app you will first be asked which stocks you want to have analyzed and from which one you want an investment advice based on chart analysis.
Please always input exactly 4 stock tickers and only 1 ticker for the moving average analysis.
It may take some time after execution until you get the local host adress with the web report since the data will be loaded from yahoo.


![Image description](screenshots/Screenshot1.png)

## Built With

- [Dash](https://dash.plot.ly/) - Main server and interactive components
- [Plotly Python](https://plot.ly/python/) - Used to create the interactive plots

The following is a screenshot of the app in this repo:

![animated](screenshots/financial-report-demo.gif)

