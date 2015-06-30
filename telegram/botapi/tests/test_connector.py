import unittest
import unittest.mock
import sys

import requests

sys.modules["requests"] = unittest.mock.Mock(spec=requests)
import telegram.botapi.connector as connector

class TestConnector(unittest.TestCase):

    def setUp(self):
        self.requests_mock = sys.modules["requests"]
        self.dummy_api_key = "0000000000"
        self.connector = connector.Connector(self.dummy_api_key)
        self.updates_response = "{\"ok\": true}"

    def test_get_updates(self):
        self.requests_mock.get.return_value = ""
