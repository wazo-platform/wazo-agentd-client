# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from xivo_lib_rest_client import make_client

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 9493
DEFAULT_VERSION = '1.0'

_Client = make_client('agentd_client.commands')

def Client(host=DEFAULT_HOST, port=DEFAULT_PORT, version=DEFAULT_VERSION):
    return _Client(host, port, version, https=False)
