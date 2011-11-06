import requests
import json
import sys


def index_create(host, port, indexname, shards, replicas):
    data_request = json.dumps({"settings" : { "number_of_shards" : shards,
        "number_of_replicas" : replicas } }, sort_keys=True, indent=4)

    try:
        request = requests.post('http://' + host + ':' + port + '/' +
                indexname, data=data_request)
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


def index_list(host, port, extended):
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
        data_result = json.loads(request.content)[u'indices']
        print 'SUCCESS: Listing Indexes'
        for index in data_result:
            print 'Name:', index
            if extended:
                print '\t Status:', data_result[index][u'status']
                print '\t Number Of Shards:', data_result[index][u'number_of_shards']
                print '\t Number Of Replicas:', data_result[index][u'number_of_replicas']
        sys.exit(0)


def index_open(host, port, indexname):
    try:
        request = requests.post('http://' + host + ':' + port + '/' +
                indexname + '/_open')
        if request.error is not None:
            print 'ERROR: Opening Index : "' + indexname + '" -', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Opening Index : "' + indexname + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Opening Index : "' + indexname + '"'
        sys.exit(0)


def index_close(host, port, indexname):
    try:
        request = requests.post('http://' + host + ':' + port + '/' +
                indexname + '/_close')
        if request.error is not None:
            print 'ERROR: Closing Index : "' + indexname + '" -', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Closing Index : "' + indexname + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Closing Index : "' + indexname + '"'
        sys.exit(0)
