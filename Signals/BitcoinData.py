""" Module to download Bitcoin prices from Quandl.

See https://www.quandl.com/data/GDAX/USD-BTC-USD-Exchange-Rate
"""

import configparser
import datetime
import quandl

class BitcoinData(object):
    TICKER = "GDAX/USD"

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
       
    def get(self, start_date, end_date):
        """Return DataFrame of prices between selected dates."""
        if type(start_date) is datetime.datetime:
            start_date = start_date.date().isoformat()
            
        if type(end_date) is datetime.datetime:
            end_date = end_date.date().isoformat()
            
        series = quandl.get(self.TICKER, api_key=self.config['Quandl']['authtoken'],
                            start_date=start_date, end_date=end_date)
        return series
        
        