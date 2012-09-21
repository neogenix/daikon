#
#   Copyright [2011] [Patrick Ancillotti]
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import requests
import anyjson as json
import urllib2

from daikon import exceptions


class Cluster:

    def __init__(self, arguments):
        self.arguments = arguments

    def cluster_status(self, cluster, host, port, extended):
        try:
            request_health_url = 'http://%s:%s/_cluster/health?level=indices' \
                    % (host, port)
            request_health = requests.get(request_health_url)
            request_health.raise_for_status()

            request_state_url = 'http://%s:%s/_cluster/state' % (host, port)
            request_state = requests.get(request_state_url)
            request_state.raise_for_status()

            print 'SUCCESS: Fetching Cluster Status : "%s"\n' % (cluster)
            result_state = json.loads(request_state.content)
            result_health = json.loads(request_health.content)[u'indices']
            master_node = result_state[u'master_node']
            master_node_state = result_state[u'nodes'][master_node]

            print '\t Information:'
            print '\t\t Cluster Name: %s' % (result_state[u'cluster_name'])
            print '\t\t Master Node: %s' % (result_state[u'master_node'])
            if extended:
                print '\t\t\t Name: %s' % (master_node_state[u'name'])
                print '\t\t\t Transport Address: %s' % \
                        (master_node_state[u'transport_address'])

            print '\t Indices:'
            for index in result_state[u'metadata'][u'indices']:
                print '\t\t Name: %s' % (index)
                if extended:
                    index_result = result_state[u'metadata'][u'indices'][index]
                    print '\t\t\t State: %s' % (index_result[u'state'])
                    print '\t\t\t Replicas: %s' % \
                            (index_result[u'settings']
                                    [u'index.number_of_replicas'])
                    print '\t\t\t Shards: %s' % \
                            (index_result[u'settings']
                                    [u'index.number_of_shards'])
                    if index_result[u'state'] == 'close':
                        print '\t\t\t Status: CLOSED'
                    else:
                        print '\t\t\t Status: %s' % \
                                (result_health[index][u'status'])

            print '\t Nodes:'
            for node in result_state[u'nodes']:
                print '\t\t Node: %s' % (node)
                if extended:
                    print '\t\t\t Name: %s' % \
                            (result_state[u'nodes'][node][u'name'])
                    print '\t\t\t Transport Address: %s' % \
                            (result_state[u'nodes'][node]
                                    [u'transport_address'])

        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Error Fetching Cluster Status - %s' % (e)
            raise exceptions.ActionClusterError(msg)

    def cluster_shutdown(self, cluster, host, port):
        try:
            request_url = 'http://%s:%s/_shutdown' % (host, port)
            request = requests.post(request_url)
            request.raise_for_status()
            print 'SUCCESS: Shutting Down Cluster : "%s"' % (cluster)
        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Shutting Down Cluster - %s' % (e)
            raise exceptions.ActionClusterError(msg)
