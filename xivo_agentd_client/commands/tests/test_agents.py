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
import unittest
from hamcrest import assert_that, equal_to
from mock import Mock, sentinel
from requests.exceptions import HTTPError
from xivo_lib_rest_client.tests.command import HTTPCommandTestCase
from xivo_agentd_client.error import AgentClientError
from xivo_agentd_client.commands.agents import AgentsCommand, _RequestFactory, _ResponseProcessor


new_response = HTTPCommandTestCase.new_response

class TestAgents(HTTPCommandTestCase):

    Command = AgentsCommand

    # XXX these tests are so mocked that I don't know if there's any real value

    def setUp(self):
        super(TestAgents, self).setUp()
        self.req_factory = Mock(_RequestFactory)
        self.resp_processor = Mock(_ResponseProcessor)
        self.command._req_factory = self.req_factory
        self.command._resp_processor = self.resp_processor
        self.session.prepare_request.return_value = sentinel.prep_req
        self.session.send.return_value = sentinel.resp

    def test_login_agent(self):
        self.req_factory.login_by_id.return_value = sentinel.req

        self.command.login_agent(sentinel.agent_id, sentinel.extension, sentinel.context)

        self.req_factory.login_by_id.assert_called_once_with(sentinel.agent_id, sentinel.extension, sentinel.context)
        self.resp_processor.generic.assert_called_once_with(sentinel.resp)
        self._assert_session_called()

    def test_login_agent_by_number(self):
        self.req_factory.login_by_number.return_value = sentinel.req

        self.command.login_agent_by_number(sentinel.agent_number, sentinel.extension, sentinel.context)

        self.req_factory.login_by_number.assert_called_once_with(sentinel.agent_number, sentinel.extension, sentinel.context)
        self.resp_processor.generic.assert_called_once_with(sentinel.resp)
        self._assert_session_called()

    def test_get_agent_status(self):
        self.req_factory.status_by_id.return_value = sentinel.req
        self.resp_processor.status.return_value = sentinel.res

        res = self.command.get_agent_status(sentinel.agent_id)

        assert_that(res, equal_to(sentinel.res))
        self.req_factory.status_by_id.assert_called_once_with(sentinel.agent_id)
        self.resp_processor.status.assert_called_once_with(sentinel.resp)
        self._assert_session_called()

    def test_get_agent_status_by_number(self):
        self.req_factory.status_by_number.return_value = sentinel.req
        self.resp_processor.status.return_value = sentinel.res

        res = self.command.get_agent_status_by_number(sentinel.agent_number)

        assert_that(res, equal_to(sentinel.res))
        self.req_factory.status_by_number.assert_called_once_with(sentinel.agent_number)
        self.resp_processor.status.assert_called_once_with(sentinel.resp)
        self._assert_session_called()

    def _assert_session_called(self):
        self.session.prepare_request.assert_called_once_with(sentinel.req)
        self.session.send.assert_called_once_with(sentinel.prep_req)


class TestRequestFactory(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://example.org/foo'
        self.req_factory = _RequestFactory(self.base_url)
        self.agent_id = 2
        self.agent_number = '1002'
        self.extension = '1222'
        self.context = 'alice'
        self.queue_id = 3

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

    def test_logoff_by_id(self):
        expected_url = '{}/by-id/2/logoff'.format(self.base_url)

        req = self.req_factory.logoff_by_id(self.agent_id)

        self._assert_post_request(req, expected_url)

    def test_logoff_by_number(self):
        expected_url = '{}/by-number/1002/logoff'.format(self.base_url)

        req = self.req_factory.logoff_by_number(self.agent_number)

        self._assert_post_request(req, expected_url)

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
        except AgentClientError as e:
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
            'extension': '1222',
            'context': 'alice',
        }
        resp = new_response(200, v)

        status = self.resp_processor.status(resp)

        assert_that(status.id, equal_to(v['id']))
        assert_that(status.origin_uuid, equal_to(v['origin_uuid']))
        assert_that(status.number, equal_to(v['number']))
        assert_that(status.logged, equal_to(v['logged']))
        assert_that(status.extension, equal_to(v['extension']))
        assert_that(status.context, equal_to(v['context']))

    def test_status_all_on_200(self):
        v = {
            'id': 2,
            'origin_uuid': '11-222',
            'number': '1002',
            'logged': True,
            'extension': '1222',
            'context': 'alice',
        }
        resp = new_response(200, [v])

        status, = self.resp_processor.status_all(resp)

        assert_that(status.id, equal_to(v['id']))
        assert_that(status.origin_uuid, equal_to(v['origin_uuid']))
        assert_that(status.number, equal_to(v['number']))
        assert_that(status.logged, equal_to(v['logged']))
        assert_that(status.extension, equal_to(v['extension']))
        assert_that(status.context, equal_to(v['context']))
