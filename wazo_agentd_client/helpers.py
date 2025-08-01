# Copyright 2022-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from dataclasses import dataclass, field

from wazo_agentd_client.error import AgentdClientError


class ResponseProcessor:
    def generic(self, resp):
        self._raise_if_not_success(resp)

    def status(self, resp):
        self._raise_if_not_success(resp, 200)

        return _AgentStatus.new_from_dict(resp.json())

    def status_all(self, resp):
        self._raise_if_not_success(resp, 200)

        return [_AgentStatus.new_from_dict(d) for d in resp.json()]

    def queue_list(self, resp):
        self._raise_if_not_success(resp, 200)
        return resp.json()

    def _raise_if_not_success(self, resp, expected_status_code=None):
        status_code_class = resp.status_code // 100
        if status_code_class == 4 or status_code_class == 5:
            try:
                obj = resp.json()
                obj_error = obj['error']
            except Exception:
                resp.raise_for_status()
            else:
                raise AgentdClientError(obj_error)

        if expected_status_code:
            if expected_status_code != resp.status_code:
                resp.raise_for_status()
        elif status_code_class != 2:
            resp.raise_for_status()


@dataclass
class _AgentStatus:
    id: str
    number: str
    origin_uuid: str
    logged: bool = False
    paused: bool = False
    extension: str | None = None
    context: str | None = None
    state_interface: str | None = None
    tenant_uuid: str | None = None
    queues: list[str] = field(default_factory=list)

    @classmethod
    def new_from_dict(cls, d):
        obj = cls(d['id'], d['number'], d['origin_uuid'])
        obj.logged = d['logged']
        obj.paused = d['paused']
        obj.extension = d['extension']
        obj.context = d['context']
        obj.state_interface = d['state_interface']
        obj.tenant_uuid = d['tenant_uuid']
        obj.queues = d.get('queues', [])
        return obj
