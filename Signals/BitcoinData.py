""" Module to download Bitcoin prices from Quandl.

See https://www.quandl.com/data/GDAX/USD-BTC-USD-Exchange-Rate
"""

import configparser
import datetime
import quandl
import pandas as pd
import numpy as np
from couchdb.mapping import Document, FloatField, DateField, TextField
from Tools.DBCache import DBCache


class BitcoinData(object):
    #TODO: Define an abc (interface) for these common methods.
    TICKER = "GDAX/USD"

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.db = DBCache()

    def get(self, start_date, end_date, cached=True):
        if cached:
            df = self.get_db(start_date, end_date)
        else:
            df = self.get_ws(start_date, end_date)
            self.set_db(df)
        return df

    def get_ws(self, start_date, end_date):
        """Return DataFrame of prices between selected dates."""
        start_date = DBCache.datetime_string(start_date)
        end_date = DBCache.datetime_string(end_date)
        series = quandl.get(
            self.TICKER,
            api_key=self.config['Quandl']['authtoken'],
            start_date=start_date,
            end_date=end_date)
        return series

    def get_db(self, start_date, end_date):
        view = self.db.get_view("DBCache_views/BitcoinData")
        start_date = DBCache.datetime_string(start_date)
        end_date = DBCache.datetime_string(end_date)
        rows = view[start_date:end_date]
        df = BitcoinDoc.get_df_from_rows(rows)
        return df

    def set_db(self, df):
        doclist = BitcoinDoc.get_doclist_from_df(df)
        # TODO: Prevent saving of duplicates
        self.db.save_doc_list(doclist)


class BitcoinDoc(Document):
    """ORM for CouchDB."""

    Type = TextField()
    Open = FloatField()
    High = FloatField()
    Low = FloatField()
    Volume = FloatField()
    Date = DateField()

    @staticmethod
    def get_doclist_from_df(df):
        df2 = df.reset_index()
        ll = []
        for row in df2.itertuples():
            doc = BitcoinDoc()
            doc.Type = "BitcoinData"
            if ~np.isnan(row.Open):
                doc.Open = row.Open
            if ~np.isnan(row.High):
                doc.High = row.High
            if ~np.isnan(row.Low):
                doc.Low = row.Low
            if ~np.isnan(row.Volume):
                doc.Volume = row.Volume
            doc.Date = row.Date.to_pydatetime()
            ll.append(doc)
        return ll

    @staticmethod
    def get_df_from_rows(rows):
        ll = [row.value for row in rows]
        df = pd.DataFrame(ll)
        df.drop(["Type", "_id", "_rev"], axis=1, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index("Date", inplace=True)
        return df
