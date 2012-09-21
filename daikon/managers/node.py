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


class Node:

    def __init__(self, arguments):
        self.arguments = arguments

    def node_status(self, host, port, extended):
        try:
            req_url = 'http://%s:%s/_cluster/nodes/_local/stats' \
                      % (host, port)
            req = requests.get(req_url)
            req.raise_for_status()
            res = json.loads(req.content)
            print 'SUCCESS: Fetching Index Status : "%s"' % (host)
            var = {}

            for node in res[u'nodes']:
                content = ('\t Status:\n'
                           '\t\t Node Status:\n'
                           '\t\t\t Cluster: %(cluster)s\n'
                           '\t\t\t ID: %(id)s')
                var['cluster'] = res[u'cluster_name']
                var['id'] = node
                print content % var
                res_n = res[u'nodes'][node]

                if not extended:
                    content = ('\t\t Index Status:\n'
                               '\t\t\t Size: %(size)s')
                    var['size'] = res_n[u'indices'][u'store'][u'size']
                    print content % var

                else:
                    content = ('\t\t\t Name: %(name)s\n'
                               '\t\t Index Status:\n'
                               '\t\t\t Size: %(size)s\n'
                               '\t\t\t Get (Total): %(get_total)s\n'
                               '\t\t\t Get (Time): %(get_time)s\n'
                               '\t\t\t Searches (Total): %(search_total)s\n'
                               '\t\t\t Searches (Time): %(search_time)s\n'
                               '\t\t OS Status:\n'
                               '\t\t\t Uptime: %(uptime)s\n'
                               '\t\t\t Load Average: %(load_ave)s\n'
                               '\t\t\t Memory Status:\n'
                               '\t\t\t\t Memory (Free): %(mem_free)s\n'
                               '\t\t\t\t Memory (Used): %(mem_used)s\n'
                               '\t\t\t Swap Status:\n'
                               '\t\t\t\t Swap (Free): %(swap_free)s\n'
                               '\t\t\t\t Swap (Used): %(swap_used)s')
                    var['name'] = res_n[u'name']
                    var['size'] = res_n[u'indices'][u'store'][u'size']
                    var['get_total'] = res_n[u'indices'][u'get'][u'total']
                    var['get_time'] = res_n[u'indices'][u'get'][u'time']
                    search = res_n[u'indices'][u'search']
                    var['search_total'] = search[u'query_total']
                    var['search_time'] = search[u'query_time']
                    os = res_n[u'os']
                    var['uptime'] = os[u'uptime']
                    var['load_ave'] = os[u'load_average']
                    var['mem_free'] = os[u'mem'][u'free']
                    var['mem_used'] = os[u'mem'][u'used']
                    var['swap_free'] = os[u'swap'][u'free']
                    var['swap_used'] = os[u'swap'][u'used']
                    print content % var

        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Error Fetching Node Status - %s' % (e)
            raise exceptions.ActionNodeError(msg)

    def node_list(self, host, port, extended):
        ''' List Nodes Here '''

        try:
            req_url = 'http://%s:%s/_cluster/state' % (host, port)
            req = requests.get(req_url)
            req.raise_for_status()
            res = json.loads(req.content)[u'nodes']
            print 'SUCCESS: Fetching Node List :\n'
            var = {}

            for node in res:
                print '\t\t Node: %s' % (node)

                if extended:
                    var['name'] = res[node][u'name']
                    var['t_address'] = res[node][u'transport_address']
                    content = ('\t\t\t Name: %(name)s\n'
                               '\t\t\t Transport Address: %(t_address)s')
                    print content % var

        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Error Fetching Node List - %s' % (e)
            raise exceptions.ActionNodeError(msg)

    def node_shutdown(self, host, port, delay):
        ''' Shutdown a Node Here '''

        try:
            req_url = ('http://%s:%s/_cluster/nodes/_local/'
                       '_shutdown?delay=%ss') % (host, port, delay)
            req = requests.post(req_url)
            req.raise_for_status()
            print 'SUCCESS: Shutting Down Node : "%s"' % (host)

        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Error Shutting Down Node - %s' % (e)
            raise exceptions.ActionNodeError(msg)
