# BitcoinModel
A simple Bitcoin price model, built in Python.

* Includes signals from:
	- [Quandl](https://www.quandl.com/tools/python) (Bitcoin prices, FX rates, financial indices)
	- Wikipedia page views
* Uses standard SciPy stack (Numpy, Pandas, etc.)
* Caches data locally in [Couchdb](http://pythonhosted.org/CouchDB)
* Implements a simple logistic regression model
* Calculates annualized profit which would be made.

To do:

* Write unit tests for DB, PnL and datetime conversion
* Other classification models, e.g. Naive Bayes.
* Add signals:
	- News sentiment from the [NY Times](http://developer.nytimes.com/article_search_v2.json#/README)
	- [Reddit](https://github.com/reddit/reddit/wiki/API) sentiment
* Include AUC chart and other model analyses
* Add [logging](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial)

Requires Python 3.  Store auth tokens usernames/passwords etc. in `config.ini`.

`$ pip install -r requirements.txt` to install required libraries.

`$ Tools/init_db.sh` to initialize the CouchDB.

`$ python -m unittest discover` to run unit tests.
