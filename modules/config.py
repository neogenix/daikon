import ConfigParser
import sys
import os.path

config = ConfigParser.ConfigParser()
config_files = config.read(['/etc/daikon/daikon.conf',
               os.path.expanduser('~/.daikon.conf'),
               'daikon.conf'])

if not config_files:
    sys.stderr.write("No config file found!\n")
    sys.exit(1)

if not config.has_section("default"):
    sys.stderr.write("No default config section defined!\n")
    sys.exit(1)

host = config.get('default', 'host')
port = config.get('default', 'port')
replicas = config.get('default', 'replicas')
shards = config.get('default', 'shards')
