# Copyright 2015-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_lib_rest_client.client import BaseClient


class AgentdClient(BaseClient):
    namespace = 'wazo_agentd_client.commands'

    def __init__(self, host, port=443, prefix='/api/agentd', version='1.0', **kwargs):
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
