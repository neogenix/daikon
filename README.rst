Daikon
======

Description
-----------

Daikon is a CLI for ElasticSearch to make some of the basic admin tasks associated
with ElasticSearch a little easier than using curl... you know for us lazy folks.

It's written in Python, and requires python 2.7.x, anyjson, and Python-Requests.

Why 'daikon'. Well, 'daikon' is a radish that is used in the making of kimchi.
For those who know ES, you'll know what that means ;) and of course HUGE shout
out to @kimchy

Installing
----------

This should work : ::

    $ pip install daikon

And even this should too, but you shouldn't use it... : ::

    $ easy_install daikon

Configuration
-------------

Configuration is defined in /etc/daikon/daikon.conf, or ~/.daikon.conf, and has
the format : ::

    [default]
    host = localhost
    port = 9200
    replicas = 3
    shards = 2

Current Functionality
---------------------

Commands : ::

    * Working with Indexes
        * Create Indexes
            examples:
                daikon index create <indexname>
                daikon index create --replicas <replicas> --shards <shards> <indexname>
                daikon index create --cluster <clustername> --host <host> --port <port> <indexname>
        * Delete Indexes
            examples:
                daikon index delete <indexname>
                daikon index delete --cluster <clustername> --host <host> --port <port> <indexname>
        * List Indexes
            examples:
                daikon index list <indexname>
                daikon index list --extended <indexname>
                daikon index list --cluster <clustername> --host <host> --port <port> <indexname>
        * Open Indexes
            examples:
                daikon index open <indexname>
                daikon index open --cluster <clustername> --host <host> --port <port> <indexname>
        * Close Indexes
            examples:
                daikon index close <indexname>
                daikon index close --cluster <clustername> --host <host> --port <port> <indexname>
        * Status Indexes
            examples:
                daikon index status <indexname>
                daikon index status --extended <indexname>
                daikon index status --cluster <clustername> --host <host> --port <port> <indexname>
    * Working with Clusters
        * Status View
            examples:
                daikon cluster status
                daikon cluster status --extended
                daikon cluster status --cluster <clustername> --host <host> --port <port>
        * Shutdown Clusters
            examples:
                daikon cluster shutdown
                daikon cluster shutdown --cluster <clustername> --host <host> --port <port>
    * Working with Nodes
        * List
            examples:
                daikon node list
                daikon node list --extended
                daikon node list --cluster <clustername> --host <host> --port <port>
        * Status
            examples:
                daikon node status <nodename>
                daikon node status --extended <nodename>
                daikon node status --cluster <clustername> --host <host> --port <port> <nodename>
        * Shutdown
            examples:
                daikon node shutdown <nodename>
                daikon node shutdown --delay <delayseconds> <nodename>
                daikon node shutdown --cluster <clustername> --port <port> <nodename>


Planned Functionality
---------------------

Future Planned Functionality : ::

    * Working with Rivers (and provide plugin supports for rivers)
    * Working with indexes to dump, and import
    * Working with cluster maintennace
    * Working with searches, exporting results
    * Enhance Logging (Syslog, Debug Logging, Log File)
