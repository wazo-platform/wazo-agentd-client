# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import requests

from wazo_lib_rest_client import RESTCommand
from wazo_agentd_client.helpers import ResponseProcessor


class AgentsCommand(RESTCommand):

    resource = 'agents'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._req_factory = _RequestFactory(self.base_url)
        self._resp_processor = ResponseProcessor()

    def add_agent_to_queue(self, agent_id, queue_id, tenant_uuid=None):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        req = self._req_factory.add_to_queue_by_id(agent_id, queue_id, tenant_uuid=tenant_uuid)
        self._execute(req, self._resp_processor.generic)

    def remove_agent_from_queue(self, agent_id, queue_id, tenant_uuid=None):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        req = self._req_factory.remove_from_queue_by_id(agent_id, queue_id, tenant_uuid=tenant_uuid)
        self._execute(req, self._resp_processor.generic)

    def login_agent(self, agent_id, extension, context, tenant_uuid=None):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        req = self._req_factory.login_by_id(agent_id, extension, context, tenant_uuid=tenant_uuid)
        self._execute(req, self._resp_processor.generic)

    def login_agent_by_number(self, agent_number, extension, context, tenant_uuid=None):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        req = self._req_factory.login_by_number(agent_number, extension, context, tenant_uuid=tenant_uuid)
        self._execute(req, self._resp_processor.generic)

    def login_user_agent(self, line_id, tenant_uuid=None):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.login_user_agent(line_id, tenant_uuid=tenant_uuid)
        self._execute(req, self._resp_processor.generic)

    def logoff_agent(self, agent_id, tenant_uuid=None):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        req = self._req_factory.logoff_by_id(agent_id, tenant_uuid=tenant_uuid)
        self._execute(req, self._resp_processor.generic)

    def logoff_agent_by_number(self, agent_number, tenant_uuid=None):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        req = self._req_factory.logoff_by_number(agent_number, tenant_uuid=tenant_uuid)
        self._execute(req, self._resp_processor.generic)

    def logoff_user_agent(self, tenant_uuid=None):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.logoff_user_agent(tenant_uuid=tenant_uuid)
        self._execute(req, self._resp_processor.generic)

    def logoff_all_agents(self, tenant_uuid=None, recurse=False):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        req = self._req_factory.logoff_all(tenant_uuid=tenant_uuid, recurse=recurse)
        self._execute(req, self._resp_processor.generic)

    def relog_all_agents(self, tenant_uuid=None, recurse=False, timeout=None):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        req = self._req_factory.relog_all(tenant_uuid=tenant_uuid, recurse=recurse)
        self._execute(req, self._resp_processor.generic, timeout=timeout)

    def pause_agent_by_number(self, agent_number, tenant_uuid=None):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        req = self._req_factory.pause_by_number(agent_number, tenant_uuid=tenant_uuid)
        self._execute(req, self._resp_processor.generic)

    def pause_user_agent(self, tenant_uuid=None):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.pause_user_agent(tenant_uuid=tenant_uuid)
        self._execute(req, self._resp_processor.generic)

    def unpause_agent_by_number(self, agent_number, tenant_uuid=None):
        req = self._req_factory.unpause_by_number(agent_number, tenant_uuid=tenant_uuid)
        self._execute(req, self._resp_processor.generic)

    def unpause_user_agent(self, tenant_uuid=None):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.unpause_user_agent(tenant_uuid=tenant_uuid)
        self._execute(req, self._resp_processor.generic)

    def get_agent_status(self, agent_id, tenant_uuid=None):
        req = self._req_factory.status_by_id(agent_id, tenant_uuid=tenant_uuid)
        return self._execute(req, self._resp_processor.status)

    def get_agent_status_by_number(self, agent_number, tenant_uuid=None):
        req = self._req_factory.status_by_number(agent_number, tenant_uuid=tenant_uuid)
        return self._execute(req, self._resp_processor.status)

    def get_user_agent_status(self, tenant_uuid=None):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        user_req_factory = _RequestFactory(self._client.url())
        req = user_req_factory.status_user_agent(tenant_uuid=tenant_uuid)
        return self._execute(req, self._resp_processor.status)

    def get_agent_statuses(self, tenant_uuid=None, recurse=False):
        tenant_uuid = tenant_uuid or self._client.tenant_uuid
        req = self._req_factory.status_all(tenant_uuid=tenant_uuid, recurse=recurse)
        return self._execute(req, self._resp_processor.status_all)

    def _execute(self, req, processor_fun, timeout=None):
        timeout = timeout if timeout is not None else self.timeout
        resp = self.session.send(self.session.prepare_request(req), timeout=timeout)
        return processor_fun(resp)


class _RequestFactory:

    def __init__(self, base_url):
        self._base_url = base_url
        self._headers = {'Accept': 'application/json'}

    def add_to_queue_by_id(self, agent_id, queue_id, tenant_uuid=None):
        return self._add_to_queue('by-id', agent_id, queue_id, tenant_uuid=tenant_uuid)

    def _add_to_queue(self, by, value, queue_id, tenant_uuid=None):
        url = f'{self._base_url}/{by}/{value}/add'
        obj = {'queue_id': queue_id}
        additional_headers = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        return self._new_post_request(url, obj, additional_headers=additional_headers)

    def remove_from_queue_by_id(self, agent_id, queue_id, tenant_uuid=None):
        return self._remove_from_queue('by-id', agent_id, queue_id, tenant_uuid=tenant_uuid)

    def _remove_from_queue(self, by, value, queue_id, tenant_uuid=None):
        url = f'{self._base_url}/{by}/{value}/remove'
        obj = {'queue_id': queue_id}
        additional_headers = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        return self._new_post_request(url, obj, additional_headers=additional_headers)

    def login_by_id(self, agent_id, extension, context, tenant_uuid=None):
        return self._login('by-id', agent_id, extension, context, tenant_uuid=tenant_uuid)

    def login_by_number(self, agent_number, extension, context, tenant_uuid=None):
        return self._login('by-number', agent_number, extension, context, tenant_uuid=tenant_uuid)

    def _login(self, by, value, extension, context, tenant_uuid=None):
        url = f'{self._base_url}/{by}/{value}/login'
        obj = {'extension': extension, 'context': context}
        additional_headers = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        return self._new_post_request(url, obj, additional_headers=additional_headers)

    def login_user_agent(self, line_id, tenant_uuid=None):
        url = f'{self._base_url}/users/me/agents/login'
        obj = {'line_id': line_id}
        additional_headers = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        return self._new_post_request(url, obj, additional_headers=additional_headers)

    def logoff_by_id(self, agent_id, tenant_uuid=None):
        return self._logoff('by-id', agent_id, tenant_uuid=tenant_uuid)

    def logoff_by_number(self, agent_number, tenant_uuid=None):
        return self._logoff('by-number', agent_number, tenant_uuid=tenant_uuid)

    def _logoff(self, by, value, tenant_uuid=None):
        url = f'{self._base_url}/{by}/{value}/logoff'
        additional_headers = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        return self._new_post_request(url, additional_headers=additional_headers)

    def logoff_user_agent(self, tenant_uuid=None):
        url = f'{self._base_url}/users/me/agents/logoff'
        additional_headers = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        return self._new_post_request(url, additional_headers=additional_headers)

    def pause_by_number(self, agent_number, tenant_uuid=None):
        return self._pause('by-number', agent_number, tenant_uuid=tenant_uuid)

    def _pause(self, by, value, tenant_uuid=None):
        url = f'{self._base_url}/{by}/{value}/pause'
        additional_headers = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        return self._new_post_request(url, additional_headers=additional_headers)

    def pause_user_agent(self, tenant_uuid=None):
        url = f'{self._base_url}/users/me/agents/pause'
        additional_headers = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        return self._new_post_request(url, additional_headers=additional_headers)

    def unpause_by_number(self, agent_number, tenant_uuid=None):
        return self._unpause('by-number', agent_number, tenant_uuid=tenant_uuid)

    def _unpause(self, by, value, tenant_uuid=None):
        url = f'{self._base_url}/{by}/{value}/unpause'
        additional_headers = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        return self._new_post_request(url, additional_headers=additional_headers)

    def unpause_user_agent(self, tenant_uuid=None):
        url = f'{self._base_url}/users/me/agents/unpause'
        additional_headers = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        return self._new_post_request(url, additional_headers=additional_headers)

    def status_by_id(self, agent_id, tenant_uuid=None):
        return self._status('by-id', agent_id, tenant_uuid=tenant_uuid)

    def status_by_number(self, agent_number, tenant_uuid=None):
        return self._status('by-number', agent_number, tenant_uuid=tenant_uuid)

    def _status(self, by, value, tenant_uuid=None):
        url = f'{self._base_url}/{by}/{value}'
        additional_headers = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        return self._new_get_request(url, additional_headers=additional_headers)

    def status_user_agent(self, tenant_uuid=None):
        url = f'{self._base_url}/users/me/agents'
        additional_headers = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        return self._new_get_request(url, additional_headers=additional_headers)

    def logoff_all(self, tenant_uuid=None, recurse=False):
        url = f'{self._base_url}/logoff'
        additional_headers = {}
        params = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        if recurse:
            params['recurse'] = True
        return self._new_post_request(url)

    def relog_all(self, tenant_uuid=None, recurse=False):
        url = f'{self._base_url}/relog'
        additional_headers = {}
        params = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        if recurse:
            params['recurse'] = True
        return self._new_post_request(url, additional_headers=additional_headers, params=params)

    def status_all(self, tenant_uuid=None, recurse=False):
        url = self._base_url
        additional_headers = {}
        params = {}
        if tenant_uuid:
            additional_headers['Wazo-Tenant'] = tenant_uuid
        if recurse:
            params['recurse'] = True
        return self._new_get_request(url, additional_headers=additional_headers, params=params)

    def _new_get_request(self, url, additional_headers=None, params=None):
        headers = dict(self._headers)
        if additional_headers:
            headers.update(additional_headers)
        return requests.Request('GET', url, headers, params=params)

    def _new_post_request(self, url, obj=None, additional_headers=None, params=None):
        headers = dict(self._headers)
        if additional_headers:
            headers.update(additional_headers)
        if obj is None:
            data = None
        else:
            data = json.dumps(obj)
            headers['Content-Type'] = 'application/json'
        return requests.Request('POST', url, headers, data=data, params=params)

