# -*- coding: utf-8 -*-
# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from requests import HTTPError


class AgentdError(HTTPError):
    def __init__(self, response):
        try:
            body = response.json()
        except ValueError:
            raise InvalidAgentdError()

        self.status_code = response.status_code
        try:
            self.message = body['message']
            self.error_id = body['error_id']
            self.details = body['details']
            self.timestamp = body['timestamp']
            if body.get('resource', None):
                self.resource = body['resource']
        except KeyError:
            raise InvalidAgentdError()

        exception_message = '{e.message}: {e.details}'.format(e=self)
        super(AgentdError, self).__init__(exception_message, response=response)


class AgentdServiceUnavailable(AgentdError):
    pass


class AgentdProtocolError(AgentdError):
    def __init__(self, response):
        try:
            body = response.json()
        except ValueError:
            raise InvalidAgentdError()

        try:
            for msg in body:
                self.message = msg['Message']
        except (TypeError, KeyError):
            raise InvalidAgentdError()

        exception_message = '{e.message}'.format(e=self)
        super(HTTPError, self).__init__(exception_message, response=response)


class InvalidAgentdError(Exception):
    pass
