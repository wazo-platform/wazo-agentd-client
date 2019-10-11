# -*- coding: utf-8 -*-
# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_lib_rest_client.client import BaseClient


class AgentdClient(BaseClient):

    namespace = 'agentd_client.commands'

    def __init__(self, host, port=9493, version='1.0', **kwargs):
        super(AgentdClient, self).__init__(host=host, port=port, version=version, **kwargs)
