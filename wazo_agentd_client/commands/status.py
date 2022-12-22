# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


from wazo_lib_rest_client.command import RESTCommand
from wazo_agentd_client.helpers import ResponseProcessor


class StatusCommand(RESTCommand):
    resource = 'status'

    def __call__(self):
        _resp_processor = ResponseProcessor()
        headers = self._get_headers()
        url = self.base_url
        r = self.session.get(url, headers=headers)

        if r.status_code != 200:
            _resp_processor.generic(r)

        return r.json()
