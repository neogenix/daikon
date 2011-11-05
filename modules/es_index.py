import requests
import json
import sys


def index_create(host, port, indexname, shards, replicas):

    data_out = json.dumps([{"index" : { "number_of_shards" : shards,
        "number_of_replicas" : replicas } }], sort_keys=True, indent=4)

    request = requests.post('http://' + host + ':' + port + '/' + indexname,
            data=data_out)

    data_in = json.loads(request.content)

    if not request.status_code == requests.codes.ok:
        print
        print 'ERROR - Error Creating Index'
        print
        print ' Status Code:', request.status_code
        print ' Error Message:', data_in[u'error']
        print
        print ' Host:', host
        print ' Replicas:', replicas
        print ' Shards:', shards
        print
    else:
        print
        print 'SUCCESS - Index "' + indexname + '" Created Successfully'
        print
        print ' Host:', host
        print ' Replicas:', replicas
        print ' Shards:', shards
        print

#def index_delete(host, indexname):
