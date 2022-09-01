# -*- coding: utf-8 -*-
# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from requests import HTTPError


class AgentdError(HTTPError):
    def __init__(self, response):
        self.status_code = response.status_code
        self.message = json.loads(response.text.strip())
        super(AgentdError, self).__init__(self.message, response=response)
