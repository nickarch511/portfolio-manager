import financeMethods as fm
import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import yfinance as yf


"""
This class will control a given stock portfolio.
It will contain two instance variables, self.stocks and self.numstocks
which contain the strings of all valid tickers and the number of 
valid tickers in the portfolio.

Any ticker that is invalid that is passed into the constructor will not
be added to the Portfolio object's stock_list or num_stocks instance variables.

"""
class Portfolio:

    # define symbolic constants
    LONG_PORTFOLIO = 0
    LIMITED_PORTFOLIO = 1
    UNLIMITED_PORTFOLIO = 2

    # Constructor
    def __init__(self, stock_list, type=LONG_PORTFOLIO, amount=1):
        
        self.stocks = set()
        self.portfolioType = type
        self.amount = amount

        for stock in stock_list:
            ticker = yf.Ticker(stock)
            
            # Determine whether is it a valid ticker
            try:
                info = ticker.info # If this runs, it is valid
                if not info['regularMarketPrice'] == None:
                    self.stocks.add(stock.upper().strip())
                    self.num_stocks += 1
            except: 
                continue # invalid
        self.num_stocks = len(self.stocks)
    
    def add_stocks(self, stock_list):
        for stock in stock_list:
            ticker = yf.Ticker(stock)
            
            # Determine whether is it a valid ticker
            try:
                info = ticker.info # If this runs, it is valid
                if not info['regularMarketPrice'] == None:
                    self.stocks.add(stock.upper().strip())
                    self.num_stocks += 1
            except: 
                continue # invalid
        
    def clear_stocks(self):
        self.stocks = set()
        self.num_stocks = 0

    def getTangentPortfolio(self):
        a_year = timedelta(days=365)
        today = datetime.strftime(datetime.today() - a_year, "%Y-%m-%d")
        assets = list(self.stocks)
        data = yf.download(" ".join(assets), start=today - a_year, end=today)
        asset_data = {}
        for name in assets:
            x = pd.DataFrame(data.xs(name,axis=1, level=1))
            x["Date"] = x.index
            asset_data[name] = fm.getDailyReturnsDataFrame(x)
        
        M = fm.getM(asset_data, assets, datetime.strftime(datetime.today() - a_year, "%Y-%m-%d"), datetime.strftime(datetime.today(), "%Y-%m-%d"))
        V = fm.getV(asset_data, assets, datetime.strftime(datetime.today() - a_year, "%Y-%m-%d"), datetime.strftime(datetime.today(), "%Y-%m-%d"))    
        
        for i, name in zip(fm.calculateFST(V,M, .0000459), assets):
            print("{}: {}".format(name,i*50000))

        return [0 for i in range(self.num_stocks)]

    def getLongPortfolio(self):
        return [0 for i in range(self.num_stocks)]

    def getLimitedLeveragePortfolio(self):
        return [0 for i in range(self.num_stocks)]

    # Add string method
    def __str__(self):
        return " ".join(self.stocks)


