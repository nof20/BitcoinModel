"""Bitcoin data tests.
"""

import unittest
from datetime import datetime
from Signals.BitcoinData import BitcoinData


class BitcoinDataTest(unittest.TestCase):

    def setUp(self):
        self.bd = BitcoinData()

    def test_get(self):
        expected = ('{"Open":{"1483228800000":961.18,"1483315200000":973.36},'
                    '"High":{"1483228800000":973.37,"1483315200000":1000.0},'
                    '"Low":{"1483228800000":949.0,"1483315200000":964.37},'
                    '"Volume":{"1483228800000":3838.21925314,'
                    '"1483315200000":4420.41105561}}')
        self.assertEqual(
            self.bd.get(
                '2017-01-01',
                '2017-01-02').to_json(),
            expected)

        from_dt = datetime(2017, 1, 1)
        to_dt = datetime(2017, 1, 2)
        self.assertEqual(self.bd.get(from_dt, to_dt).to_json(), expected)

if __name__ == "__main__":
    unittest.main()
