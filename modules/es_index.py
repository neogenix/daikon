import requests
import json
import sys


def index_create(host, port, indexname, shards, replicas):
    data_out = json.dumps({"settings" : { "number_of_shards" : shards,
        "number_of_replicas" : replicas } }, sort_keys=True, indent=4)

    try:
        request = requests.post('http://' + host + ':' + port + '/' +
                indexname, data=data_out)
        if request.error is not None:
            print 'ERROR: Creating Index : "' + indexname + '" -', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Creating Index : "' + indexname + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Creating Index : "' + indexname + '"'
        sys.exit(0)


def index_delete(host, port, indexname):
    try:
        request = requests.delete('http://' + host + ':' + port + '/' + indexname)
        if request.error is not None:
            print 'ERROR: Deleteing Index : "' + indexname + '" -', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Deleting Index : "' + indexname + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Deleting Index : "' + indexname + '"'
        sys.exit(0)


def index_list(host, port):
    try:
        request = requests.get('http://' + host + ':' + port +
                '/_cluster/health?level=indices')
        if request.error is not None:
            print 'ERROR: Listing Indexes :', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR:  Listing Indexes -', e
        sys.exit(1)
    else:
        for index in json.loads(request.content)[u'indices']:
            print "Name: " + index
        sys.exit(0)
