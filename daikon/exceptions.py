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


class DaikonError(Exception):
    ''' Base Exception Class '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'ERROR: Error - %s' % (self.value)


class ConfigError(DaikonError):
    ''' Config Exception Class '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'ERROR: Configuration Error - %s' % (self.value)


class IndexError(DaikonError):
    ''' Index Exception Class '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'ERROR: Index Error - %s' % (self.value)
