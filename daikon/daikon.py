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

#!/usr/bin/env python

import index
import cluster
import node
import argparse

from config import configuration
from exceptions import ConfigError

VERSION = __import__('daikon').__version__


def main():
    parser_main = argparse.ArgumentParser(description='ElasticSearch CLI v'
            + VERSION)

    parser_main.add_argument('--version', action='version',
            version=VERSION)

    parser_main.add_argument('--cluster')
    parser_main.add_argument('--host')
    parser_main.add_argument('--port')

    subparsers_main = parser_main.add_subparsers(title='subcommands',
            description='valid subcommands', help='additional help',
            dest='subparsers_main')

    # index

    subparser_index = subparsers_main.add_parser('index')
    subparser_index = subparser_index.add_subparsers(title='subcommands',
            description='valid subcommands', help='additional help',
            dest='subparser_index_name')

    # index create

    subparser_index_create = subparser_index.add_parser('create')
    subparser_index_create.add_argument('subarser_index_create_indexname',
            metavar='indexname')
    subparser_index_create.add_argument('--cluster')
    subparser_index_create.add_argument('--shards')
    subparser_index_create.add_argument('--replicas')
    subparser_index_create.add_argument('--host')
    subparser_index_create.add_argument('--port')

    # index delete

    subparser_index_delete = subparser_index.add_parser('delete')
    subparser_index_delete.add_argument('subparser_index_delete_indexname',
            metavar='indexname')
    subparser_index_delete.add_argument('--cluster')
    subparser_index_delete.add_argument('--host')
    subparser_index_delete.add_argument('--port')

    # index open

    subparser_index_open = subparser_index.add_parser('open')
    subparser_index_open.add_argument('subparser_index_open_indexname',
            metavar='indexname')
    subparser_index_open.add_argument('--cluster')
    subparser_index_open.add_argument('--host')
    subparser_index_open.add_argument('--port')

    # index close

    subparser_index_close = subparser_index.add_parser('close')
    subparser_index_close.add_argument('subparser_index_close_indexname',
            metavar='indexname')
    subparser_index_close.add_argument('--cluster')
    subparser_index_close.add_argument('--host')
    subparser_index_close.add_argument('--port')

    # index status

    subparser_index_status = subparser_index.add_parser('status')
    subparser_index_status.add_argument('subparser_index_status_indexname',
            metavar='indexname')
    subparser_index_status.add_argument('--cluster')
    subparser_index_status.add_argument('--host')
    subparser_index_status.add_argument('--port')
    subparser_index_status.add_argument('--extended', action='store_true')

    # index list

    subparser_index_list = subparser_index.add_parser('list')
    subparser_index_list.add_argument('--cluster')
    subparser_index_list.add_argument('--host')
    subparser_index_list.add_argument('--port')
    subparser_index_list.add_argument('--extended', action='store_true')

    # cluster

    subparser_cluster = subparsers_main.add_parser('cluster')
    subparser_cluster = subparser_cluster.add_subparsers(title='subcommands',
            description='valid subcommands', help='additional help',
            dest='subparser_cluster_name')

    # cluster status

    subparser_cluster_status = subparser_cluster.add_parser('status')
    subparser_cluster_status.add_argument('--cluster')
    subparser_cluster_status.add_argument('--host')
    subparser_cluster_status.add_argument('--port')
    subparser_cluster_status.add_argument('--extended', action='store_true')

    # cluster shutdown

    subparser_cluster_shutdown = subparser_cluster.add_parser('shutdown')
    subparser_cluster_shutdown.add_argument('--cluster')
    subparser_cluster_shutdown.add_argument('--host')
    subparser_cluster_shutdown.add_argument('--port')

    # node

    subparser_node = subparsers_main.add_parser('node')
    subparser_node = subparser_node.add_subparsers(title='subcommands',
            description='valid subcommands', help='additional help',
            dest='subparser_node_name')

    # node list

    subparser_node_list = subparser_node.add_parser('list')
    subparser_node_list.add_argument('--cluster')
    subparser_node_list.add_argument('--host')
    subparser_node_list.add_argument('--port')
    subparser_node_list.add_argument('--extended', action='store_true')

    # node status

    subparser_node_status = subparser_node.add_parser('status')
    subparser_node_status.add_argument('subparser_node_status_hostname',
            metavar='hostname')
    subparser_node_status.add_argument('--cluster')
    subparser_node_status.add_argument('--port')
    subparser_node_status.add_argument('--extended', action='store_true')

    # node shutdown

    subparser_node_shutdown = subparser_node.add_parser('shutdown')
    subparser_node_shutdown.add_argument('subparser_node_shutdown_hostname',
            metavar='hostname')
    subparser_node_shutdown.add_argument('--delay', default=None)
    subparser_node_shutdown.add_argument('--port')
    subparser_node_shutdown.add_argument('--cluster')

    # end

    args = parser_main.parse_args()

    try:
        config = configuration(args)
        config.config_setup()
    except ConfigError as error:
        print error
        return 1

    if hasattr(args, 'subparser_index_name'):
        if args.subparser_index_name == 'list':
            index.index_list(config.host(), config.port(), args.extended)
        if args.subparser_index_name == 'create':
            index.index_create(config.host(), config.port(),
                    args.subarser_index_create_indexname, config.shards(),
                    config.replicas())
        if args.subparser_index_name == 'delete':
            index.index_delete(config.host(), config.port(),
                    args.subparser_index_delete_indexname)
        if args.subparser_index_name == 'open':
            index.index_open(config.host(), config.port(),
                    args.subparser_index_open_indexname)
        if args.subparser_index_name == 'close':
            index.index_close(config.host(), config.port(),
                    args.subparser_index_close_indexname)
        if args.subparser_index_name == 'status':
            index.index_status(config.host(), config.port(),
                    args.subparser_index_status_indexname, args.extended)
    elif hasattr(args, 'subparser_cluster_name'):
        if args.subparser_cluster_name == 'status':
            cluster.cluster_status(config.cluster(), config.host(),
                    config.port(), args.extended)
        if args.subparser_cluster_name == 'shutdown':
            cluster.cluster_shutdown(config.cluster(), config.host(),
                    config.port())
    elif hasattr(args, 'subparser_node_name'):
        if args.subparser_node_name == 'shutdown':
            node.node_shutdown(args.subparser_node_shutdown_hostname,
                    config.port(), args.delay)
        if args.subparser_node_name == 'status':
            node.node_status(args.subparser_node_status_hostname,
                    config.port(), args.extended)
        if args.subparser_node_name == 'list':
            node.node_list(config.host(), config.port(), args.extended)


if __name__ == '__main__':
        main()
