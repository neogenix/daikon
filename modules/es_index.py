import requests
import json
import sys


def index_create(host, port, indexname, shards, replicas):

    data = json.dumps([{"index" : { "number_of_shards" : shards,
        "number_of_replicas" : replicas } }], sort_keys=True, indent=4)
    request = requests.post('http://' + host + ':' + port + '/' + indexname,
            data=data)

    if request.raise_for_status() is not None:
        print request.raise_for_status()
        sys.exit[1]

    if not request.status_code == requests.codes.ok:
        print request.content
        print request.status_code
        print request.raise_for_status()
    else:
        print 'Index "' + indexname + '" Created Successfully'

#def index_delete(host, indexname):
