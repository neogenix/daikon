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

import requests
import anyjson as json
import urllib2
import sys

from exceptions import ActionIndexError


def index_create(host, port, indexname, shards, replicas):
    try:
        request_data = json.dumps('{"settings" : { "number_of_shards" : %s, \
                "number_of_replicas" : %s } }') % (shards, replicas)
        request_url = 'http://%s:%s/%s' % (host, port, indexname)
        request = requests.post(request_url, data=request_data)
        request.raise_for_status()
        print 'SUCCESS: Creating Index : "%s"' % (indexname)
    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionIndexError('Error Creating Index - %s' % (e))


def index_delete(host, port, indexname):
    try:
        request_url = 'http://%s:%s/%s' % (host, port, indexname)
        request = requests.delete(request_url)

        if request.error is not None:
            print 'ERROR: Deleteing Index : "%s" - %s' % (indexname,
                    request.error)
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Deleting Index : "%s" - %s' % (indexname,  e)
        sys.exit(1)
    else:
        print 'SUCCESS: Deleting Index : "%s" - %s' % (indexname)


def index_list(host, port, extended):
    try:
        request_health_url = 'http://%s:%s/_cluster/health?level=indices' % \
                (host, port)
        request_health = requests.get(request_health_url)
        if request_health.error is not None:
            print 'ERROR: Listing Indexes : %s' % (request_health.error)
            sys.exit(1)
        else:
            request_health.raise_for_status()

        request_state_url = 'http://%s:%s/_cluster/state' % (host, port)
        request_state = requests.get(request_state_url)
        if request_state.error is not None:
            print 'ERROR: Listing Indexes : %s' % (request_state.error)
            sys.exit(1)
        else:
            request_state.raise_for_status()

    except request_health.RequestException, e:
        print 'ERROR:  Listing Indexes - %s' % (e)
        sys.exit(1)
    except request_state.RequestException, e:
        print 'ERROR:  Listing Indexes - %s' % (e)
        sys.exit(1)
    else:
        data_result_state = json.loads(request_state.content)[u'metadata'][u'indices']
        data_result_health = json.loads(request_health.content)[u'indices']
        print 'SUCCESS: Listing Indexes'
        for index in data_result_state:
            print '\t Name: %s' % (index)
            if extended:
                print '\t\t State: %s' % (data_result_state[index][u'state'])
                if data_result_state[index][u'state'] == 'close':
                    print '\t\t Status: CLOSED'
                else:
                    print '\t\t Status: %s' % \
                            (data_result_health[index][u'status'])
                print '\t\t Number Of Shards: %s' % \
                        (data_result_state[index][u'settings'][u'index.number_of_shards'])
                print '\t\t Number Of Replicas: %s' % \
                        (data_result_state[index][u'settings'][u'index.number_of_replicas'])


def index_open(host, port, indexname):
    try:
        request_url = 'http://%s:%s/%s/_open' % (host, port, indexname)
        request = requests.post(request_url)
        if request.error is not None:
            print 'ERROR: Opening Index : "%s" - %s' % \
                (indexname, request.error)
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Opening Index : "%s" - %s' % (indexname, e)
        sys.exit(1)
    else:
        print 'SUCCESS: Opening Index : "%s"' % (indexname)


def index_close(host, port, indexname):
    try:
        request_url = 'http://%s:%s/%s/_close' % (host, port, indexname)
        request = requests.post(request_url)
        if request.error is not None:
            print 'ERROR: Closing Index : "%s" - %s' % (indexname, \
                    request.error)
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Closing Index : "%s" - %s' % (indexname, e)
        sys.exit(1)
    else:
        print 'SUCCESS: Closing Index : "%s"' % (indexname)


def index_status(host, port, indexname, extended):
    try:
        request = requests.get('http://' + host + ':' + port + '/' +
                indexname + '/_status')
        if request.error is not None:
            print 'ERROR: Fetching Index Status : "%s" - %s' % (indexname, \
                    request.error)
            sys.exit(1)
        else:
            request.raise_for_status()
    except requests.RequestException, e:
        print 'ERROR: Fetching Index Status : "%s" - %s' % (indexname, e)
        sys.exit(1)
    else:
        print 'SUCCESS: Fetching Index Status : "%s"' % (indexname)
        data_result = json.loads(request.content)

        print '\t Size Status:'
        print '\t\t Primary Size: %s' % \
                (data_result[u'indices'][indexname][u'index'][u'primary_size'])
        if extended:
            print '\t\t Total Size: %s' % \
                (data_result[u'indices'][indexname][u'index'][u'size'])

        print '\t Document Status:'
        print '\t\t Number Of Docs (Current): %s' % \
            (data_result[u'indices'][indexname][u'docs'][u'num_docs'])
        if extended:
            print '\t\t Number Of Docs (Max): %s' % \
                    (data_result[u'indices'][indexname][u'docs'][u'max_doc'])
            print '\t\t Number Of Docs (Deleted): %s' % \
                    (data_result[u'indices'][indexname][u'docs'][u'deleted_docs'])

        print '\t Merge Status:'
        print '\t\t Total Merges: %s' % \
                (data_result[u'indices'][indexname][u'merges'][u'total'])
        if extended:
            print '\t\t Current Merges: %s' % \
                    (data_result[u'indices'][indexname][u'merges'][u'current'])

        if extended:
            print '\n\t Shard Status:'
            for shard in data_result[u'indices'][indexname][u'shards']:
                print '\n\t\t Number: %s' % (shard)

                data_shard = data_result[u'indices'][indexname][u'shards'][shard][0]
                print '\t\t\t State: %s' % (data_shard[u'routing'][u'state'])
                print '\t\t\t Size: %s' % (data_shard[u'index'][u'size'])
                print '\t\t\t Number Of Docs (Current): %s' % \
                        (data_shard[u'docs'][u'num_docs'])
                print '\t\t\t Number Of Docs (Max): %s' % \
                        (data_shard[u'docs'][u'max_doc'])
                print '\t\t\t Number Of Docs (Deleted): %s' % \
                        (data_shard[u'docs'][u'deleted_docs'])
