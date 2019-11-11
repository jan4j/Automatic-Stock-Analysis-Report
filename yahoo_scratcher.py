#!/usr/bin/python
#you need the following modules
import pandas_datareader as web
import pathlib
import datetime
import pandas as pd

from yahoofinancials import YahooFinancials



def yahoo_data():
    #ticker needs to be in ["nvda","yahoo"] format
    # #date needs to be in (YYYY,M,D) format
    start = datetime.datetime(2000, 1, 1)

    #We define the end date as the date from today
    end = datetime.datetime.now().date()

    #DataReader method name is case sensitive input:  str(input("Input the tickers!!!")) ["GOOG", "AAPL"]
    tickers = ["GOOG", "AAPL"]

    #Takes only the adjusted closing prices from yahoo
    prices = web.DataReader(tickers,"yahoo", start, end)['Adj Close']

    #build returns. Takes all information from yahoo
    returns = web.DataReader(tickers,"yahoo", start, end)
    daily_returns = returns['Adj Close'].pct_change()
    monthly_returns = returns['Adj Close'].resample('M').ffill().pct_change()

    #create a summary list for the stocks
    summary = monthly_returns.describe()
    summary = summary.round(2)
    mean_daily_returns = daily_returns.mean()


    #We take from yahoo_financials all the summary data about the ticker like beta P/E ratio etc
    #Output is in json datastring
    YF = YahooFinancials(tickers)
    rate = YF.get_key_statistics_data()
    #We transform the json string to a pandas dataframe
    rate = pd.DataFrame(rate)

    #We only take certain ratios with names like beta bookValue etc from column 0 (axis=0)
    facts =rate.filter({'beta', 'bookValue','priceToBook','forwardPE','profitMargins','enterpriseValue',
                       'enterpriseToRevenue','enterpriseToEbitda','sharesShort'}, axis=0)

    print(facts)

    inc=pd.DataFrame(YF.get_financial_stmts('annual', 'balance',reformat=True))


    print(inc)
    #inc=pd.DataFrame(YF.get_financial_stmts('annual', 'income'))




    ################################%%%%%%create the csv files %%%%%%%%%%%%%%%%
    # get relative data folder
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("./data").resolve()


    #save the collected data to data folder as summary file
    #here we have the prices
    prices.to_csv(DATA_PATH.joinpath("prices.csv"))
    #here we have the monthly returns
    monthly_returns.to_csv(DATA_PATH.joinpath("monthly_returns.csv"))
    #save the summary table
    summary.to_csv(DATA_PATH.joinpath("summary.csv"))

    #save the facts table
    facts.to_csv(DATA_PATH.joinpath("facts.csv"))

yahoo_data()