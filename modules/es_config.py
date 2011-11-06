import ConfigParser
import sys
import os.path

config = {}


def configuration(arguments):
    global config
    cparser = ConfigParser.ConfigParser()

    if hasattr(arguments, "cluster") and arguments.cluster is not None:
        config["cluster"] = arguments.cluster
    else:
        config["cluster"] = 'default'

    if not cparser.read(['/etc/daikon/daikon.conf',
                os.path.expanduser('~/.daikon.conf'), 'daikon.conf']):
        sys.stderr.write("ERROR: No cparser file found!\n")
        sys.exit(1)

    if not cparser.has_section(config["cluster"]):
        sys.stderr.write("ERROR: No cluster section defined for this cluster!\n")
        sys.exit(1)

    # Host Config Setup

    if not cparser.get(config["cluster"], 'host'):
        sys.stderr.write("ERROR: No default host defined!\n")
        sys.exit(1)
    elif hasattr(arguments, 'host') and arguments.host:
        config["host"] = arguments.host
    else:
        config["host"] = cparser.get(config["cluster"], 'host')

    # Port Config Setup

    if not cparser.get(config["cluster"], 'port'):
        sys.stderr.write("ERROR: No default port defined!\n")
        sys.exit(1)
    elif hasattr(arguments, 'port') and arguments.port:
        config["port"] = arguments.port
    else:
        config["port"] = cparser.get(config["cluster"], 'port')

    # Replicas Config Setup

    if not cparser.get(config["cluster"], 'replicas'):
        sys.stderr.write("ERROR: No default replicas defined!\n")
        sys.exit(1)
    elif hasattr(arguments, 'replicas') and arguments.replicas:
        config["replicas"] = arguments.replicas
    else:
        config["replicas"] = cparser.get(config["cluster"], 'replicas')

    # Replicas Config Setup

    if not cparser.get(config["cluster"], 'shards'):
        sys.stderr.write("ERROR: No default shards defined!\n")
        sys.exit(1)
    elif hasattr(arguments, 'shards') and arguments.shards:
        config["shards"] = arguments.shards
    else:
        config["shards"] = cparser.get(config["cluster"], 'shards')
