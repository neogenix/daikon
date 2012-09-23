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

import sys
import logging
from time import time

from daikon import display
from daikon import managers
from daikon import config
from daikon import connection
from daikon import exceptions
from daikon import parser

# ---------------------
# Variables
# ---------------------

VERSION = '1.50'

# ---------------------
# Logging
# ---------------------

log_format = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
log_stream = logging.StreamHandler()
log_stream.setLevel(logging.INFO)
log_stream.setFormatter(log_format)
log_stream.addFilter('daikon')

log = logging.getLogger('daikon')
log.addHandler(log_stream)

stime = time()


# ---------------------
# Main
# ---------------------

def main():
    try:
        d = display.Display()

        p = parser.Parser(VERSION)
        p.setup()
        args = p.get_results()

        conf = config.Config(args)
        conf.setup()

        conn = connection.Connection(conf.host(), conf.port())

        if hasattr(args, 'index_name'):
            action = args.index_name
            index = managers.Index(conn)

            if action == 'list':
                output = index.list(args.extended)
                d.print_output('SUCCESS: Listing Indexes')
                d.print_output(output, level=1)

            if action == 'status':
                index_name = args.index_status_indexname
                output = index.status(index_name, args.extended)
                d.print_output(output)

            if action == 'create':
                index_name = args.index_create_indexname
                shards = conf.shards()
                replicas = conf.replicas()
                output = index.create(index_name, shards, replicas)
                d.print_output('SUCCESS: Creating Index : "%s"',  output)

            if action == 'delete':
                index_name = args.index_delete_indexname
                output = index.delete(index_name)
                d.print_output('SUCCESS: Deleting Index : "%s"', output)

            if action == 'open':
                index_name = args.index_open_indexname
                output = index.open(index_name)
                d.print_output('SUCCESS: Opening Index : "%s"', output)

            if action == 'close':
                index_name = args.index_close_indexname
                output = index.close(index_name)
                d.print_output('SUCCESS: Closing Index : "%s"', output)

        elif hasattr(args, 'node_name'):
            node = managers.Node(args, d)
            if args.node_name == 'shutdown':
                node.node_shutdown(args.node_shutdown_hostname,
                        conf.port(), args.delay)
            if args.node_name == 'status':
                node.node_status(args.node_status_hostname,
                        conf.port(), args.extended)
            if args.node_name == 'list':
                node.node_list(conf.host(), conf.port(), args.extended)

        elif hasattr(args, 'cluster_name'):
            cluster = managers.Cluster(args, d)
            if args.cluster_name == 'status':
                cluster.cluster_status(conf.cluster(), conf.host(),
                        conf.port(), args.extended)
            if args.cluster_name == 'shutdown':
                cluster.cluster_shutdown(conf.cluster(), conf.host(),
                        conf.port())

        total_time = round(float(time() - stime), 3)
        d.print_output('Execution Time: "%s" seconds', total_time)
    except exceptions.ConfigError as error:
        print error
        return 1
    except (exceptions.ActionIndexError,
            exceptions.ActionNodeError,
            exceptions.ActionClusterError) as error:
        print error
        return 1
    finally:
        sys.exit()


if __name__ == '__main__':
        main()
