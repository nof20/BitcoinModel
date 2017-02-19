"""Manage DB cache."""

from datetime import datetime, timedelta
from Signals.BitcoinData import BitcoinData
from Signals.FXData import FXData
from Signals.WikipediaData import WikipediaData


class CacheManager(object):
    START_DATE = datetime(2016, 1, 1)
    END_DATE = datetime(2017, 1, 1)
    STEP = 30  # days

    def __init__(self):
        self.bd = BitcoinData()
        self.fd = FXData()
        self.wd = WikipediaData()

    def fill_cache(self):
        start_range = self.START_DATE
        end_range = self.START_DATE + timedelta(days=self.STEP)
        while start_range < self.END_DATE:
            print(
                "Filling cache from {} to {}".format(
                    start_range.date().isoformat(),
                    end_range.date().isoformat()))
            df = self.bd.get_ws(start_range, end_range)
            self.bd.set_db(df)
            df = self.fd.get_ws(start_range, end_range)
            self.fd.set_db(df)
            df = self.wd.get_ws(start_range, end_range)
            self.wd.set_db(df)
            start_range = end_range
            end_range = end_range + timedelta(days=self.STEP)
            if end_range > self.END_DATE:
                end_range = END_DATE


if __name__ == "__main__":
    cm = CacheManager()
    cm.fill_cache()
