"""Calculate P/L.

Relies on Python 3 float division.
"""

import math
import numpy as np
import pandas as pd


class PnL(object):
    COMMISSION = 25  # basis points: see e.g. https://gemini.com/fee-schedule/

    def calc_pnl(self, x, y, price_col="Open"):
        """Calculate P/L.  x is dataframe of price, with price_col;
        y is boolean price signal, often from a model prediction."""
        if x.shape[0] != y.shape[0]:
            raise ValueError("Dataframes have different numbers of rows.")
        days = x.shape[0]
        cash = 100.0
        position = 0.0
        price = 0.0
        for i in range(days):
            if isinstance(y, np.ndarray):
                signal = y[i]
            elif isinstance(y, pd.core.series.Series):
                signal = y.iloc[i]
            else:
                raise TypeError(
                    "Type {} not supported, provide Numpy or Pandas data".format(
                        type(y)))
            if (signal) and (cash > 0):
                # Buy
                price = x[price_col].iloc[i]
                commission = cash * 0.0025
                amount = (cash - commission) / price
                position += amount
                cash = 0
                # print("Bought {:.3f} @ {:.3f}, commission {:.3f}, position now {:.3f}"\
                #.format(amount, price, commission, position))
            elif (signal == False) and (position > 0):
                # Sell
                price = x[price_col].iloc[i]
                valuation = position * price
                amount = position
                commission = valuation * 0.0025
                cash += (valuation - commission)
                position = 0
                # print("Sold {:.3f} @ {:.3f}, commission {:.3f}, position now {:.3f}"\
                #.format(amount, price, commission, position))

        value = cash + (position * price)
        year_frac = days / 365.0
        ret = value - 100.0
        fact = ret / 100.0
        year_fact = math.pow(fact, 1 / year_frac) if fact > 0 else - \
            1 * math.pow(abs(fact), 1 / year_frac)
        apr = 100 * (year_fact - 1)

        return {"cash": cash,
                "position": position,
                "value": value,
                "APR": apr}
