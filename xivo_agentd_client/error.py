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

NO_SUCH_AGENT = 'no such agent'
NO_SUCH_QUEUE = 'no such queue'
ALREADY_LOGGED = 'already logged'
NOT_LOGGED = 'not logged in'
ALREADY_IN_USE = 'extension and context already in use'
ALREADY_IN_QUEUE = 'agent already in queue'
NOT_IN_QUEUE = 'agent not in queue'
NO_SUCH_EXTEN = 'no such extension and context'


class AgentdClientError(Exception):

    def __init__(self, error):
        super(AgentdClientError, self).__init__(error)
        self.error = error
