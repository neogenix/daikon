import requests
import anyjson as json
import sys


def cluster_status(cluster, host, port, extended):
    try:
        request_health = requests.get('http://' + host + ':' + port +
                '/_cluster/health?level=indices')
        if request_health.error is not None:
            print 'ERROR: Fetching Cluster Status : "' + cluster + '" -', request_health.error
            sys.exit(1)
        else:
            request_health.raise_for_status()

        request_state = requests.get('http://' + host + ':' + port +
                '/_cluster/state')
        if request_state.error is not None:
            print 'ERROR: Fetching Cluster Status : "' + cluster + '" -', request_state.error
            sys.exit(1)
        else:
            request_state.raise_for_status()
    except request_health.RequestException, e:
        print 'ERROR: Fetching Cluster Status : "' + cluster + '" -',  e
        sys.exit(1)
    except requests.RequestException, e:
        print 'ERROR: Fetching Cluster Status : "' + cluster + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Fetching Cluster Status : "' + cluster + '"\n'
        data_result_state = json.loads(request_state.content)
        data_result_health = json.loads(request_health.content)[u'indices']
        master_node = data_result_state[u'master_node']

        print '\t Information:'
        print '\t\t Cluster Name:', data_result_state[u'cluster_name']
        print '\t\t Master Node:', data_result_state[u'master_node']
        if extended:
            print '\t\t\t Name:', data_result_state[u'nodes'][master_node][u'name']
            print '\t\t\t Transport Address:', data_result_state[u'nodes'][master_node][u'transport_address']

        print '\t Indices:'
        for index in data_result_state[u'metadata'][u'indices']:
            print '\t\t Name:', index
            if extended:
                print '\t\t\t State:', data_result_state[u'metadata'][u'indices'][index][u'state']
                print '\t\t\t Replicas:', data_result_state[u'metadata'][u'indices'][index][u'settings'][u'index.number_of_replicas']
                print '\t\t\t Shards:', data_result_state[u'metadata'][u'indices'][index][u'settings'][u'index.number_of_shards']
                if data_result_state[u'metadata'][u'indices'][index][u'state'] == 'close':
                    print '\t\t\t Status: CLOSED'
                else:
                    print '\t\t\t Status:', data_result_health[index][u'status']

        print '\t Nodes:'
        for node in data_result_state[u'nodes']:
            print '\t\t Node:', node
            if extended:
                print '\t\t\t Name:', data_result_state[u'nodes'][node][u'name']
                print '\t\t\t Transport Address:', data_result_state[u'nodes'][node][u'transport_address']


def cluster_shutdown(cluster, host, port):
    try:
        request = requests.post('http://' + host + ':' + port + '/_shutdown' )
        if request.error is not None:
            print 'ERROR: Shutting Down Cluster : "' + cluster + '" -', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Shutting Down Cluster : "' + cluster + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Shutting Down Cluster : "' + cluster + '"'
