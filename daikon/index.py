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

from exceptions import ActionIndexError


def index_create(host, port, indexname, shards, replicas):
    try:
        res_data = json.dumps('{"settings" : { "number_of_shards" : %s, \
                "number_of_replicas" : %s } }') % (shards, replicas)
        res_url = 'http://%s:%s/%s' % (host, port, indexname)
        res = requests.post(res_url, data=res_data)
        res.raise_for_status()
        print 'SUCCESS: Creating Index : "%s"' % (indexname)
    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionIndexError('Error Creating Index - %s' % (e))


def index_delete(host, port, indexname):
    try:
        res_url = 'http://%s:%s/%s' % (host, port, indexname)
        res = requests.delete(res_url)
        res.raise_for_status()
        print 'SUCCESS: Deleting Index : "%s"' % (indexname)
    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionIndexError('Error Deleting Index - %s' % (e))


def index_list(host, port, extended):
    try:
        res_health_url = 'http://%s:%s/_cluster/health?level=indices' % \
                (host, port)
        res_health = requests.get(res_health_url)
        res_health.raise_for_status()

        res_state_url = 'http://%s:%s/_cluster/state' % (host, port)
        res_state = requests.get(res_state_url)
        res_state.raise_for_status()

        result_state = json.loads(res_state.content)[u'metadata'][u'indices']
        result_health = json.loads(res_health.content)[u'indices']
        print 'SUCCESS: Listing Indexes'
        for index in result_state:
            print '\t Name: %s' % (index)
            if extended:
                print '\t\t State: %s' % (result_state[index][u'state'])
                if result_state[index][u'state'] == 'close':
                    print '\t\t Status: CLOSED'
                else:
                    print '\t\t Status: %s' % \
                            (result_health[index][u'status'])
                print '\t\t Number Of Shards: %s' % \
                        (result_state[index][u'settings'][u'index.number_of_shards'])
                print '\t\t Number Of Replicas: %s' % \
                        (result_state[index][u'settings'][u'index.number_of_replicas'])

    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionIndexError('Error Listing Indexes - %s' % (e))


def index_open(host, port, indexname):
    try:
        res_url = 'http://%s:%s/%s/_open' % (host, port, indexname)
        res = requests.post(res_url)
        res.raise_for_status()
        print 'SUCCESS: Opening Index : "%s"' % (indexname)
    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionIndexError('Error Opening Index - %s' % (e))


def index_close(host, port, indexname):
    try:
        res_url = 'http://%s:%s/%s/_close' % (host, port, indexname)
        res = requests.post(res_url)
        res.raise_for_status()
        print 'SUCCESS: Closing Index : "%s"' % (indexname)
    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionIndexError('Error Closing Index - %s' % (e))


def index_status(host, port, indexname, extended, display):
    try:
        res_url = 'http://%s:%s/%s/_status' % (host, port, indexname)
        res = requests.get(res_url)
        res.raise_for_status()
        print 'SUCCESS: Fetching Index Status : "%s"' % (indexname)
        result = json.loads(res.content)[u'indices'][indexname]

        if extended:
            display = 'extended'

        var = {}
        if display == 'extended':
            content = ('\t Size Status:\n'
                       '\t\t Primary Size: %(s_pri)s\n'
                       '\t\t Total Size: %(s_total)s\n'
                       '\t Document Status:\n'
                       '\t\t Number Of Docs (Current): %(d_cur)s\n'
                       '\t\t Number Of Docs (Max): %(d_max)s\n'
                       '\t\t Number Of Docs (Deleted): %(d_del)s\n'
                       '\t Merge Status:\n'
                       '\t\t Total Merges: %(m_total)s\n'
                       '\t\t Current Merges: %(m_cur)s\n')

            var['s_pri'] = result[u'index'][u'primary_size']
            var['s_total'] = result[u'index'][u'size']
            var['d_cur'] = result[u'docs'][u'num_docs']
            var['d_max'] = result[u'docs'][u'max_doc']
            var['d_del'] = result[u'docs'][u'deleted_docs']
            var['m_total'] = result[u'merges'][u'total']
            var['m_cur'] = result[u'merges'][u'current']
            print content % var

            s_content = ('\t Shard Status:\n'
                         '\t\t Number: %(number)s\n'
                         '\t\t\t State: %(state)s\n'
                         '\t\t\t Size: %(size)s\n'
                         '\t\t\t Number Of Docs (Current): %(d_cur)s\n'
                         '\t\t\t Number Of Docs (Max): %(d_max)s\n'
                         '\t\t\t Number Of Docs (Deleted): %(d_del)s\n')

            for s in result[u'shards']:
                s_data = result[u'shards'][s][0]
                var[s] = {}
                var[s]['number'] = s
                var[s]['state'] = s_data[u'routing'][u'state']
                var[s]['size'] = s_data[u'index'][u'size']
                var[s]['d_cur'] = s_data[u'docs'][u'num_docs']
                var[s]['d_max'] = s_data[u'docs'][u'max_doc']
                var[s]['d_del'] = s_data[u'docs'][u'deleted_docs']
                print s_content % var[s]

        else:
            content = ('\t Size Status:\n'
                       '\t\t Primary Size: %(s_pri)s\n'
                       '\t Document Status:\n'
                       '\t\t Number Of Docs (Current): %(d_cur)s\n'
                       '\t Merge Status:\n'
                       '\t\t Total Merges: %(m_total)s\n')

            var['s_pri'] = result[u'index'][u'primary_size']
            var['d_cur'] = result[u'docs'][u'num_docs']
            var['m_total'] = result[u'merges'][u'total']
            print content % var

    except (requests.RequestException, urllib2.HTTPError), e:
        raise ActionIndexError('Error Fetching Index Status - %s' % (e))
