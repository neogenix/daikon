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
import sys
import urllib2

from exceptions import ActionNodeError


def node_status(host, port, extended):
    try:
        request_url = 'http://%s:%s/_cluster/nodes/_local/stats' % (host, port)
        request = requests.get(request_url)
        request.raise_for_status()
        print 'SUCCESS: Fetching Index Status : "%s"\n' % (host)

        data_result = json.loads(request.content)
        for node in data_result[u'nodes']:
            print '\t Status:'
            print '\t\t Node Status:'
            print '\t\t\t Cluster: %s' % (data_result[u'cluster_name'])
            print '\t\t\t ID: %s' % (node)
            if extended:
                print '\t\t\t Name: %s' % \
                        (data_result[u'nodes'][node][u'name'])

            print '\t\t Index Status:'
            print '\t\t\t Size: %s' % \
                    (data_result[u'nodes'][node][u'indices'][u'store'][u'size'])
            if extended:
                print '\t\t\t Get (Total): %s' % \
                        (data_result[u'nodes'][node][u'indices'][u'get'][u'total'])
                print '\t\t\t Get (Time): %s' % \
                        data_result[u'nodes'][node][u'indices'][u'get'][u'time']
                print '\t\t\t Searches (Total): %s' % \
                        (data_result[u'nodes'][node][u'indices'][u'search'][u'query_total'])
                print '\t\t\t Searches (Time): %s' % \
                        (data_result[u'nodes'][node][u'indices'][u'search'][u'query_time'])

            if extended:
                print '\t\t OS Status:'
                print '\t\t\t Uptime: %s' % \
                        (data_result[u'nodes'][node][u'os'][u'uptime'])
                print '\t\t\t Load Average: %s' % \
                        (data_result[u'nodes'][node][u'os'][u'load_average'])
                print '\t\t\t Memory Status:'
                print '\t\t\t\t Memory (Free): %s' % \
                        (data_result[u'nodes'][node][u'os'][u'mem'][u'free'])
                print '\t\t\t\t Memory (Used): %s' % \
                        (data_result[u'nodes'][node][u'os'][u'mem'][u'used'])
                print '\t\t\t Swap Status:'
                print '\t\t\t\t Swap (Free): %s' % \
                        (data_result[u'nodes'][node][u'os'][u'swap'][u'free'])
                print '\t\t\t\t Swap (Used): %s' % \
                        (data_result[u'nodes'][node][u'os'][u'swap'][u'used'])
    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionNodeError('Error Fetching Node Status - %s' % (e))


def node_list(host, port, extended):
    try:
        request_url = 'http://%s:%s/_cluster/state' % (host, port)
        request = requests.get(request_url)
        print 'SUCCESS: Fetching Node List :\n'

        data_result = json.loads(request.content)[u'nodes']
        print '\t Nodes:'
        for node in data_result:
            print '\t\t Node:', node
            if extended:
                print '\t\t\t Name:', data_result[node][u'name']
                print '\t\t\t Transport Address:', data_result[node][u'transport_address']
    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionNodeError('Error Fetching Node List - %s' % (e))


def node_shutdown(host, port, delay):
    try:
        request_url = 'http://%s:%s/_cluster/nodes/_local/_shutdown?delay=%ss' \
                % (host, port, delay)
        request = requests.post(request_url)
        request.raise_for_status()
        print 'SUCCESS: Shutting Down Node : "' + host + '"'
    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionNodeError('Error Shutting Down Node - %s' % (e))
