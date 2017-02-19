"""Class to store and retrieve data from DB.
"""

import couchdb
import configparser
import json
from uuid import uuid4
from datetime import datetime


class DBCache(object):
    DB_NAME = "bitcoin-model"

    @staticmethod
    def datetime_string(dt):
        if isinstance(dt, datetime):
            return dt.date().isoformat()
        elif isinstance(dt, str):
            return dt
        else:
            raise TypeError(
                "Incompatible object provided to DBCache.datetime_string().")

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        url = "http://{}:{}".format(self.config['DB']['hostname'],
                                    self.config['DB']['port'])
        self.db = couchdb.Server(url)[self.DB_NAME]

    def save_doc(self, doc):
        doc_id = uuid4()
        self.db[doc_id] = doc

    def save_doc_list(self, list):
        for doc in list:
            try:
                doc.store(self.db)
            except Exception:
                print("Caught exception storing doc {}".format(doc))
                raise Exception

    def get_view(self, viewname):
        return self.db.view(viewname)
