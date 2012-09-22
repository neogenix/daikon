#
#   Copyright [2012] [Patrick Ancillotti]
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

import argparse as arg


class Parser(object):

    def __init__(self, version):
        self._version = version
        self._main = None

    def setup(self):
        self._main = arg.ArgumentParser(description='ElasticSearch CLI v%s' % (self._version))
        self._main.add_argument('--version', action='version', version=self._version)
        self._main.add_argument('--cluster')
        self._main.add_argument('--host')
        self._main.add_argument('--port')

        main_sub = self._main.add_subparsers(title='subcommands', description='valid subcommands', help='additional help', dest='sub_main')

        # index

        sub_index = main_sub.add_parser('index')
        sub_index = sub_index.add_subparsers(title='subcommands', description='valid subcommands', help='additional help', dest='sub_index_name')

        # index create

        sub_index_create = sub_index.add_parser('create')
        sub_index_create.add_argument('sub_index_create_indexname', metavar='indexname')
        sub_index_create.add_argument('--cluster')
        sub_index_create.add_argument('--shards')
        sub_index_create.add_argument('--replicas')
        sub_index_create.add_argument('--host')
        sub_index_create.add_argument('--port')

        # index delete

        sub_index_delete = sub_index.add_parser('delete')
        sub_index_delete.add_argument('sub_index_delete_indexname', metavar='indexname')
        sub_index_delete.add_argument('--cluster')
        sub_index_delete.add_argument('--host')
        sub_index_delete.add_argument('--port')

        # index open

        sub_index_open = sub_index.add_parser('open')
        sub_index_open.add_argument('sub_index_open_indexname', metavar='indexname')
        sub_index_open.add_argument('--cluster')
        sub_index_open.add_argument('--host')
        sub_index_open.add_argument('--port')

        # index close

        sub_index_close = sub_index.add_parser('close')
        sub_index_close.add_argument('sub_index_close_indexname', metavar='indexname')
        sub_index_close.add_argument('--cluster')
        sub_index_close.add_argument('--host')
        sub_index_close.add_argument('--port')

        # index status

        sub_index_status = sub_index.add_parser('status')
        sub_index_status.add_argument('sub_index_status_indexname', metavar='indexname')
        sub_index_status.add_argument('--cluster')
        sub_index_status.add_argument('--host')
        sub_index_status.add_argument('--port')
        sub_index_status.add_argument('--extended', action='store_true')
        sub_index_status.add_argument('--display', choices=['extended', 'regular'])

        # index list

        sub_index_list = sub_index.add_parser('list')
        sub_index_list.add_argument('--cluster')
        sub_index_list.add_argument('--host')
        sub_index_list.add_argument('--port')
        sub_index_list.add_argument('--extended', action='store_true')

        # cluster

        sub_cluster = main_sub.add_parser('cluster')
        sub_cluster = sub_cluster.add_subparsers(title='subcommands', description='valid subcommands', help='additional help', dest='sub_cluster_name')

        # cluster status

        sub_cluster_status = sub_cluster.add_parser('status')
        sub_cluster_status.add_argument('--cluster')
        sub_cluster_status.add_argument('--host')
        sub_cluster_status.add_argument('--port')
        sub_cluster_status.add_argument('--extended', action='store_true')

        # cluster shutdown

        sub_cluster_shutdown = sub_cluster.add_parser('shutdown')
        sub_cluster_shutdown.add_argument('--cluster')
        sub_cluster_shutdown.add_argument('--host')
        sub_cluster_shutdown.add_argument('--port')

        # node

        sub_node = main_sub.add_parser('node')
        sub_node = sub_node.add_subparsers(title='subcommands', description='valid subcommands', help='additional help', dest='sub_node_name')

        # node list

        sub_node_list = sub_node.add_parser('list')
        sub_node_list.add_argument('--cluster')
        sub_node_list.add_argument('--host')
        sub_node_list.add_argument('--port')
        sub_node_list.add_argument('--extended', action='store_true')

        # node status

        sub_node_status = sub_node.add_parser('status')
        sub_node_status.add_argument('sub_node_status_hostname', metavar='hostname')
        sub_node_status.add_argument('--cluster')
        sub_node_status.add_argument('--port')
        sub_node_status.add_argument('--extended', action='store_true')

        # node shutdown

        sub_node_shutdown = sub_node.add_parser('shutdown')
        sub_node_shutdown.add_argument('sub_node_shutdown_hostname', metavar='hostname')
        sub_node_shutdown.add_argument('--delay', default=0)
        sub_node_shutdown.add_argument('--port')
        sub_node_shutdown.add_argument('--cluster')

    def get_results(self):
        return self._main.parse_args()
