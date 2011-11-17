import requests
import anyjson as json
import urlparse

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
