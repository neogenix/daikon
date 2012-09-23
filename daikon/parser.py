# -*- coding: utf-8 -*-
#
#   Copyright [2012] [Patrick Ancillotti]
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
import argparse as arg

# ---------------------
# Logging
# ---------------------

log = logging.getLogger('daikon')


# ---------------------
# Classes
# ---------------------

class Parser(object):

    def __init__(self, version):
        self._version = version
        self._main = None

    def setup(self):
        self._main = arg.ArgumentParser(description='ElasticSearch CLI v%s' %
                                        (self._version))
        self._main.add_argument('--version', action='version',
                                version=self._version)
        self._main.add_argument('--cluster')
        self._main.add_argument('--host')
        self._main.add_argument('--port')

        main_sub = self._main.add_subparsers(title='subcommands',
                                             description='valid subcommands',
                                             help='additional help',
                                             dest='main_sub')

        # index

        index = main_sub.add_parser('index')
        index = index.add_subparsers(title='subcommands',
                                     description='valid subcommands',
                                     help='additional help',
                                     dest='index_name')

        # index create

        index_create = index.add_parser('create')
        index_create.add_argument('index_create_indexname',
                                  metavar='indexname')
        index_create.add_argument('--cluster')
        index_create.add_argument('--shards')
        index_create.add_argument('--replicas')
        index_create.add_argument('--host')
        index_create.add_argument('--port')

        # index delete

        index_delete = index.add_parser('delete')
        index_delete.add_argument('index_delete_indexname',
                                  metavar='indexname')
        index_delete.add_argument('--cluster')
        index_delete.add_argument('--host')
        index_delete.add_argument('--port')

        # index open

        index_open = index.add_parser('open')
        index_open.add_argument('index_open_indexname',
                                metavar='indexname')
        index_open.add_argument('--cluster')
        index_open.add_argument('--host')
        index_open.add_argument('--port')

        # index close

        index_close = index.add_parser('close')
        index_close.add_argument('index_close_indexname',
                                 metavar='indexname')
        index_close.add_argument('--cluster')
        index_close.add_argument('--host')
        index_close.add_argument('--port')

        # index status

        index_status = index.add_parser('status')
        index_status.add_argument('index_status_indexname',
                                  metavar='indexname')
        index_status.add_argument('--cluster')
        index_status.add_argument('--host')
        index_status.add_argument('--port')
        index_status.add_argument('--extended', action='store_true')
        index_status.add_argument('--display', choices=['extended', 'regular'])

        # index list

        index_list = index.add_parser('list')
        index_list.add_argument('--cluster')
        index_list.add_argument('--host')
        index_list.add_argument('--port')
        index_list.add_argument('--extended', action='store_true')

        # cluster

        cluster = main_sub.add_parser('cluster')
        cluster = cluster.add_subparsers(title='subcommands',
                                         description='valid subcommands',
                                         help='additional help',
                                         dest='cluster_name')

        # cluster status

        cluster_status = cluster.add_parser('status')
        cluster_status.add_argument('--cluster')
        cluster_status.add_argument('--host')
        cluster_status.add_argument('--port')
        cluster_status.add_argument('--extended', action='store_true')

        # cluster shutdown

        cluster_shutdown = cluster.add_parser('shutdown')
        cluster_shutdown.add_argument('--cluster')
        cluster_shutdown.add_argument('--host')
        cluster_shutdown.add_argument('--port')

        # node

        node = main_sub.add_parser('node')
        node = node.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='additional help',
                                   dest='node_name')

        # node list

        node_list = node.add_parser('list')
        node_list.add_argument('--cluster')
        node_list.add_argument('--host')
        node_list.add_argument('--port')
        node_list.add_argument('--extended', action='store_true')

        # node status

        node_status = node.add_parser('status')
        node_status.add_argument('node_status_hostname',
                                 metavar='hostname')
        node_status.add_argument('--cluster')
        node_status.add_argument('--port')
        node_status.add_argument('--extended', action='store_true')

        # node shutdown

        node_shutdown = node.add_parser('shutdown')
        node_shutdown.add_argument('node_shutdown_hostname',
                                   metavar='hostname')
        node_shutdown.add_argument('--delay', default=0)
        node_shutdown.add_argument('--port')
        node_shutdown.add_argument('--cluster')

    def get_results(self):
        return self._main.parse_args()
