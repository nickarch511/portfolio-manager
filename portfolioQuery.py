import financeMethods as fm
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import random



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

        # Graph the frontier
        self.graphFrontier(fst)

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
        
        # Graph the frontier
        self.graphFrontier(flt)

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

    def graphFrontier(self, portfolio):
        # Get asset data
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
        
        # Get Return mean vector and covariance matrix
        M = fm.getM(asset_data, assets, datetime.strftime(datetime.today() - a_year, "%Y-%m-%d"), datetime.strftime(datetime.today(), "%Y-%m-%d"))
        V = fm.getV(asset_data, assets, datetime.strftime(datetime.today() - a_year, "%Y-%m-%d"), datetime.strftime(datetime.today(), "%Y-%m-%d"))    

        rm = fm.getReturnMeanForTwoRatePortfolio(fm.calculateFmv(V,M),M)
        rv = fm.getReturnVolatilityForTwoRatePortfolio(fm.calculateFmv(V,M),V)

        rmPortfolio = fm.getReturnMeanForTwoRatePortfolio(portfolio,M)
        rvPortfolio = fm.getReturnVolatilityForTwoRatePortfolio(portfolio,V)

        # Plot frontier
        plt.figure(figsize=(14,14))
        mu = np.arange(-2*abs(rmPortfolio),2*abs(rmPortfolio),.000001)
        sigma = [fm.calculateMarkowitzFrontier(V,M,i) for i in mu]

        plt.plot(sigma,mu)
        plt.scatter(rv,rm,s=100)    
        plt.text(rv, rm, "MV", fontsize=12)        
        print("rv is {} and rm is {}".format(rvPortfolio,rmPortfolio))
        plt.scatter(rvPortfolio,rmPortfolio,s=100)    
        plt.text(rvPortfolio, rmPortfolio, "Your Portfolio", fontsize=12)   

        plt.show()


    '''
    This is a helper function for pickLongPortfolio
    The asset string here will be a space-delimited string
    of all ticker symbols.

    The Rf will be the coupon rate for a 52-week treasury bill

    returns flt object and names
    '''
    def getLongPortfolioGivenAssetStringAndRf(self, asset_names, muSi, money_to_invest):
        a_year = timedelta(days=365)
        datetime.strftime(datetime.today() - a_year, "%Y-%m-%d")
        data = data = yf.download(" ".join(asset_names), start=datetime.strftime(datetime.today() - a_year, "%Y-%m-%d"), end=datetime.strftime(datetime.today(), "%Y-%m-%d"))
        asset_data = {}
        for name in asset_names:
            x = pd.DataFrame(data.xs(name,axis=1, level=1))
            x["Date"] = x.index
            asset_data[name] = fm.getDailyReturnsDataFrame(x)
        muSi = (1+muSi)**(1/len(asset_data[asset_names[0]]['Date'])) - 1
        M = fm.getM(asset_data, asset_names, "1999-01-01", "2023-01-01")
        V = fm.getV(asset_data, asset_names, "2021-01-01", "2022-01-01")
        flt = fm.getFlt(V,M,muSi)
        print("The expected risk of this portfolio is {}, and the expected return is {}".format(flt['sigma'], flt['mu']))
        for i,name in zip(flt['Flt'][0]*money_to_invest, asset_names):
            if i > 500: print("{}: {}".format(name,i))
        return flt, asset_names


    '''
    While other features of this class require a portfolio, this function will 
    select the best portfolio of size numAssets that it finds after 100 random
    portfolios.
    It maximizes the ratio of reward to return
    '''
    def pickLongPortfolio(self, numAssets):
        assets = "ZTS ZION ZBRA ZBH YUM XYL XRAY XOM XLNX XEL WYNN WY WU WST WRK WRB WMT WMB WM WHR WFC WELL WEC WDC WBA WAT WAB VZ VTRS VTR VRTX VRSN VRSK VNO VMC VLO VIAC VFC V USB URI UPS UNP UNH ULTA UHS UDR UAL UAA UA TYL TXT TXN TWTR TTWO TT TSN TSLA TSCO TRV TROW TRMB TPR TMUS TMO TJX TGT TFX TFC TER TEL TECH TDY TDG TAP T SYY SYK SYF SWKS SWK STZ STX STT STE SRE SPGI SPG SO SNPS SNA SLB SJM SIVB SHW SEE SCHW SBUX SBAC RTX RSG ROST ROP ROL ROK RMD RL RJF RHI RF REGN REG RE RCL QRVO QCOM PYPL PXD PWR PVH PTC PSX PSA PRU PPL PPG POOL PNW PNR PNC PM PLD PKI PKG PHM PH PGR PG PFG PFE PEP PENN PEG PEAK PCAR PBCT PAYX PAYC OXY OTIS ORLY ORCL OMC OKE OGN ODFL O NXPI NWSA NWS NWL NVR NVDA NUE NTRS NTAP NSC NRG NOW NOC NLSN NLOK NKE NI NFLX NEM NEE NDAQ NCLH MU MTD MTCH MTB MSI MSFT MSCI MS MRO MRNA MRK MPC MOS MO MNST MMM MMC MLM MKTX MKC MHK MGM MET MDT MDLZ MCO MCK MCHP MCD MAS MAR MAA MA LYV LYB LW LVS LUV LUMN LRCX LOW LNT LNC LMT LLY LKQ LIN LHX LH LEN LEG LDOS L KR KO KMX KMI KMB KLAC KIM KHC KEYS KEY K JPM JNPR JNJ JKHY JCI JBHT J IVZ ITW IT ISRG IRM IR IQV IPGP IPG IP INTU INTC INFO INCY ILMN IFF IEX IDXX ICE IBM HWM HUM HSY HST HSIC HRL HPQ HPE HON HOLX HLT HII HIG HES HD HCA HBI HBAN HAS HAL GWW GS GRMN GPS GPN GPC GOOGL GOOG GNRC GM GLW GL GIS GILD GE GD FTV FTNT FRT FRC FOXA FOX FMC FLT FITB FISV FIS FFIV FE FDX FCX FBHS FB FAST FANG F EXR EXPE EXPD EXC EW EVRG ETSY ETR ETN ESS ES EQR EQIX EOG ENPH EMR EMN EL EIX EFX ED ECL EBAY EA DXCM DXC DVN DVA DUK DTE DRI DRE DPZ DOW DOV DLTR DLR DISH DISCK DISCA DIS DHR DHI DGX DG DFS DE DD D CZR CVX CVS CTXS CTVA CTSH CTRA CTLT CTAS CSX CSCO CRM CRL CPRT CPB COST COP COO COF CNP CNC CMS CMI CMG CME CMCSA CMA CLX CL CINF CI CHTR CHRW CHD CFG CF CERN CE CDW CDNS CDAY CCL CCI CBRE CBOE CB CAT CARR CAH CAG C BXP BWA BSX BRO BR BMY BLL BLK BKR BKNG BK BIO BIIB  BEN BDX BBY BBWI BAX BAC BA AZO AXP AWK AVY AVGO AVB ATVI ATO ARE APTV APH APD APA AOS AON ANTM ANSS ANET AMZN AMT AMP AMGN AME AMD AMCR AMAT ALLE ALL ALK ALGN ALB AKAM AJG AIZ AIG AFL AES AEP AEE ADSK ADP ADM ADI ADBE ACN ABT ABMD ABC ABBV AAPL AAP AAL A"
        assets = assets.split(" ")
        x = [i for i in assets if i != '']
        bestflt = None
        bestNames = None
        bestRewardToReturnRatio = 0

        self.num_stocks = numAssets
        for _ in range(3):
            self.stocks = random.sample(x,numAssets)
            flt,names = self.getLongPortfolioGivenAssetStringAndRf(self.stocks, self.get_si_rate(), 1)
            if flt['mu']/flt['sigma'] > bestRewardToReturnRatio:
                bestRewardToReturnRatio = flt['mu']/flt['sigma']
                bestflt = flt
                bestNames = names
        print(bestflt)
        print(bestNames)
        self.stocks = bestNames

        # Graph the frontier
        self.graphFrontier(bestflt['Flt'][0])
        bestflt = bestflt['Flt'][0]
        string = ""
        for i, name in zip(bestflt, self.stocks):
            allocation_string = '-$' + str(-1*round(i*self.amount, 2)) if i < 0 else '$' + str(round(i*self.amount, 2))
            string += "{}: {}".format(name,allocation_string) + '\n'

        return string

    # Add string method
    def __str__(self):
        return " ".join(self.stocks)


