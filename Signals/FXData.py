""" Module to download FX and Volatility data from Quandl.

e.g. https://www.quandl.com/data/BOE/XUDLBK73-Spot-exchange-rate-Chinese-Yuan-into-Dollar
"""

import configparser
import datetime
import quandl
import pandas as pd
from couchdb.mapping import Document, FloatField, DateField, TextField
from Tools.DBCache import DBCache

class FXData(object):
    TICKERS = ["BOE/XUDLBK73", "BOE/XUDLERD", "CBOE/VIX"] # USDCNY, USDEUR, VIX

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.db = DBCache()

       
    def get(self, start_date, end_date, cached=True):
        #TODO: Handle partial caching of range
        if cached:
            df = self.get_db(start_date, end_date)
        else:
            df = self.get_ws(start_date, end_date)
            doclist = FXDoc.get_doclist_from_df(df)
            self.db.save_doc_list(doclist)
        return df
       
    def get_ws(self, start_date, end_date):
        """Return DataFrame of prices between selected dates."""
        start_date = DBCache.datetime_string(start_date)
        end_date = DBCache.datetime_string(end_date)
        series = quandl.get(self.TICKERS, api_key=self.config['Quandl']['authtoken'],
                            start_date=start_date, end_date=end_date)
        
        series.drop(["CBOE/VIX - VIX Open", "CBOE/VIX - VIX High", \
                     "CBOE/VIX - VIX Low"], axis=1, inplace=True)
        series.rename(columns={"BOE/XUDLBK73 - Value":"USDCNY",\
                               "BOE/XUDLERD - Value":"USDEUR",\
                               "CBOE/VIX - VIX Close":"VIX"}, inplace=True)
        return series

    def get_db(self, start_date, end_date):
        view = self.db.get_view("DBCache_views/FXData")
        start_date = DBCache.datetime_string(start_date)
        end_date = DBCache.datetime_string(end_date)
        rows = view[start_date:end_date]
        df = FXDoc.get_df_from_rows(rows)
        return df
        
class FXDoc(Document):
    """ORM for CouchDB."""

    Type = TextField()
    USDCNY = FloatField()
    USDEUR = FloatField()
    VIX = FloatField()
    Date = DateField()
    
    @staticmethod
    def get_doclist_from_df(df):
        df2 = df.reset_index()
        ll = []
        for row in df2.itertuples():
            doc = FXDoc()
            doc.Type = "FXData"
            doc.USDCNY = row.USDCNY
            doc.USDEUR = row.USDEUR
            doc.VIX = row.VIX
            doc.Date = row.Date.to_pydatetime()
            ll.append(doc)
        return ll

    @staticmethod
    def get_df_from_rows(rows):
        ll = [row.value for row in rows]
        df = pd.DataFrame(ll)
        df.drop(["Type", "_id", "_rev"], axis=1, inplace=True)
        df.set_index("Date", inplace=True)
        return df
        