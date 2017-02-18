"""Import Wikipedia viewership data.
"""

from requests import get
from datetime import datetime
import pandas as pd

class WikipediaData(object):
    BASEURL = ('https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/'
               'en.wikipedia/all-access/all-agents/')
    PAGE = 'Bitcoin'
    FREQ = 'daily'
    
    def get(self, start_date, end_date):
        """Return DataFrame of viewer data between selected dates."""
        
        if type(start_date) is datetime:
            date_arr = map(lambda x: "{:02d}".format(x), start_date.timetuple()[:3])
            start_date = "".join(date_arr)
            
        if type(end_date) is datetime:
            date_arr = map(lambda x: "{:02d}".format(x), end_date.timetuple()[:3])
            end_date = "".join(date_arr)
                
        url = self.BASEURL + self.PAGE + '/' + self.FREQ + '/' \
              + start_date + '/' + end_date

        response = get(url)
        if response.status_code == 200:
            values = response.json()['items']
            wiki = pd.DataFrame(values)
            wiki['date'] = wiki.apply(lambda row: datetime(int(row.timestamp[0:4]), \
                                      int(row.timestamp[4:6]), \
                                      int(row.timestamp[6:8])).date(), axis=1)
            wiki['date'] = pd.to_datetime(wiki['date'])
            wiki.drop(['access', 'agent', 'article', 'granularity', 'project', \
                       'timestamp'], axis=1, inplace=True)
            wiki.set_index('date', inplace=True)
            wiki.sort_index(inplace=True)
            return wiki
