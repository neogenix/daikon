import requests
import json

def index_create(host, indexname, shards, replicas):
    data = json.dumps([{"index" : { "number_of_shards" : shards,
        "number_of_replicas": replicas } }], sort_keys = True, indent = 4)
    request = requests.post('http://' + host + '/' + indexname)
    print data

#def index_delete(host, indexname):

