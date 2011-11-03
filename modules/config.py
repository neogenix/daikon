import ConfigParser
import sys
import os.path

config = ConfigParser.ConfigParser()

if not config.read(['/etc/daikon/daikon.conf',
        os.path.expanduser('~/.daikon.conf'), 'daikon.conf']):
    sys.stderr.write("No config file found!\n")
    sys.exit(1)

if not config.has_section("default"):
    sys.stderr.write("No default config section defined!\n")
    sys.exit(1)

host = config.get('default', 'host')
if not host:
    sys.stderr.write("No default host defined!\n")
    sys.exit(1)

port = config.get('default', 'port')
if not port:
    sys.stderr.write("No default port defined!\n")
    sys.exit(1)

replicas = config.get('default', 'replicas')
if not replicas:
    sys.stderr.write("No default replicas defined!\n")
    sys.exit(1)

shards = config.get('default', 'shards')
if not shards:
    sys.stderr.write("No default shards defined!\n")
    sys.exit(1)
