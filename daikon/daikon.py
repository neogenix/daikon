#!/usr/bin/env python

import argparse
from modules import es_index, es_cluster, es_config, es_node

VERSION = '0.13'


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
    subparser_node_list.add_argument('list')
    subparser_node_list.add_argument('--cluster')
    subparser_node_list.add_argument('--host')
    subparser_node_list.add_argument('--port')
    subparser_node_list.add_argument('--extended')

    # node status

    subparser_node_status = subparser_node.add_parser('status')
    subparser_node_status.add_argument('subparser_node_status_hostname',
            metavar='hostname')
    subparser_node_status.add_argument('--cluster')
    subparser_node_status.add_argument('--port')

    # node shutdown

    subparser_node_shutdown = subparser_node.add_parser('shutdown')
    subparser_node_shutdown.add_argument('subparser_node_shutdown_hostname',
            metavar='hostname')
    subparser_node_shutdown.add_argument('--delay', default=None)
    subparser_node_shutdown.add_argument('--port')
    subparser_node_shutdown.add_argument('--cluster')

    # end

    es_args = parser_main.parse_args()
    es_config.configuration(es_args)

    if hasattr(es_args, 'subparser_index_name'):
        if es_args.subparser_index_name == 'list':
            es_index.index_list(es_config.config['host'],
                    es_config.config['port'], es_args.extended)
        if es_args.subparser_index_name == 'create':
            es_index.index_create(es_config.config['host'],
                    es_config.config['port'],
                    es_args.subarser_index_create_indexname,
                    es_config.config['shards'], es_config.config['replicas'])
        if es_args.subparser_index_name == 'delete':
            es_index.index_delete(es_config.config['host'],
                    es_config.config['port'],
                    es_args.subparser_index_delete_indexname)
        if es_args.subparser_index_name == 'open':
            es_index.index_open(es_config.config['host'],
                    es_config.config['port'],
                    es_args.subparser_index_open_indexname)
        if es_args.subparser_index_name == 'close':
            es_index.index_close(es_config.config['host'],
                    es_config.config['port'],
                    es_args.subparser_index_close_indexname)
        if es_args.subparser_index_name == 'status':
            es_index.index_status(es_config.config['host'],
                    es_config.config['port'],
                    es_args.subparser_index_status_indexname, es_args.extended)
    elif hasattr(es_args, 'subparser_cluster_name'):
        if es_args.subparser_cluster_name == 'status':
            es_cluster.cluster_status(es_config.config['cluster'],
                    es_config.config['host'], es_config.config['port'],
                    es_args.extended)
        if es_args.subparser_cluster_name == 'shutdown':
            es_cluster.cluster_shutdown(es_config.config['cluster'],
                    es_config.config['host'], es_config.config['port'])
    elif hasattr(es_args, 'subparser_node_name'):
        if es_args.subparser_node_name == 'shutdown':
            es_node.node_shutdown(es_args.subparser_node_shutdown_hostname,
                    es_config.config['port'], es_args.delay)
        if es_args.subparser_node_name == 'list':
            es_node.node_list(es_config.config['host'],
                    es_config.config['port'], es_args.extended)


if __name__ == '__main__':
    main()
