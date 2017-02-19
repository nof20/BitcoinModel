"""Import Wikipedia viewership data.
"""

from requests import get
from datetime import datetime
import pandas as pd
import numpy as np
from couchdb.mapping import Document, FloatField, DateField, TextField
from Tools.DBCache import DBCache


class WikipediaData(object):
    BASEURL = (
        'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/'
        'en.wikipedia/all-access/all-agents/')
    PAGE = 'Bitcoin'
    FREQ = 'daily'

    def __init__(self):
        self.db = DBCache()

    def get(self, start_date, end_date, cached=True):
        # TODO: Handle partial caching of range
        if cached:
            df = self.get_db(start_date, end_date)
        else:
            df = self.get_ws(start_date, end_date)
            self.set_db(df)
        return df

    def get_ws(self, start_date, end_date):
        if isinstance(start_date, datetime):
            date_arr = map(
                lambda x: "{:02d}".format(x),
                start_date.timetuple()[
                    :3])
            start_date = "".join(date_arr)
        if isinstance(end_date, datetime):
            date_arr = map(
                lambda x: "{:02d}".format(x),
                end_date.timetuple()[
                    :3])
            end_date = "".join(date_arr)
        url = self.BASEURL + self.PAGE + '/' + self.FREQ + '/' \
            + start_date + '/' + end_date
        response = get(url)
        if response.status_code == 200:
            values = response.json()['items']
            wiki = pd.DataFrame(values)
            wiki['Date'] = wiki.apply(lambda row: datetime(int(row.timestamp[0:4]), int(
                row.timestamp[4:6]), int(row.timestamp[6:8])).date(), axis=1)
            wiki['Date'] = pd.to_datetime(wiki['Date'])
            wiki.drop(['access', 'agent', 'article', 'granularity', 'project',
                       'timestamp'], axis=1, inplace=True)
            wiki.set_index('Date', inplace=True)
            wiki.sort_index(inplace=True)
            return wiki
        else:
            raise ValueError(
                "Incorrect response received from WikiMedia server.")

    def get_db(self, start_date, end_date):
        view = self.db.get_view("DBCache_views/WikipediaData")
        start_date = DBCache.datetime_string(start_date)
        end_date = DBCache.datetime_string(end_date)
        rows = view[start_date:end_date]
        df = WikipediaDoc.get_df_from_rows(rows)
        return df

    def set_db(self, df):
        doclist = WikipediaDoc.get_doclist_from_df(df)
        self.db.save_doc_list(doclist)


class WikipediaDoc(Document):
    """ORM for CouchDB."""

    Type = TextField()
    views = FloatField()
    Date = DateField()

    @staticmethod
    def get_doclist_from_df(df):
        df2 = df.reset_index()
        ll = []
        for row in df2.itertuples():
            doc = WikipediaDoc()
            doc.Type = "WikipediaData"
            if ~np.isnan(row.views):
                doc.views = row.views
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
