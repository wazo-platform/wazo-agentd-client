# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

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
