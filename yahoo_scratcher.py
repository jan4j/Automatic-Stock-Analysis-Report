#!/usr/bin/python
#you need the following modules
import pandas_datareader as web
import pathlib
import datetime
import pandas as pd

#This module do you need to get the key fact and ratios about the tickers
from yahoofinancials import YahooFinancials

def yahoo_data():
    #ticker needs to be in ["nvda","yahoo"] format
    # #date needs to be in (YYYY,M,D) format
    start = datetime.datetime(2005, 1, 1)

    # We define the end date as the date from today.
    end = datetime.datetime.now().date()

    # The input for the code follows. With the while and try function the code will ask the user to enter the tickers again in case if there was an error.
    # The variable var is first set on 1 an changed to 0 as soon as entering the input was successful.
    var=1
    while (var==1):
        try:
            # The input is converted to upperletters in case it isn't to avoid identification problems with yahoo. The string is splitted in to single elements and stored in a list.
            inputone = input("Enter the tickers of four stocks, you'd like to analyze, like 'GOOG AAPL NFLX TSLA': ")
            inputonesplitted = inputone.upper()
            tickers = inputonesplitted.split()
            var=0

            # If the user enters less than for tickers, he is asked to enter four of them, until he does so.
            while (len(tickers) < 4):
                inputone = input("You entered less than four tickers. Please enter four of them: ")
                inputonesplitted = inputone.upper()
                tickers = inputonesplitted.split()
            var=0

            # If the user enters more than for tickers, he is asked to enter four of them, until he does so.
            while (len(tickers) > 4):
                inputone = input("You entered more than four tickers. Please enter four of them: ")
                inputonesplitted = inputone.upper()
                tickers = inputonesplitted.split()
            var=0

        except:
            print("Something went wrong. Try it again!")
            var=1
    #Takes only the adjusted closing prices from yahoo
    prices = web.DataReader(tickers,"yahoo", start, end)['Adj Close']
    #standardize to compare the time series

    #build returns. Takes all information from yahoo
    returns = web.DataReader(tickers,"yahoo", start, end)
    #daily_returns = returns['Adj Close'].pct_change()
    monthly_returns = returns['Adj Close'].resample('M').ffill().pct_change()

    #create a summary list for the stocks
    summary = monthly_returns.describe()
    summary = summary.round(3)
    #mean_daily_returns = daily_returns.mean()


    #We take from yahoo_financials all the summary data about the ticker like beta P/E ratio etc
    #Output is in json datastring
    YF = YahooFinancials(tickers)
    rate = YF.get_key_statistics_data()
    #We transform the json string to a pandas dataframe
    rate = pd.DataFrame(rate)

    #We only take certain ratios with names like beta bookValue etc from column 0 (axis=0)
    facts =rate.filter({'beta', 'bookValue','priceToBook','forwardPE','profitMargins',
                       'enterpriseToRevenue','enterpriseToEbitda','earningsQuarterlyGrowth'}, axis=0)
    #We make a separate variable with the enterprise values (ev)
    ev = rate.filter({'enterpriseValue'}, axis=0)

    #inc=pd.DataFrame(YF.get_financial_stmts('annual', 'balance',reformat=True))


    ####################                   create the csv files                %%%%%%%%%%%%%%%%
    # get relative data folder
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("./data").resolve()

    #Save the collected data to data folder
    prices.to_csv(DATA_PATH.joinpath("prices.csv"))
    monthly_returns.to_csv(DATA_PATH.joinpath("monthly_returns.csv"))
    summary.to_csv(DATA_PATH.joinpath("summary.csv"))
    facts.to_csv(DATA_PATH.joinpath("facts.csv"))
    ev.to_csv(DATA_PATH.joinpath("ev.csv"))


