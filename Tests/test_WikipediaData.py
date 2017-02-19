"""Bitcoin data tests.
"""

import unittest
from datetime import datetime
from Signals.WikipediaData import WikipediaData


class WikipediaDataTest(unittest.TestCase):

    def setUp(self):
        self.wd = WikipediaData()

    def test_get(self):
        expected = ('{"views":{"1483228800000":9846,"1483315200000":23985}}')

        self.assertEqual(
            self.wd.get(
                '20170101',
                '20170102').to_json(),
            expected)

        from_dt = datetime(2017, 1, 1)
        to_dt = datetime(2017, 1, 2)
        self.assertEqual(self.wd.get(from_dt, to_dt).to_json(), expected)

if __name__ == "__main__":
    unittest.main()
