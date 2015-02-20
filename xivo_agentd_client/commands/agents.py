# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import json
import requests

from xivo_lib_rest_client import BaseHTTPCommand
from xivo_agentd_client.error import AgentClientError


class AgentsCommand(BaseHTTPCommand):

    resource = 'agents'

    def __init__(self, *args, **kwargs):
        super(AgentsCommand, self).__init__(*args, **kwargs)
        self._req_factory = _RequestFactory(self.base_url)
        self._resp_processor = _ResponseProcessor()

    def add_agent_to_queue(self, agent_id, queue_id):
        req = self._req_factory.add_to_queue_by_id(agent_id, queue_id)
        self._execute(req, self._resp_processor.generic)

    def remove_agent_from_queue(self, agent_id, queue_id):
        req = self._req_factory.remove_from_queue_by_id(agent_id, queue_id)
        self._execute(req, self._resp_processor.generic)

    def login_agent(self, agent_id, extension, context):
        req = self._req_factory.login_by_id(agent_id, extension, context)
        self._execute(req, self._resp_processor.generic)

    def login_agent_by_number(self, agent_number, extension, context):
        req = self._req_factory.login_by_number(agent_number, extension, context)
        self._execute(req, self._resp_processor.generic)

    def logoff_agent(self, agent_id):
        req = self._req_factory.logoff_by_id(agent_id)
        self._execute(req, self._resp_processor.generic)

    def logoff_agent_by_number(self, agent_number):
        req = self._req_factory.logoff_by_number(agent_number)
        self._execute(req, self._resp_processor.generic)

    def logoff_all_agents(self):
        req = self._req_factory.logoff_all()
        self._execute(req, self._resp_processor.generic)

    def relog_all_agents(self):
        req = self._req_factory.relog_all()
        self._execute(req, self._resp_processor.generic)

    def pause_agent_by_number(self, agent_number):
        req = self._req_factory.pause_by_number(agent_number)
        self._execute(req, self._resp_processor.generic)

    def unpause_agent_by_number(self, agent_number):
        req = self._req_factory.unpause_by_number(agent_number)
        self._execute(req, self._resp_processor.generic)

    def get_agent_status(self, agent_id):
        req = self._req_factory.status_by_id(agent_id)
        return self._execute(req, self._resp_processor.status)

    def get_agent_status_by_number(self, agent_number):
        req = self._req_factory.status_by_number(agent_number)
        return self._execute(req, self._resp_processor.status)

    def get_agent_statuses(self):
        req = self._req_factory.status_all()
        return self._execute(req, self._resp_processor.status_all)

    def _execute(self, req, processor_fun):
        resp = self.session.send(self.session.prepare_request(req))
        return processor_fun(resp)


class _RequestFactory(object):

    def __init__(self, base_url):
        self._base_url = base_url
        self._headers = {'Accept': 'application/json'}

    def add_to_queue_by_id(self, agent_id, queue_id):
        return self._add_to_queue('by-id', agent_id, queue_id)

    def _add_to_queue(self, by, value, queue_id):
        url = '{}/{}/{}/add'.format(self._base_url, by, value)
        obj = {'queue_id': queue_id}
        return self._new_post_request(url, obj)

    def remove_from_queue_by_id(self, agent_id, queue_id):
        return self._remove_from_queue('by-id', agent_id, queue_id)

    def _remove_from_queue(self, by, value, queue_id):
        url = '{}/{}/{}/remove'.format(self._base_url, by, value)
        obj = {'queue_id': queue_id}
        return self._new_post_request(url, obj)

    def login_by_id(self, agent_id, extension, context):
        return self._login('by-id', agent_id, extension, context)

    def login_by_number(self, agent_number, extension, context):
        return self._login('by-number', agent_number, extension, context)

    def _login(self, by, value, extension, context):
        url = '{}/{}/{}/login'.format(self._base_url, by, value)
        obj = {'extension': extension, 'context': context}
        return self._new_post_request(url, obj)

    def logoff_by_id(self, agent_id):
        return self._logoff('by-id', agent_id)

    def logoff_by_number(self, agent_number):
        return self._logoff('by-number', agent_number)

    def _logoff(self, by, value):
        url = '{}/{}/{}/logoff'.format(self._base_url, by, value)
        return self._new_post_request(url)

    def pause_by_number(self, agent_number):
        return self._pause('by-number', agent_number)

    def _pause(self, by, value):
        url = '{}/{}/{}/pause'.format(self._base_url, by, value)
        return self._new_post_request(url)

    def unpause_by_number(self, agent_number):
        return self._unpause('by-number', agent_number)

    def _unpause(self, by, value):
        url = '{}/{}/{}/unpause'.format(self._base_url, by, value)
        return self._new_post_request(url)

    def status_by_id(self, agent_id):
        return self._status('by-id', agent_id)

    def status_by_number(self, agent_number):
        return self._status('by-number', agent_number)

    def _status(self, by, value):
        url = '{}/{}/{}'.format(self._base_url, by, value)
        return self._new_get_request(url)

    def logoff_all(self):
        url = '{}/logoff'.format(self._base_url)
        return self._new_post_request(url)

    def relog_all(self):
        url = '{}/relog'.format(self._base_url)
        return self._new_post_request(url)

    def status_all(self):
        url = self._base_url
        return self._new_get_request(url)

    def _new_get_request(self, url):
        return requests.Request('GET', url, self._headers)

    def _new_post_request(self, url, obj=None):
        if obj is None:
            data = None
            headers = self._headers
        else:
            data = json.dumps(obj)
            headers = dict(self._headers)
            headers['Content-Type'] = 'application/json'
        return requests.Request('POST', url, headers, data=data)


class _ResponseProcessor(object):

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
                raise AgentClientError(obj_error)

        if expected_status_code:
            if expected_status_code != resp.status_code:
                resp.raise_for_status()
        elif status_code_class != 2:
            resp.raise_for_status()


class _AgentStatus(object):

    def __init__(self, agent_id, agent_number, origin_uuid):
        self.id = agent_id
        self.number = agent_number
        self.origin_uuid = origin_uuid
        self.logged = False
        self.extension = None
        self.context = None

    @classmethod
    def new_from_dict(cls, d):
        obj = cls(d['id'], d['number'], d['origin_uuid'])
        obj.logged = d['logged']
        obj.extension = d['extension']
        obj.context = d['context']
        return obj
