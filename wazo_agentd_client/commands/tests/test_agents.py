# Copyright 2015-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import unittest

from hamcrest import assert_that, equal_to
from requests.exceptions import HTTPError
from wazo_lib_rest_client.tests.command import RESTCommandTestCase

from wazo_agentd_client.commands.agents import _RequestFactory
from wazo_agentd_client.error import AgentdClientError
from wazo_agentd_client.helpers import ResponseProcessor

new_response = RESTCommandTestCase.new_response

FAKE_TENANT = 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee'


class TestRequestFactory(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://example.org/foo'
        self.req_factory = _RequestFactory(self.base_url)
        self.agent_id = 2
        self.agent_number = '1002'
        self.extension = '1222'
        self.context = 'alice'
        self.queue_id = 3
        self.line_id = 4

    def test_add_to_queue_by_id(self):
        expected_url = f'{self.base_url}/by-id/2/add'
        expected_body = {'queue_id': self.queue_id}

        req = self.req_factory.add_to_queue_by_id(self.agent_id, self.queue_id)

        self._assert_post_request(req, expected_url, expected_body)

    def test_remove_from_queue_by_id(self):
        expected_url = f'{self.base_url}/by-id/2/remove'
        expected_body = {'queue_id': self.queue_id}

        req = self.req_factory.remove_from_queue_by_id(self.agent_id, self.queue_id)

        self._assert_post_request(req, expected_url, expected_body)

    def test_list_user_queues(self):
        expected_url = f'{self.base_url}/users/me/agents/queues'

        req = self.req_factory.list_user_queues()

        self._assert_get_request(req, expected_url)

    def test_list_user_queues_with_params(self):
        expected_url = f'{self.base_url}/users/me/agents/queues'
        expected_params = {'order': 'name', 'direction': 'asc'}

        req = self.req_factory.list_user_queues(order='name', direction='asc')

        self._assert_get_request_with_params(req, expected_url, expected_params)

    def test_list_user_queues_with_pagination(self):
        expected_url = f'{self.base_url}/users/me/agents/queues'
        expected_params = {
            'order': 'name',
            'direction': 'asc',
            'limit': '10',
            'offset': '20',
        }

        req = self.req_factory.list_user_queues(
            order='name', direction='asc', limit=10, offset=20
        )

        self._assert_get_request_with_params(req, expected_url, expected_params)

    def test_list_queues_by_id(self):
        expected_url = f'{self.base_url}/by-id/2/queues'

        req = self.req_factory.list_queues_by_id(self.agent_id)

        self._assert_get_request(req, expected_url)

    def test_list_queues_by_id_with_params(self):
        expected_url = f'{self.base_url}/by-id/2/queues'
        expected_params = {'order': 'id', 'direction': 'desc'}

        req = self.req_factory.list_queues_by_id(
            self.agent_id, order='id', direction='desc'
        )

        self._assert_get_request_with_params(req, expected_url, expected_params)

    def test_list_queues_by_id_with_pagination(self):
        expected_url = f'{self.base_url}/by-id/2/queues'
        expected_params = {
            'order': 'id',
            'direction': 'desc',
            'limit': '5',
            'offset': '10',
        }

        req = self.req_factory.list_queues_by_id(
            self.agent_id, order='id', direction='desc', limit=5, offset=10
        )

        self._assert_get_request_with_params(req, expected_url, expected_params)

    def test_list_queues_by_number(self):
        expected_url = f'{self.base_url}/by-number/1002/queues'

        req = self.req_factory.list_queues_by_number(self.agent_number)

        self._assert_get_request(req, expected_url)

    def test_list_queues_by_number_with_params(self):
        expected_url = f'{self.base_url}/by-number/1002/queues'
        expected_params = {'order': 'name', 'direction': 'asc'}

        req = self.req_factory.list_queues_by_number(
            self.agent_number, order='name', direction='asc'
        )

        self._assert_get_request_with_params(req, expected_url, expected_params)

    def test_list_queues_by_number_with_pagination(self):
        expected_url = f'{self.base_url}/by-number/1002/queues'
        expected_params = {
            'order': 'name',
            'direction': 'asc',
            'limit': '15',
            'offset': '30',
        }

        req = self.req_factory.list_queues_by_number(
            self.agent_number, order='name', direction='asc', limit=15, offset=30
        )

        self._assert_get_request_with_params(req, expected_url, expected_params)

    def test_login_by_id(self):
        expected_url = f'{self.base_url}/by-id/2/login'
        expected_body = {'extension': self.extension, 'context': self.context}

        req = self.req_factory.login_by_id(self.agent_id, self.extension, self.context)

        self._assert_post_request(req, expected_url, expected_body)

    def test_login_by_number(self):
        expected_url = f'{self.base_url}/by-number/1002/login'
        expected_body = {'extension': self.extension, 'context': self.context}

        req = self.req_factory.login_by_number(
            self.agent_number, self.extension, self.context
        )

        self._assert_post_request(req, expected_url, expected_body)

    def test_login_user_agent(self):
        expected_url = f'{self.base_url}/users/me/agents/login'
        expected_body = {'line_id': self.line_id}

        req = self.req_factory.login_user_agent(self.line_id)

        self._assert_post_request(req, expected_url, expected_body)

    def test_logoff_by_id(self):
        expected_url = f'{self.base_url}/by-id/2/logoff'

        req = self.req_factory.logoff_by_id(self.agent_id)

        self._assert_post_request(req, expected_url)

    def test_logoff_by_number(self):
        expected_url = f'{self.base_url}/by-number/1002/logoff'

        req = self.req_factory.logoff_by_number(self.agent_number)

        self._assert_post_request(req, expected_url)

    def test_logoff_user_agent(self):
        expected_url = f'{self.base_url}/users/me/agents/logoff'

        req = self.req_factory.logoff_user_agent()

        self._assert_post_request(req, expected_url, expected_body=None)

    def test_pause_by_number(self):
        expected_url = f'{self.base_url}/by-number/1002/pause'

        req = self.req_factory.pause_by_number(self.agent_number)

        self._assert_post_request(req, expected_url)

    def test_unpause_by_number(self):
        expected_url = f'{self.base_url}/by-number/1002/unpause'

        req = self.req_factory.unpause_by_number(self.agent_number)

        self._assert_post_request(req, expected_url)

    def test_status_by_id(self):
        expected_url = f'{self.base_url}/by-id/2'

        req = self.req_factory.status_by_id(self.agent_id)

        self._assert_get_request(req, expected_url)

    def test_status_by_number(self):
        expected_url = f'{self.base_url}/by-number/1002'

        req = self.req_factory.status_by_number(self.agent_number)

        self._assert_get_request(req, expected_url)

    def test_logoff_all(self):
        expected_url = f'{self.base_url}/logoff'

        req = self.req_factory.logoff_all()

        self._assert_post_request(req, expected_url)

    def test_relog_all(self):
        expected_url = f'{self.base_url}/relog'

        req = self.req_factory.relog_all()

        self._assert_post_request(req, expected_url)

    def test_status_all(self):
        expected_url = self.base_url

        req = self.req_factory.status_all()

        self._assert_get_request(req, expected_url)

    def _assert_get_request(self, req, expected_url):
        prep_req = req.prepare()
        assert_that(prep_req.method, equal_to('GET'))
        assert_that(prep_req.url, equal_to(expected_url))

    def _assert_post_request(self, req, expected_url, expected_body=None):
        prep_req = req.prepare()
        assert_that(prep_req.method, equal_to('POST'))
        assert_that(prep_req.url, equal_to(expected_url))
        if expected_body is None:
            assert_that(prep_req.body, equal_to(None))
        else:
            assert_that(json.loads(prep_req.body), equal_to(expected_body))

    def _assert_get_request_with_params(self, req, expected_url, expected_params):
        prep_req = req.prepare()
        before_params, after_params = prep_req.url.split('?', 1)
        pairs = [pair.split('=', 1) for pair in after_params.split('&')]
        params = {k: v for (k, v) in pairs}
        assert_that(prep_req.method, equal_to('GET'))
        assert_that(params, equal_to(expected_params))
        assert_that(before_params, equal_to(expected_url))


class TestResponseProcessor(unittest.TestCase):
    def setUp(self):
        self.resp_processor = ResponseProcessor()

    def test_generic_on_200(self):
        resp = new_response(200)

        self.resp_processor.generic(resp)

    def test_generic_on_204(self):
        resp = new_response(204)

        self.resp_processor.generic(resp)

    def test_generic_on_404_with_json_error(self):
        v = {'error': 'meh'}
        resp = new_response(404, v)

        try:
            self.resp_processor.generic(resp)
            self.fail()
        except AgentdClientError as e:
            assert_that(e.error, equal_to(v['error']))

    def test_generic_on_500_no_json_error(self):
        resp = new_response(500)

        self.assertRaises(HTTPError, self.resp_processor.generic, resp)

    def test_status_on_200(self):
        v = {
            'id': 2,
            'origin_uuid': '11-222',
            'number': '1002',
            'logged': True,
            'paused': True,
            'extension': '1222',
            'context': 'alice',
            'state_interface': 'SIP/alice',
            'tenant_uuid': FAKE_TENANT,
        }
        resp = new_response(200, v)

        status = self.resp_processor.status(resp)

        assert_that(status.id, equal_to(v['id']))
        assert_that(status.origin_uuid, equal_to(v['origin_uuid']))
        assert_that(status.number, equal_to(v['number']))
        assert_that(status.logged, equal_to(v['logged']))
        assert_that(status.paused, equal_to(v['paused']))
        assert_that(status.extension, equal_to(v['extension']))
        assert_that(status.context, equal_to(v['context']))
        assert_that(status.state_interface, equal_to(v['state_interface']))
        assert_that(status.tenant_uuid, equal_to(FAKE_TENANT))

    def test_status_all_on_200(self):
        v = {
            'id': 2,
            'origin_uuid': '11-222',
            'number': '1002',
            'logged': True,
            'paused': False,
            'extension': '1222',
            'context': 'alice',
            'state_interface': 'SIP/alice',
            'tenant_uuid': FAKE_TENANT,
        }
        resp = new_response(200, [v])

        status = self.resp_processor.status_all(resp)[0]

        assert_that(status.id, equal_to(v['id']))
        assert_that(status.origin_uuid, equal_to(v['origin_uuid']))
        assert_that(status.number, equal_to(v['number']))
        assert_that(status.logged, equal_to(v['logged']))
        assert_that(status.paused, equal_to(v['paused']))
        assert_that(status.extension, equal_to(v['extension']))
        assert_that(status.context, equal_to(v['context']))
        assert_that(status.state_interface, equal_to(v['state_interface']))
        assert_that(status.tenant_uuid, equal_to(FAKE_TENANT))

    def test_queue_list_on_200(self):
        v = [
            {
                'id': 1,
                'name': 'queue1',
                'tenant_uuid': FAKE_TENANT,
            },
            {
                'id': 2,
                'name': 'queue2',
                'tenant_uuid': FAKE_TENANT,
            },
        ]
        resp = new_response(200, v)

        result = self.resp_processor.queue_list(resp)

        assert_that(result, equal_to(v))
