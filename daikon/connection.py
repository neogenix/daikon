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
import urlparse

# ---------------------
# Logging
# ---------------------

log = logging.getLogger('daikon')


# ---------------------
# Classes
# ---------------------

class Connection(object):
    _state = None
    _health = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = 'http://%s:%s' % (host, port)

    def get(self, path, raise_for_status=True):
        url = urlparse.urljoin(self.url, path)
        req = requests.get(url)
        if raise_for_status:
            req.raise_for_status()
        return req

    def post(self, path, data=None, raise_for_status=True):
        url = urlparse.urljoin(self.url, path)
        req = requests.post(url, data=data)
        if raise_for_status:
            req.raise_for_status()
        return req

    def delete(self, path, raise_for_status=True):
        url = urlparse.urljoin(self.url, path)
        req = requests.delete(url)
        if raise_for_status:
            req.raise_for_status()
        return req

    @property
    def health(self):
        if self._health is not None:
            return self._health

        path = '/_cluster/health?level=indices'
        health = json.loads(self.get(path).content)
        self._health = health[u'indices']
        return self._health

    @property
    def state(self):
        if self._state is not None:
            return self._state

        path = '/_cluster/state'
        state = json.loads(self.get(path).content)
        self._state = state[u'metadata'][u'indices']
        return self._state
