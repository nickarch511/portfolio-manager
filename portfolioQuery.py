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

    # Constructor
    def __init__(self, stock_list):
        
        self.stocks = set()

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
        return [0 for i in range(self.num_stocks)]

    def getLongPortfolio(self):
        return [0 for i in range(self.num_stocks)]

    def getLimitedLeveragePortfolio(self):
        return [0 for i in range(self.num_stocks)]

    # Add string method
    def __str__(self):
        return " ".join(self.stocks)