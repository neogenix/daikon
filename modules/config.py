import ConfigParser
import sys
import os.path


def configuration(cluster):
    config = ConfigParser.ConfigParser()

    if cluster is None:
        cluster = 'default'

    if not config.read(['/etc/daikon/daikon.conf',
                os.path.expanduser('~/.daikon.conf'), 'daikon.conf']):
        sys.stderr.write("No config file found!\n")
        sys.exit(1)

    if not config.has_section(cluster):
        sys.stderr.write("No cluster section defined for this cluster!\n")
        sys.exit(1)

    host = config.get(cluster, 'host')
    if not host:
        sys.stderr.write("No default host defined!\n")
        sys.exit(1)

    port = config.get(cluster, 'port')
    if not port:
        sys.stderr.write("No default port defined!\n")
        sys.exit(1)

    replicas = config.get(cluster, 'replicas')
    if not replicas:
        sys.stderr.write("No default replicas defined!\n")
        sys.exit(1)

    shards = config.get(cluster, 'shards')
    if not shards:
        sys.stderr.write("No default shards defined!\n")
        sys.exit(1)
