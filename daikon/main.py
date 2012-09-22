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

import os
import types
from pprint import pprint

from daikon import managers
from daikon import config
from daikon import connection
from daikon import exceptions
from daikon import parser

VERSION = '1.10'


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
    try:
        parse = parser.Parser(VERSION)
        parse.setup()
        args = parse.get_results()

        conf = config.Config(args)
        conf.setup()

        conn = connection.Connection(conf.host(), conf.port())

        if hasattr(args, 'index_name'):
            action = args.index_name
            index = managers.Index(conn)

            if action == 'list':
                output = index.list(args.extended)
                print_output('SUCCESS: Listing Indexes')
                print_output(output, level=1)

            if action == 'status':
                index_name = args.index_status_indexname
                output = index.status(index_name, args.extended)
                print_output(output)

            if action == 'create':
                index_name = args.index_create_indexname
                shards = conf.shards()
                replicas = conf.replicas()
                output = index.create(index_name, shards, replicas)
                print_output('SUCCESS: Creating Index : "%s"',  output)

            if action == 'delete':
                index_name = args.index_delete_indexname
                output = index.delete(index_name)
                print_output('SUCCESS: Deleting Index : "%s"', output)

            if action == 'open':
                index_name = args.index_open_indexname
                output = index.open(index_name)
                print_output('SUCCESS: Opening Index : "%s"', output)

            if action == 'close':
                index_name = args.index_close_indexname
                output = index.close(index_name)
                print_output('SUCCESS: Closing Index : "%s"', output)

        elif hasattr(args, 'node_name'):
            node = managers.Node(args)
            if args.node_name == 'shutdown':
                node.node_shutdown(args.node_shutdown_hostname,
                        conf.port(), args.delay)
            if args.node_name == 'status':
                node.node_status(args.node_status_hostname,
                        conf.port(), args.extended)
            if args.node_name == 'list':
                node.node_list(conf.host(), conf.port(), args.extended)

        elif hasattr(args, 'cluster_name'):
            cluster = managers.Cluster(args)
            if args.cluster_name == 'status':
                cluster.cluster_status(conf.cluster(), conf.host(),
                        conf.port(), args.extended)
            if args.cluster_name == 'shutdown':
                cluster.cluster_shutdown(conf.cluster(), conf.host(),
                        conf.port())

        pprint(vars(args))
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
