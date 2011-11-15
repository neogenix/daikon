
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
        request.raise_for_status()
        print 'SUCCESS: Deleting Index : "%s"' % (indexname)
    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionIndexError('Error Deleting Index - %s' % (e))


def index_list(host, port, extended):
    try:
        request_health_url = 'http://%s:%s/_cluster/health?level=indices' % \
                (host, port)
        request_health = requests.get(request_health_url)
        request_health.raise_for_status()

        request_state_url = 'http://%s:%s/_cluster/state' % (host, port)
        request_state = requests.get(request_state_url)
        request_state.raise_for_status()

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

    except (request_health.RequestException, request_state.RequestException, \
            urllib2.HTTPError), e:
        raise ActionIndexError('Error Listing Indexes - %s' % (e))


def index_open(host, port, indexname):
    try:
        request_url = 'http://%s:%s/%s/_open' % (host, port, indexname)
        request = requests.post(request_url)
        request.raise_for_status()
        print 'SUCCESS: Opening Index : "%s"' % (indexname)
    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionIndexError('Error Opening Index - %s' % (e))


def index_close(host, port, indexname):
    try:
        request_url = 'http://%s:%s/%s/_close' % (host, port, indexname)
        request = requests.post(request_url)
        request.raise_for_status()
        print 'SUCCESS: Closing Index : "%s"' % (indexname)
    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionIndexError('Error Closing Index - %s' % (e))


def index_status(host, port, indexname, extended):
    try:
        request_url = 'http://%s:%s/%s/_status' % (host, port, indexname)
        request = requests.get(request_url)
        request.raise_for_status()
        print 'SUCCESS: Fetching Index Status : "%s"' % (indexname)

        request_result = json.loads(request.content)[u'indices'][indexname]
        print '\t Size Status:'
        print '\t\t Primary Size: %s' % \
                (request_result[u'index'][u'primary_size'])
        if extended:
            print '\t\t Total Size: %s' % \
                (request_result[u'index'][u'size'])

        print '\t Document Status:'
        print '\t\t Number Of Docs (Current): %s' % \
            (request_result[u'docs'][u'num_docs'])
        if extended:
            print '\t\t Number Of Docs (Max): %s' % \
                    (request_result[u'docs'][u'max_doc'])
            print '\t\t Number Of Docs (Deleted): %s' % \
                    (request_result[u'docs'][u'deleted_docs'])

        print '\t Merge Status:'
        print '\t\t Total Merges: %s' % (request_result[u'merges'][u'total'])
        if extended:
            print '\t\t Current Merges: %s' % \
                    (request_result[u'merges'][u'current'])
        if extended:
            print '\n\t Shard Status:'
            for shard in request_result[u'shards']:
                print '\n\t\t Number: %s' % (shard)

                shard_data = request_result[u'shards'][shard][0]
                print '\t\t\t State: %s' % (shard_data[u'routing'][u'state'])
                print '\t\t\t Size: %s' % (shard_data[u'index'][u'size'])
                print '\t\t\t Number Of Docs (Current): %s' % \
                        (shard_data[u'docs'][u'num_docs'])
                print '\t\t\t Number Of Docs (Max): %s' % \
                        (shard_data[u'docs'][u'max_doc'])
                print '\t\t\t Number Of Docs (Deleted): %s' % \
                        (shard_data[u'docs'][u'deleted_docs'])
    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionIndexError('Error Fetching Index Status - %s' % (e))
