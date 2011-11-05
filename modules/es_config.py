import ConfigParser
import sys
import os.path

config = {}

def configuration(cluster):
    global config
    cparser = ConfigParser.ConfigParser()

    if cluster is None:
        config["cluster"] = 'default'

    if not cparser.read(['/etc/daikon/daikon.conf',
                os.path.expanduser('~/.daikon.conf'), 'daikon.conf']):
        sys.stderr.write("No cparser file found!\n")
        sys.exit(1)

    if not cparser.has_section(config["cluster"]):
        sys.stderr.write("No cluster section defined for this cluster!\n")
        sys.exit(1)

    config["host"] = cparser.get(cluster, 'host')
    if not config["host"]:
        sys.stderr.write("No default host defined!\n")
        sys.exit(1)

    config["port"] = cparser.get(cluster, 'port')
    if not config["port"]:
        sys.stderr.write("No default port defined!\n")
        sys.exit(1)

    config["replicas"] = cparser.get(cluster, 'replicas')
    if not config["replicas"]:
        sys.stderr.write("No default replicas defined!\n")
        sys.exit(1)

    config["shards"] = cparser.get(cluster, 'shards')
    if not config["shards"]:
        sys.stderr.write("No default shards defined!\n")
        sys.exit(1)
