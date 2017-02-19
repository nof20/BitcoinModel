#!/bin/sh 

#TODO: Use hostname/port from .ini file

curl -X PUT 'http://localhost:5984/bitcoin-model'

curl -X PUT -d @DBCache_views.json 'http://localhost:5984/bitcoin-model/_design/DBCache_views'
