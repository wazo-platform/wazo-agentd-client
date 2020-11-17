# -*- coding: utf-8 -*-
# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import unittest
from hamcrest import assert_that, equal_to
from requests.exceptions import HTTPError
from wazo_lib_rest_client.tests.command import RESTCommandTestCase
from wazo_agentd_client.error import AgentdClientError
from wazo_agentd_client.commands.agents import _RequestFactory, _ResponseProcessor


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
        expected_url = '{}/by-id/2/add'.format(self.base_url)
        expected_body = {'queue_id': self.queue_id}

        req = self.req_factory.add_to_queue_by_id(self.agent_id, self.queue_id)

        self._assert_post_request(req, expected_url, expected_body)

    def test_remove_from_queue_by_id(self):
        expected_url = '{}/by-id/2/remove'.format(self.base_url)
        expected_body = {'queue_id': self.queue_id}

        req = self.req_factory.remove_from_queue_by_id(self.agent_id, self.queue_id)

        self._assert_post_request(req, expected_url, expected_body)

    def test_login_by_id(self):
        expected_url = '{}/by-id/2/login'.format(self.base_url)
        expected_body = {'extension': self.extension, 'context': self.context}

        req = self.req_factory.login_by_id(self.agent_id, self.extension, self.context)

        self._assert_post_request(req, expected_url, expected_body)

    def test_login_by_number(self):
        expected_url = '{}/by-number/1002/login'.format(self.base_url)
        expected_body = {'extension': self.extension, 'context': self.context}

        req = self.req_factory.login_by_number(self.agent_number, self.extension, self.context)

        self._assert_post_request(req, expected_url, expected_body)

    def test_login_user_agent(self):
        expected_url = '{}/users/me/agents/login'.format(self.base_url)
        expected_body = {'line_id': self.line_id}

        req = self.req_factory.login_user_agent(self.line_id)

        self._assert_post_request(req, expected_url, expected_body)

    def test_logoff_by_id(self):
        expected_url = '{}/by-id/2/logoff'.format(self.base_url)

        req = self.req_factory.logoff_by_id(self.agent_id)

        self._assert_post_request(req, expected_url)

    def test_logoff_by_number(self):
        expected_url = '{}/by-number/1002/logoff'.format(self.base_url)

        req = self.req_factory.logoff_by_number(self.agent_number)

        self._assert_post_request(req, expected_url)

    def test_logoff_user_agent(self):
        expected_url = '{}/users/me/agents/logoff'.format(self.base_url)

        req = self.req_factory.logoff_user_agent()

        self._assert_post_request(req, expected_url, expected_body=None)

    def test_pause_by_number(self):
        expected_url = '{}/by-number/1002/pause'.format(self.base_url)

        req = self.req_factory.pause_by_number(self.agent_number)

        self._assert_post_request(req, expected_url)

    def test_unpause_by_number(self):
        expected_url = '{}/by-number/1002/unpause'.format(self.base_url)

        req = self.req_factory.unpause_by_number(self.agent_number)

        self._assert_post_request(req, expected_url)

    def test_status_by_id(self):
        expected_url = '{}/by-id/2'.format(self.base_url)

        req = self.req_factory.status_by_id(self.agent_id)

        self._assert_get_request(req, expected_url)

    def test_status_by_number(self):
        expected_url = '{}/by-number/1002'.format(self.base_url)

        req = self.req_factory.status_by_number(self.agent_number)

        self._assert_get_request(req, expected_url)

    def test_logoff_all(self):
        expected_url = '{}/logoff'.format(self.base_url)

        req = self.req_factory.logoff_all()

        self._assert_post_request(req, expected_url)

    def test_relog_all(self):
        expected_url = '{}/relog'.format(self.base_url)

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


class TestResponseProcessor(unittest.TestCase):

    def setUp(self):
        self.resp_processor = _ResponseProcessor()

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
        }
        resp = new_response(200, [v])

        status, = self.resp_processor.status_all(resp)

        assert_that(status.id, equal_to(v['id']))
        assert_that(status.origin_uuid, equal_to(v['origin_uuid']))
        assert_that(status.number, equal_to(v['number']))
        assert_that(status.logged, equal_to(v['logged']))
        assert_that(status.paused, equal_to(v['paused']))
        assert_that(status.extension, equal_to(v['extension']))
        assert_that(status.context, equal_to(v['context']))
        assert_that(status.state_interface, equal_to(v['state_interface']))
