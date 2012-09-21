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

import argparse
import os
import types


from daikon import managers
from daikon import config
from daikon import connection
from daikon import exceptions


VERSION = __import__('daikon').__version__


def print_dict(output, level=0):
    for key, value in output.iteritems():
        if isinstance(value, types.DictType):
            print_output(key, level=level)
            print_dict(value, level=level + 1)
        else:
            print_output('%s: %s' % (key, value), level=level)


def print_output(output, vars=None, level=0):
    if isinstance(output, types.ListType):
        output = os.linesep.join(output)
    elif isinstance(output, types.DictType):
        return print_dict(output, level=level)
    if vars is not None:
        output = output % vars
    prefix = ''
    if level > 0:
        prefix = '\t' * level
    print prefix + output


def main():
    parser_main = argparse.ArgumentParser(description='ElasticSearch CLI v%s'
                                          % (VERSION))
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
    subparser_index_status.add_argument('--display', choices=['extended',
            'regular'])

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
    subparser_node_shutdown.add_argument('--delay', default=0)
    subparser_node_shutdown.add_argument('--port')
    subparser_node_shutdown.add_argument('--cluster')

    # end

    args = parser_main.parse_args()

    try:
        conf = config.Configuration(args)
        conf.setup()

        conn = connection.Connection(conf.host(), conf.port())

        if hasattr(args, 'subparser_index_name'):
            action = args.subparser_index_name
            index = managers.Index(conn)

            if action == 'list':
                output = index.list(args.extended)
                print_output('SUCCESS: Listing Indexes')
                print_output(output, level=1)

            if action == 'status':
                index_name = args.subparser_index_status_indexname
                output = index.status(index_name, args.extended)
                print_output(output)

            if action == 'create':
                index_name = args.subparser_index_create_indexname
                shards = conf.shards()
                replicas = conf.replicas()
                output = index.create(index_name, shards, replicas)
                print_output('SUCCESS: Creating Index : "%s"',  output)

            if action == 'delete':
                index_name = args.subparser_index_delete_indexname
                output = index.delete(index_name)
                print_output('SUCCESS: Deleting Index : "%s"', output)

            if action == 'open':
                index_name = args.subparser_index_open_indexname
                output = index.open(index_name)
                print_output('SUCCESS: Opening Index : "%s"', output)

            if action == 'close':
                index_name = args.subparser_index_close_indexname
                output = index.close(index_name)
                print_output('SUCCESS: Closing Index : "%s"', output)

        elif hasattr(args, 'subparser_node_name'):
            node = managers.Node(args)
            if args.subparser_node_name == 'shutdown':
                node.node_shutdown(args.subparser_node_shutdown_hostname,
                        conf.port(), args.delay)
            if args.subparser_node_name == 'status':
                node.node_status(args.subparser_node_status_hostname,
                        conf.port(), args.extended)
            if args.subparser_node_name == 'list':
                node.node_list(config.host(), config.port(), args.extended)

        elif hasattr(args, 'subparser_cluster_name'):
            cluster = managers.Cluster(args)
            if args.subparser_cluster_name == 'status':
                cluster.cluster_status(config.cluster(), config.host(),
                        config.port(), args.extended)
            if args.subparser_cluster_name == 'shutdown':
                cluster.cluster_shutdown(config.cluster(), config.host(),
                        config.port())

    except exceptions.ConfigError as error:
        print error
        return 1
    except (exceptions.ActionIndexError,
            exceptions.ActionNodeError,
            exceptions.ActionClusterError) as error:
        print error
        return 1


if __name__ == '__main__':
        main()
