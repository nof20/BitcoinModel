""" Module to download FX and Volatility data from Quandl.

e.g. https://www.quandl.com/data/BOE/XUDLBK73-Spot-exchange-rate-Chinese-Yuan-into-Dollar
"""

import configparser
import datetime
import quandl

class FXData(object):
    TICKERS = ["BOE/XUDLBK73", "BOE/XUDLERD", "CBOE/VIX"] # USDCNY, USDEUR, VIX

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
       
    def get(self, start_date, end_date):
        """Return DataFrame of prices between selected dates."""
        if type(start_date) is datetime.datetime:
            start_date = start_date.date().isoformat()
            
        if type(end_date) is datetime.datetime:
            end_date = end_date.date().isoformat()
        
        series = quandl.get(self.TICKERS, api_key=self.config['Quandl']['authtoken'],
                            start_date=start_date, end_date=end_date)
        
        series.drop(["CBOE/VIX - VIX Open", "CBOE/VIX - VIX High", \
                     "CBOE/VIX - VIX Low"], axis=1, inplace=True)
        series.rename(columns={"BOE/XUDLBK73 - Value":"USDCNY",\
                               "BOE/XUDLERD - Value":"USDEUR",\
                               "CBOE/VIX - VIX Close":"VIX"}, inplace=True)
        return series
