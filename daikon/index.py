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


class Index:

    def __init__(self, arguments):
        self.arguments = arguments
        self._state = None
        self._health = None

    def index_setup(self, host, port):
        ''' Setup Health and Status info fetches '''

        try:
            if self._health is None:
                h_url = 'http://%s:%s/_cluster/health?level=indices' \
                        % (host, port)
                h = requests.get(h_url)
                h.raise_for_status()
                self._health = json.loads(h.content)[u'indices']

            if self._state is None:
                s_url = 'http://%s:%s/_cluster/state' % (host, port)
                s = requests.get(s_url)
                s.raise_for_status()
                self._state = json.loads(s.content)[u'metadata'][u'indices']

        except (requests.RequestException, urllib2.HTTPError), e:
            raise ActionIndexError('Error Setting Up Indexes - %s' % (e))

    def index_create(self, host, port, indexname, shards, replicas):
        ''' Creat Indexes Here '''

        try:
            res_data = json.dumps('{"settings" : { "number_of_shards" : %s, \
                    "number_of_replicas" : %s } }') % (shards, replicas)
            res_url = 'http://%s:%s/%s' % (host, port, indexname)
            res = requests.post(res_url, data=res_data)
            res.raise_for_status()
            print 'SUCCESS: Creating Index : "%s"' % (indexname)

        except (requests.RequestException, urllib2.HTTPError), e:
            raise ActionIndexError('Error Creating Index - %s' % (e))

    def index_delete(self, host, port, indexname):
        ''' Delete Indexes Here '''

        try:
            res_url = 'http://%s:%s/%s' % (host, port, indexname)
            res = requests.delete(res_url)
            res.raise_for_status()
            print 'SUCCESS: Deleting Index : "%s"' % (indexname)

        except (requests.RequestException, urllib2.HTTPError), e:
            raise ActionIndexError('Error Deleting Index - %s' % (e))

    def index_open(self, host, port, indexname):
        ''' Open Indexes Here '''

        try:
            res_url = 'http://%s:%s/%s/_open' % (host, port, indexname)
            res = requests.post(res_url)
            res.raise_for_status()
            print 'SUCCESS: Opening Index : "%s"' % (indexname)

        except (requests.RequestException, urllib2.HTTPError), e:
            raise ActionIndexError('Error Opening Index - %s' % (e))

    def index_close(self, host, port, indexname):
        ''' Close Indexes Here '''
        try:
            res_url = 'http://%s:%s/%s/_close' % (host, port, indexname)
            res = requests.post(res_url)
            res.raise_for_status()
            print 'SUCCESS: Closing Index : "%s"' % (indexname)

        except (requests.RequestException, urllib2.HTTPError), e:
            raise ActionIndexError('Error Closing Index - %s' % (e))

    def index_status(self, host, port, indexname, extended):
        ''' Fetch Info and Status For an Index Here '''

        try:
            req_url = 'http://%s:%s/%s/_status' % (host, port, indexname)
            req = requests.get(req_url)
            req.raise_for_status()
            res = json.loads(req.content)[u'indices'][indexname]
            var = {}

            if extended:
                content = ('Name: %(name)s\n'
                           '\t Size Status:\n'
                           '\t\t Primary Size: %(s_pri)s\n'
                           '\t\t Total Size: %(s_total)s\n'
                           '\t Document Status:\n'
                           '\t\t Number Of Docs (Current): %(d_cur)s\n'
                           '\t\t Number Of Docs (Max): %(d_max)s\n'
                           '\t\t Number Of Docs (Deleted): %(d_del)s\n'
                           '\t Merge Status:\n'
                           '\t\t Total Merges: %(m_total)s\n'
                           '\t\t Current Merges: %(m_cur)s\n')
                var['name'] = indexname
                var['s_pri'] = res[u'index'][u'primary_size']
                var['s_total'] = res[u'index'][u'size']
                var['d_cur'] = res[u'docs'][u'num_docs']
                var['d_max'] = res[u'docs'][u'max_doc']
                var['d_del'] = res[u'docs'][u'deleted_docs']
                var['m_total'] = res[u'merges'][u'total']
                var['m_cur'] = res[u'merges'][u'current']
                print content % var
                s_content = ('\t Shard Status:\n'
                             '\t\t Number: %(number)s\n'
                             '\t\t\t State: %(state)s\n'
                             '\t\t\t Size: %(size)s\n'
                             '\t\t\t Number Of Docs (Current): %(d_cur)s\n'
                             '\t\t\t Number Of Docs (Max): %(d_max)s\n'
                             '\t\t\t Number Of Docs (Deleted): %(d_del)s')

                for s in res[u'shards']:
                    s_data = res[u'shards'][s][0]
                    var[s] = {}
                    var[s]['number'] = s
                    var[s]['state'] = s_data[u'routing'][u'state']
                    var[s]['size'] = s_data[u'index'][u'size']
                    var[s]['d_cur'] = s_data[u'docs'][u'num_docs']
                    var[s]['d_max'] = s_data[u'docs'][u'max_doc']
                    var[s]['d_del'] = s_data[u'docs'][u'deleted_docs']
                    print s_content % var[s]

            else:
                content = ('Name: %(name)s\n'
                           '\t Size Status:\n'
                           '\t\t Primary Size: %(s_pri)s\n'
                           '\t Document Status:\n'
                           '\t\t Number Of Docs (Current): %(d_cur)s\n'
                           '\t Merge Status:\n'
                           '\t\t Total Merges: %(m_total)s')
                var['name'] = indexname
                var['s_pri'] = res[u'index'][u'primary_size']
                var['d_cur'] = res[u'docs'][u'num_docs']
                var['m_total'] = res[u'merges'][u'total']
                print content % var

        except (requests.RequestException, urllib2.HTTPError), e:
            raise ActionIndexError('Error Fetching Index Status - %s' % (e))

    def index_list(self, host, port, extended):
        ''' List Indexes '''

        try:
            print 'SUCCESS: Listing Indexes'
            for index in self._state:
                print '\t Name: %s' % (index)

                if extended:
                    var = {}

                    if self._state[index][u'state'] == 'close':
                        status = 'closed'
                    else:
                        status = self._health[index][u'status']

                    var['state'] = self._state[index][u'state']
                    var['status'] = status
                    settings = self._state[index][u'settings']
                    var['shards'] = settings[u'index.number_of_shards']
                    var['replicas'] = settings[u'index.number_of_replicas']
                    content = ('\t\t State: %(state)s\n'
                               '\t\t Status: %(status)s\n'
                               '\t\t Number Of Shards: %(shards)s\n'
                               '\t\t Number Of Replicas: %(replicas)s')
                    print content % var

        except (requests.RequestException, urllib2.HTTPError), e:
            raise ActionIndexError('Error Listing Indexes - %s' % (e))
