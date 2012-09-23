# -*- coding: utf-8 -*-
#
#   Copyright [2011] [Patrick Ancillotti]
#   Copyright [2011] [Jason Kölker]
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

# ---------------------
# Imports
# ---------------------

import logging
import requests
import anyjson as json
import urllib2

from daikon import exceptions

# ---------------------
# Logging
# ---------------------

log = logging.getLogger('daikon')


# ---------------------
# Classes
# ---------------------

class Index(object):
    def __init__(self, connection):
        self._connection = connection

    def create(self, index_name, shards, replicas):
        try:
            data = {"settings": {"number_of_shards": shards,
                                 "number_of_replicas": replicas}}
            self._connection.post(index_name, data)
        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Error Creating Index - %s' % (e)
            raise exceptions.ActionIndexError(msg)
        return index_name

    def delete(self, index_name):
        try:
            self._connection.delete(index_name)
        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Error Deleting Index - %s' % (e)
            raise exceptions.ActionIndexError(msg)
        return index_name

    def open(self, index_name):
        try:
            url = '%s/_open' % index_name
            self._connection.post(url)
        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Error Opening Index - %s' % (e)
            raise exceptions.ActionIndexError(msg)
        return index_name

    def close(self, index_name):
        try:
            url = '%s/_close' % index_name
            self._connection.post(url)
        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Error Closing Index - %s' % (e)
            raise exceptions.ActionIndexError(msg)
        return index_name

    def status(self, index_name, extended=False):
        try:
            url = '%s/_status' % index_name
            res = json.loads(self._connection.get(url).content)
        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Error Fetching Index Status - %s' % (e)
            raise exceptions.ActionIndexError(msg)

        output = {}
        size = {}
        doc = {}
        merge = {}

        if index_name not in res['indices']:
            output['Status'] = 'Closed'
            return {index_name: output}
        else:
            output['Status'] = 'Open'

        output['Size'] = size
        output['Documents'] = doc
        output['Merge'] = merge

        status = res['indices'][index_name]

        size['Primary'] = status['index']['primary_size']
        doc['Current'] = status['docs']['num_docs']
        merge['Total'] = status['merges']['total']

        if extended:
            size['Total'] = status['index']['size']

            doc['Max'] = status['docs']['max_doc']
            doc['Deleted'] = status['docs']['deleted_docs']

            merge['Current'] = status['merges']['current']

            shards = {}
            for shard, value in status['shards'].iteritems():
                s_data = {}
                value = value[0]
                s_data['State'] = value['routing']['state']
                s_data['Size'] = value['index']['size']

                s_docs = {}
                s_docs['Current'] = value['docs']['num_docs']
                s_docs['Max'] = value['docs']['max_doc']
                s_docs['Deleted'] = value[u'docs']['deleted_docs']

                s_data['Documents'] = s_docs
                shards['Shard %s' % shard] = s_data

            output['Shards'] = shards
        return {index_name: output}

    def list(self, extended=False):
        try:
            health = self._connection.health
            state = self._connection.state
        except (requests.RequestException, urllib2.HTTPError), e:
            msg = 'Error Listing Indexes - %s' % (e)
            raise exceptions.ActionIndexError(msg)

        output = {}
        for index in state:
            out = {}
            if extended:
                out['state'] = state[index][u'state']

                if out['state'] == 'close':
                    out['status'] = 'closed'
                else:
                    out['status'] = health[index][u'status']

                settings = state[index]['settings']
                out['shards'] = settings['index.number_of_shards']
                out['replicas'] = settings['index.number_of_replicas']

            output[index] = out
        return output
