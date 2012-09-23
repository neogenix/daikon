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
import ConfigParser
import os.path
import anyjson as json

from daikon import exceptions

# ---------------------
# Logging
# ---------------------

log = logging.getLogger('daikon')


# ---------------------
# Classes
# ---------------------

class Config(object):

    def __init__(self, arguments):
        self.arguments = arguments
        self._cluster = None
        self._host = None
        self._port = None
        self._replicas = None
        self._shards = None
        self._version = None

    def setup(self):
        ''' Setup configuration, and read config files '''

        self.config_parser = ConfigParser.ConfigParser()

        if not self.config_parser.read(
                ['/etc/daikon/daikon.conf',
                    os.path.expanduser('~/.daikon.conf'), 'daikon.conf']):
            msg = 'No config file found!'
            raise exceptions.ConfigError(msg)
        elif not self.config_parser.has_section(self.cluster()):
            msg = 'No cluster section defined for this cluster!'
            raise exceptions.ConfigError(msg)
        else:
            return self.config_parser

    def cluster(self):
        ''' Cluster configuration '''

        if self._cluster is not None:
            return self._cluster

        if hasattr(self.arguments, 'cluster') and \
                self.arguments.cluster is not None:
            self._cluster = self.arguments.cluster
        else:
            self._cluster = 'default'

        return self._cluster

    def host(self):
        ''' Host configuration '''

        if self._host is not None:
            return self._host

        if not self.config_parser.get(self.cluster(), 'host'):
            raise exceptions.ConfigError('No default host defined!')
        elif hasattr(self.arguments, 'host') and self.arguments.host:
            self._hsot = self.arguments.host
        else:
            self._host = self.config_parser.get(self.cluster(), 'host')

        return self._host

    def port(self):
        ''' Port configuration '''

        if self._port is not None:
            return self._port

        if not self.config_parser.get(self.cluster(), 'port'):
            raise exceptions.ConfigError('No default port defined!')
        elif hasattr(self.arguments, 'port') and self.arguments.port:
            self._port = self.arguments.port
        else:
            self._port = self.config_parser.get(self.cluster(), 'port')

        return self._port

    def replicas(self):
        ''' Replicas configuration '''

        if self._replicas is not None:
            return self._replicas

        if not self.config_parser.get(self.cluster(), 'replicas'):
            raise exceptions.ConfigError('No default replicas defined!')
        elif hasattr(self.arguments, 'replicas') and self.arguments.replicas:
            self._replicas = self.arguments.replicas
        else:
            self._replicas = self.config_parser.get(self.cluster(), 'replicas')

        return self._replicas

    def shards(self):
        ''' Shards configuration '''

        if self._shards is not None:
            return self._shards

        if not self.config_parser.get(self.cluster(), 'shards'):
            raise exceptions.ConfigError('No default shards defined!')
        elif hasattr(self.arguments, 'shards') and self.arguments.shards:
            self._shards = self.arguments.shards
        else:
            self._shards = self.config_parser.get(self.cluster(), 'shards')

        return self._shards

    def version(self):
        ''' Get ElasticSearch Version '''

        if self._version is not None:
            return self._version

        if self._host is None:
            self._host = self.host()

        if self._port is None:
            self._port = self.port()

        try:
            request_url = 'http://%s:%s' % (self._host, self._port)
            request = requests.get(request_url)
            request.raise_for_status()
            self._version = json.loads(request.content)[u'version'][u'number']
            return self._version
        except requests.RequestException, e:
            raise exceptions.ConfigError('Error fetching version - ' + str(e))
