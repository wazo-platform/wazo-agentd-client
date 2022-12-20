# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


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


class _AgentStatus:

    def __init__(self, agent_id, agent_number, origin_uuid):
        self.id = agent_id
        self.number = agent_number
        self.origin_uuid = origin_uuid
        self.logged = False
        self.paused = None
        self.extension = None
        self.context = None
        self.state_interface = None

    @classmethod
    def new_from_dict(cls, d):
        obj = cls(d['id'], d['number'], d['origin_uuid'])
        obj.logged = d['logged']
        obj.paused = d['paused']
        obj.extension = d['extension']
        obj.context = d['context']
        obj.state_interface = d['state_interface']
        return obj
