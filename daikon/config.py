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

import ConfigParser
import os.path

from exceptions import ConfigError


class configuration:
    _host = None
    _port = None

    def __init__(self, arguments):
        self.arguments = arguments

    def config_setup(self):
        """ Setup configuration, and read config files """

        self.config_parser = ConfigParser.ConfigParser()

        if not self.config_parser.read(['/etc/daikon/daikon.conf',
                os.path.expanduser('~/.daikon.conf'), 'daikon.conf']):
            raise ConfigError('No config file found!\n')
        elif not self.config_parser.has_section(self.cluster()):
            raise ConfigError('No cluster section defined for this cluster!\n')
        else:
            return self.config_parser

    def cluster(self):
        """ Cluster configuration """

        if hasattr(self.arguments, "cluster") and self.arguments.cluster is not None:
            cluster = self.arguments.cluster
        else:
            cluster = 'default'
        return cluster

    def host(self):
        """ Host configuration """
        if self._host is not None:
            return self._host

        if not self.config_parser.get(self.cluster(), 'host'):
            raise ConfigError('No default host defined!\n')
        elif hasattr(self.arguments, 'host') and self.arguments.host:
            host = self.arguments.host
        else:
            host = self.config_parser.get(self.cluster(), 'host')

        self._host = host
        return host

    def port(self):
        """ Port configuration """
        if self._port is not None:
            return self._port

        if not self.config_parser.get(self.cluster(), 'port'):
            raise ConfigError('No default port defined!\n')
        elif hasattr(self.arguments, 'port') and self.arguments.port:
            port = self.arguments.port
        else:
            port = self.config_parser.get(self.cluster(), 'port')

        self._port = port
        return port

    def replicas(self):
        """ Replicas configuration """

        if not self.config_parser.get(self.cluster(), 'replicas'):
            raise ConfigError('No default replicas defined!\n')
        elif hasattr(self.arguments, 'replicas') and self.arguments.replicas:
            replicas = self.arguments.replicas
        else:
            replicas = self.config_parser.get(self.cluster(), 'replicas')
        return replicas

    def shards(self):
        """ Shards configuration """

        if not self.config_parser.get(self.cluster(), 'shards'):
            raise ConfigError('No default shards defined!\n')
        elif hasattr(self.arguments, 'shards') and self.arguments.shards:
            shards = self.arguments.shards
        else:
            shards = self.config_parser.get(self.cluster(), 'shards')
        return shards
