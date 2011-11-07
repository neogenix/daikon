import requests
import anyjson
import sys


def cluster_status(cluster, host, port, extended):
    try:
        request = requests.get('http://' + host + ':' + port +
                '/_cluster/state')
        if request.error is not None:
            print 'ERROR: Fetching Cluster Status : "' + cluster + '" -', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Fetching Cluster Status : "' + cluster + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Fetching Cluster Status : "' + cluster + '"\n'
        data_result = json.loads(request.content)
        master_node = data_result[u'master_node']

        print '\t Information:'
        print '\t\t Cluster Name:', data_result[u'cluster_name']
        print '\t\t Master Node:', data_result[u'master_node']
        if extended:
            print '\t\t\t Name:', data_result[u'nodes'][master_node][u'name']
            print '\t\t\t Transport Address:', data_result[u'nodes'][master_node][u'transport_address']

        print '\t Indices:'
        for index in data_result[u'metadata'][u'indices']:
            print '\t\t Name:', index
            if extended:
                print '\t\t\t State:', data_result[u'metadata'][u'indices'][index][u'state']
                print '\t\t\t Replicas:', data_result[u'metadata'][u'indices'][index][u'settings'][u'index.number_of_replicas']
                print '\t\t\t Shards:', data_result[u'metadata'][u'indices'][index][u'settings'][u'index.number_of_shards']

        print '\t Nodes:'
        for node in data_result[u'nodes']:
            print '\t\t Node:', node
            if extended:
                print '\t\t\t Name:', data_result[u'nodes'][node][u'name']
                print '\t\t\t Transport Address:', data_result[u'nodes'][node][u'transport_address']
