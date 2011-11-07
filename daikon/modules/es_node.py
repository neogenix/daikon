import requests
import anyjson as json
import sys

def node_status(host, port, extended):
    try:
        request = requests.get('http://' + host + ':' + port +
                '/_cluster/nodes/_local/stats')
        if request.error is not None:
            print 'ERROR: Fetching Node Status : "' + host + '" -', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Fetching Index Status : "' + host + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Fetching Index Status : "' + host + '"\n'
        data_result = json.loads(request.content)

        for node in data_result[u'nodes']:
            print '\t Status:'

            print '\t\t Node Status:'
            print '\t\t\t Cluster:', data_result[u'cluster_name']
            print '\t\t\t ID:', node
            if extended:
                print '\t\t\t Name:', data_result[u'nodes'][node][u'name']

            print '\t\t Index Status:'
            print '\t\t\t Size:', data_result[u'nodes'][node][u'indices'][u'store'][u'size']
            if extended:
                print '\t\t\t Get (Total):', data_result[u'nodes'][node][u'indices'][u'get'][u'total']
                print '\t\t\t Get (Time):', data_result[u'nodes'][node][u'indices'][u'get'][u'time']
                print '\t\t\t Searches (Total):', data_result[u'nodes'][node][u'indices'][u'search'][u'query_total']
                print '\t\t\t Searches (Time):', data_result[u'nodes'][node][u'indices'][u'search'][u'query_time']

            if extended:
                print '\t\t OS Status:'
                print '\t\t\t Uptime:', data_result[u'nodes'][node][u'os'][u'uptime']
                print '\t\t\t Load Average:', data_result[u'nodes'][node][u'os'][u'load_average']
                print '\t\t\t Memory Status:'
                print '\t\t\t\t Memory (Free):', data_result[u'nodes'][node][u'os'][u'mem'][u'free']
                print '\t\t\t\t Memory (Used):', data_result[u'nodes'][node][u'os'][u'mem'][u'used']
                print '\t\t\t Swap Status:'
                print '\t\t\t\t Swap (Free):', data_result[u'nodes'][node][u'os'][u'swap'][u'free']
                print '\t\t\t\t Swap (Used):', data_result[u'nodes'][node][u'os'][u'swap'][u'used']


def node_list(host, port, extended):
    try:
        request = requests.get('http://' + host + ':' + port +
                '/_cluster/state')
        if request.error is not None:
            print 'ERROR: Fetching Node List :', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Fetching Node List :',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Fetching Node List :\n'
        data_result = json.loads(request.content)

        print '\t Nodes:'
        for node in data_result[u'nodes']:
            print '\t\t Node:', node
            if extended:
                print '\t\t\t Name:', data_result[u'nodes'][node][u'name']
                print '\t\t\t Transport Address:', data_result[u'nodes'][node][u'transport_address']


def node_shutdown(host, port, delay):
    try:
        if delay is not None:
            request = requests.post('http://' + host + ':' + port +
                '/_cluster/nodes/_local/_shutdown?delay=' + delay + 's')
        else:
            request = requests.post('http://' + host + ':' + port +
                '/_cluster/nodes/_local/_shutdown')

        if request.error is not None:
            print 'ERROR: Shutting Down Node : "' + host + '" -', request.error
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Shutting Down Node : "' + host + '" -',  e
        sys.exit(1)
    else:
        print 'SUCCESS: Shutting Down Node : "' + host + '"'
