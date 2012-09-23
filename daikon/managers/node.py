# -*- coding: utf-8 -*-
#
#   Copyright [2011] [Patrick Ancillotti]
#   Copyright [2011] [Jason Kölker]
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

# ---------------------
# Imports
# ---------------------

import logging
import requests
import urllib2
import anyjson as json

from daikon import exceptions

# ---------------------
# Logging
# ---------------------

log = logging.getLogger('daikon')


# ---------------------
# Classes
# ---------------------

class Node(object):

    def __init__(self, arguments, d):
        self.d = d
        self.arguments = arguments

    def node_status(self, host, port, extended):
        try:
            req_url = 'http://%s:%s/_cluster/nodes/_local/stats' \
                      % (host, port)
            req = requests.get(req_url)
            req.raise_for_status()
            res = json.loads(req.content)
            self.d.print_output('SUCCESS: Fetching Index Status : "%s"', host)

            for node in res[u'nodes']:
                self.d.print_output('Status:', level=1)
                self.d.print_output('Node Status:', level=2)
                self.d.print_output('Cluster: %s',
                                    res[u'cluster_name'],
                                    level=3)
                self.d.print_output('ID: %s', node, level=3)

                res_n = res[u'nodes'][node]

                if not extended:
                    self.d.print_output('Index Status:', level=2)
                    self.d.print_output('Size: %s',
                                        res_n[u'indices'][u'store'][u'size'],
                                        level=3)

                else:
                    self.d.print_output('Name: %s', res_n[u'name'], level=3)
                    self.d.print_output('Index Status:', level=2)
                    self.d.print_output('Size: %s',
                                        res_n[u'indices'][u'store'][u'size'],
                                        level=3)
                    self.d.print_output('Get (Total): %s',
                                        res_n[u'indices'][u'get'][u'total'],
                                        level=3)
                    self.d.print_output('Get (Time): %s',
                                        res_n[u'indices'][u'get'][u'time'],
                                        level=3)
                    self.d.print_output('Searches (Total): %s',
                                        res_n[u'indices'][u'search']
                                            [u'query_total'],
                                        level=3)
                    self.d.print_output('Searches (Time): %s',
                                        res_n[u'indices'][u'search']
                                            [u'query_time'],
                                        level=3)

        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Error Fetching Node Status - %s' % (e)
            raise exceptions.ActionNodeError(msg)

    def node_list(self, host, port, extended):

        try:
            req_url = 'http://%s:%s/_cluster/state' % (host, port)
            req = requests.get(req_url)
            req.raise_for_status()
            res = json.loads(req.content)[u'nodes']
            self.d.print_output('SUCCESS: Fetching Node List :')

            for node in res:
                self.d.print_output('Node: %s', node, level=2)

                if extended:
                    self.d.print_output('Name: %s',
                                        res[node][u'name'],
                                        level=3)
                    self.d.print_output('Transport Address: %s',
                                        res[node][u'transport_address'],
                                        level=3)

        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Error Fetching Node List - %s' % (e)
            raise exceptions.ActionNodeError(msg)

    def node_shutdown(self, host, port, delay):

        try:
            req_url = ('http://%s:%s/_cluster/nodes/_local/'
                       '_shutdown?delay=%ss') % (host, port, delay)
            req = requests.post(req_url)
            req.raise_for_status()
            self.d.print_output('SUCCESS: Shutting Down Node : "%s"', host)

        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Error Shutting Down Node - %s' % (e)
            raise exceptions.ActionNodeError(msg)
