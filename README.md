# BitcoinModel
A simple Bitcoin price model, built in Python.

* Includes signals from:
	- [Quandl](https://www.quandl.com/tools/python) (Bitcoin prices, FX rates, financial indices)
	- Wikipedia page views
* Uses standard SciPy stack (Numpy, Pandas, etc.)
* Caches data locally in [Couchdb](http://pythonhosted.org/CouchDB).

To do:

* Implement Logistic Regression model
* Add signals:
	- News sentiment
	- [Reddit](https://github.com/reddit/reddit/wiki/API) sentiment
* Calculate measures:
	- P/L
	- AUC chart
* Add [logging](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial)

Requires Python 3.  Store auth tokens usernames/passwords etc. in `config.ini`.

`$ python -m unittest discover` to run unit tests.
