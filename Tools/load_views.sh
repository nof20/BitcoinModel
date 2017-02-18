#!/bin/sh 

curl -X PUT -d @DBCache_views.json 'http://localhost:5984/bitcoin-model/_design/DBCache_views'
