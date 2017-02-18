"""Bitcoin data tests.
"""

import unittest
from datetime import datetime
from Signals.FXData import FXData

class FXDataTest(unittest.TestCase):

    def setUp(self):
        self.fd = FXData()
        
    def test_get(self):
        expected = ('{"USDCNY":{"1483401600000":6.9575,"1483488000000":6.9322},'
                    '"USDEUR":{"1483401600000":0.9629,"1483488000000":0.9546},'
                    '"VIX":{"1483401600000":12.85,"1483488000000":11.85}}')
                    
        self.assertEqual(self.fd.get('2017-01-03', '2017-01-04').to_json(), expected)
        
        from_dt = datetime(2017, 1, 3)
        to_dt = datetime(2017, 1, 4)
        self.assertEqual(self.fd.get(from_dt, to_dt).to_json(), expected)
        
if __name__ == "__main__":
    unittest.main()