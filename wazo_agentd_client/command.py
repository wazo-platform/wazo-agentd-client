# -*- coding: utf-8 -*-
# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_lib_rest_client.command import RESTCommand

from .exceptions import AgentdError
from .exceptions import AgentdServiceUnavailable
from .exceptions import InvalidAgentdError
from .exceptions import AgentdProtocolError


class AgentdCommand(RESTCommand):
    @staticmethod
    def raise_from_response(response):
        if response.status_code == 503:
            raise AgentdServiceUnavailable(response)

        try:
            raise AgentdError(response)
        except InvalidAgentdError:
            RESTCommand.raise_from_response(response)

    @staticmethod
    def raise_from_protocol(response):
        try:
            raise AgentdProtocolError(response)
        except InvalidAgentdError:
            RESTCommand.raise_from_response(response)

