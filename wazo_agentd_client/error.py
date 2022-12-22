# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

NO_SUCH_AGENT = 'no such agent'
NO_SUCH_LINE = 'no such line'
NO_SUCH_QUEUE = 'no such queue'
ALREADY_LOGGED = 'already logged'
NOT_LOGGED = 'not logged in'
ALREADY_IN_USE = 'extension and context already in use'
ALREADY_IN_QUEUE = 'agent already in queue'
NOT_IN_QUEUE = 'agent not in queue'
NO_SUCH_EXTEN = 'no such extension and context'
CONTEXT_DIFFERENT_TENANT = 'agent and context are not in the same tenant'
QUEUE_DIFFERENT_TENANT = 'agent and queue are not in the same tenant'
UNAUTHORIZED = 'invalid token or unauthorized'


class AgentdClientError(Exception):
    def __init__(self, error):
        super().__init__(error)
        self.error = error
