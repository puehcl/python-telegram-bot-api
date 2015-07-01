import unittest
import unittest.mock
import sys
import json

import requests

ORIGINAL_REQUESTS = sys.modules["requests"]
sys.modules["requests"] = unittest.mock.Mock(spec=ORIGINAL_REQUESTS)
import telegram.botapi.util as util
import telegram.botapi.api as api
import telegram.botapi.connector as connector
import telegram.botapi.tests.testdata as testdata
from telegram.botapi.tests.testtools import *


class TestConnector(unittest.TestCase):

    def setUp(self):
        self.original_requests = ORIGINAL_REQUESTS
        self.mocked_requests = sys.modules["requests"]
        self.mocked_requests.reset_mock()

        self.mocked_response = unittest.mock.Mock(spec=ORIGINAL_REQUESTS.Response)
        self.mocked_response.json = json.loads

        self.dummy_api_key = "0000000000"
        self.connector = connector.Connector(self.dummy_api_key)
        self.expected_base_url =    connector.DEFAULT_ENDPOINT_URL + \
                                    self.dummy_api_key + "/"


    def test_get_me(self):
        self.mocked_response.json = lambda: json.loads(testdata.USER_RESPONSE)
        self.mocked_requests.get.return_value = self.mocked_response
        response = self.connector.get_me()

        expected_full_url = api.get_me_url(self.expected_base_url)
        self.mocked_requests.get.assert_called_once_with(   expected_full_url, \
                                                            params={}, \
                                                            timeout=0)

    def test_get_raw_updates(self):
        self.mocked_response.json = lambda: json.loads(testdata.MULTIPLE_UPDATES)
        self.mocked_requests.get.return_value = self.mocked_response
        response = self.connector.get_raw_updates()
        expected_full_url = api.get_updates_url(self.expected_base_url)
        expected_params = { "timeout": connector.DEFAULT_LONGPOLLING_TIMEOUT, \
                            "offset": 0 }
        expected_timeout = connector.DEFAULT_LONGPOLLING_TIMEOUT

        self.mocked_requests.get.assert_called_once_with(   expected_full_url, \
                                                            params=expected_params, \
                                                            timeout=expected_timeout)
        self.assertTrue(isinstance(response, util.JsonObject))
        self.assertEqual(3, len(response.result))
        self.assertTrue(inlist(response.result, \
            lambda x: x.update_id == testdata.MULTIPLE_UPDATES_LAST_ID-2))
        self.assertTrue(inlist(response.result, \
            lambda x: x.update_id == testdata.MULTIPLE_UPDATES_LAST_ID-1))
        self.assertTrue(inlist(response.result, \
            lambda x: x.update_id == testdata.MULTIPLE_UPDATES_LAST_ID))

    def test_get_updates(self):
        self.mocked_response.json = lambda: json.loads(testdata.MULTIPLE_UPDATES)
        self.mocked_requests.get.return_value = self.mocked_response
        updates = self.connector.get_updates()

        self.assertEqual(testdata.MULTIPLE_UPDATES_TEXTS[0], updates[0].text)
        self.assertEqual(testdata.MULTIPLE_UPDATES_TEXTS[-1], updates[-1].text)
        self.assertEqual(testdata.MULTIPLE_UPDATES_LAST_ID, self.connector.last_update_id)

    def test_stream_updates(self):
        self.mocked_response.json = lambda: json.loads(testdata.MULTIPLE_UPDATES)
        self.mocked_requests.get.return_value = self.mocked_response
        first_update = next(self.connector.stream_updates())

        self.assertEqual(testdata.MULTIPLE_UPDATES_TEXTS[0], first_update.text)
        all_updates = take(3, self.connector.stream_updates())
        self.assertEqual(testdata.MULTIPLE_UPDATES_TEXTS[2], all_updates[2].text)

    def test_send_message(self):
        self.mocked_response.json = lambda: json.loads(testdata.MESSAGE_RESPONSE)
        self.mocked_requests.post.return_value = self.mocked_response
        chat_id = 1337
        testmessage = "testmessage"
        response = self.connector.send_message(chat_id, testmessage)
        expected_full_url = api.send_message_url(self.expected_base_url)
        expected_params = { "chat_id": str(chat_id),
                            "text": testmessage}

        self.mocked_requests.post.assert_called_once_with(  expected_full_url, \
                                                            params=expected_params,
                                                            files={})

    def test_send_message_optional_args(self):
        self.mocked_response.json = lambda: json.loads(testdata.MESSAGE_RESPONSE)
        self.mocked_requests.post.return_value = self.mocked_response
        chat_id = 1337
        testmessage = "testmessage"
        optionals = {"disable_web_page_preview": True, \
                    "reply_to_message_id": 42, \
                    "reply_markup": None}
        response = self.connector.send_message(chat_id, testmessage, optionals=optionals)

        expected_full_url = api.send_message_url(self.expected_base_url)
        expected_params = { "chat_id": str(chat_id),
                            "text": testmessage}
        expected_params.update(optionals)
        self.mocked_requests.post.assert_called_once_with(  expected_full_url, \
                                                            params=expected_params,
                                                            files={})

    def test_send_photo_file_name(self):
        self.mocked_response.json = lambda: json.loads(testdata.MESSAGE_RESPONSE)
        self.mocked_requests.post.return_value = self.mocked_response
        chat_id = 1337
        filename = "testphoto.jpg"
        filehandle = unittest.mock.sentinel.file_handle
        mock = unittest.mock.MagicMock(return_value=filehandle)
        with unittest.mock.patch('builtins.open', mock):
            response = self.connector.send_photo(chat_id, file_or_filename=filename)

        expected_full_url = api.send_photo_url(self.expected_base_url)
        expected_params = { "chat_id": str(chat_id) }
        expected_files = {"photo": filehandle}
        self.mocked_requests.post.assert_called_once_with(  expected_full_url, \
                                                            params=expected_params,
                                                            files=expected_files)

    def test_send_photo_file_handle(self):
        self.mocked_response.json = lambda: json.loads(testdata.MESSAGE_RESPONSE)
        self.mocked_requests.post.return_value = self.mocked_response
        chat_id = 1337
        filehandle = unittest.mock.sentinel.file_handle
        mock = unittest.mock.MagicMock(return_value=filehandle)
        with unittest.mock.patch('builtins.open', mock):
            response = self.connector.send_photo(chat_id, file_or_filename=filehandle)

        expected_full_url = api.send_photo_url(self.expected_base_url)
        expected_params = { "chat_id": str(chat_id) }
        expected_files = {"photo": filehandle}
        self.mocked_requests.post.assert_called_once_with(  expected_full_url, \
                                                            params=expected_params,
                                                            files=expected_files)

    def test_send_photo_id(self):
        self.mocked_response.json = lambda: json.loads(testdata.MESSAGE_RESPONSE)
        self.mocked_requests.post.return_value = self.mocked_response
        chat_id = 1337
        photo_id = "deadbeef"
        optionals = {   "caption": "testcaption", \
                        "reply_to_message_id": 42, \
                        "reply_markup": None }
        response = self.connector.send_photo(chat_id, photo_id=photo_id, optionals=optionals)

        expected_full_url = api.send_photo_url(self.expected_base_url)
        expected_params = { "chat_id": str(chat_id), "photo": photo_id }
        expected_params.update(optionals)
        expected_files = {}
        self.mocked_requests.post.assert_called_once_with(  expected_full_url, \
                                                            params=expected_params,
                                                            files=expected_files)
