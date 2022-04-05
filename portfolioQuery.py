import financeMethods as fm
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import dataframe_image as dfi
import requests
from bs4 import BeautifulSoup



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
        today = datetime.strftime(datetime.today(), "%Y-%m-%d")
        last_year = datetime.strftime(datetime.today() - a_year, "%Y-%m-%d")
        assets = list(self.stocks)
        data = yf.download(" ".join(assets), start=last_year, end=today)
        asset_data = {}
        print(data)
        for name in assets:
            x = pd.DataFrame(data.xs(name,axis=1, level=1))
            x["Date"] = x.index
            asset_data[name] = fm.getDailyReturnsDataFrame(x)
        
        M = fm.getM(asset_data, assets, datetime.strftime(datetime.today() - a_year, "%Y-%m-%d"), datetime.strftime(datetime.today(), "%Y-%m-%d"))
        V = fm.getV(asset_data, assets, datetime.strftime(datetime.today() - a_year, "%Y-%m-%d"), datetime.strftime(datetime.today(), "%Y-%m-%d"))    
        
        fst = fm.calculateFST(V,M, self.get_si_rate())
        string = ""
        for i, name in zip(fst, assets):
            allocation_string = '-$' + str(-1*round(i*self.amount, 2)) if i < 0 else '$' + str(round(i*self.amount, 2))
            string += "{}: {}".format(name,allocation_string) + '\n'

        return string

    def getLongPortfolio(self):
        a_year = timedelta(days=365)
        today = datetime.strftime(datetime.today(), "%Y-%m-%d")
        last_year = datetime.strftime(datetime.today() - a_year, "%Y-%m-%d")
        assets = list(self.stocks)
        data = yf.download(" ".join(assets), start=last_year, end=today)
        asset_data = {}
        print(data)
        for name in assets:
            x = pd.DataFrame(data.xs(name,axis=1, level=1))
            x["Date"] = x.index
            asset_data[name] = fm.getDailyReturnsDataFrame(x)
        
        M = fm.getM(asset_data, assets, datetime.strftime(datetime.today() - a_year, "%Y-%m-%d"), datetime.strftime(datetime.today(), "%Y-%m-%d"))
        V = fm.getV(asset_data, assets, datetime.strftime(datetime.today() - a_year, "%Y-%m-%d"), datetime.strftime(datetime.today(), "%Y-%m-%d"))    
        
        flt = fm.getFlt(V,M, self.get_si_rate())['Flt'][0]
        string = ""
        for i, name in zip(flt, assets):
            allocation_string = '-$' + str(-1*round(i*self.amount, 2)) if i < 0 else '$' + str(round(i*self.amount, 2))
            string += "{}: {}".format(name,allocation_string) + '\n'

        return string

    # This function with take a decimal argument p, the maximal percentage of portfolio held in short
    def getLimitedLeveragePortfolio(self):
        a_year = timedelta(days=365)
        today = datetime.strftime(datetime.today(), "%Y-%m-%d")
        last_year = datetime.strftime(datetime.today() - a_year, "%Y-%m-%d")
        assets = list(self.stocks)
        data = yf.download(" ".join(assets), start=last_year, end=today)
        asset_data = {}
        print(data)
        for name in assets:
            x = pd.DataFrame(data.xs(name,axis=1, level=1))
            x["Date"] = x.index
            asset_data[name] = fm.getDailyReturnsDataFrame(x)
        
        M = fm.getM(asset_data, assets, datetime.strftime(datetime.today() - a_year, "%Y-%m-%d"), datetime.strftime(datetime.today(), "%Y-%m-%d"))
        V = fm.getV(asset_data, assets, datetime.strftime(datetime.today() - a_year, "%Y-%m-%d"), datetime.strftime(datetime.today(), "%Y-%m-%d"))    
        
        fst = fm.calculateFST(V,M, self.get_si_rate())
        string = ""
        for i, name in zip(fst, assets):
            allocation_string = '-$' + str(-1*round(i*self.amount, 2)) if i < 0 else '$' + str(round(i*self.amount, 2))
            string += "{}: {}".format(name,allocation_string) + '\n'

        return string

    def get_si_rate(self):
        date = datetime.strftime(datetime.today(), "%Y%m")
        page = requests.get('https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_bill_rates&field_tdr_date_value_month='+date)
        soup = BeautifulSoup(page.text, 'html.parser')
        res = [s.strip(' ') for s in soup.find_all('table')[0].get_text().split('\n')]
        res = [s for s in res if not s == 'N/A' and not s == ''][-1]
        res = float(res)/100
        
        a_year = timedelta(days=365)
        today = datetime.strftime(datetime.today(), "%Y-%m-%d")
        last_year = datetime.strftime(datetime.today() - a_year, "%Y-%m-%d")
        assets = list(self.stocks)
        data = yf.download(" ".join(assets), start=last_year, end=today)
        asset_data = {}
        print(data)
        for name in assets:
            x = pd.DataFrame(data.xs(name,axis=1, level=1))
            x["Date"] = x.index
            asset_data[name] = fm.getDailyReturnsDataFrame(x)

        res = (1+res)**(1/fm.getTradingDays(asset_data, assets, last_year,today)) - 1
        return res

    # Add string method
    def __str__(self):
        return " ".join(self.stocks)


