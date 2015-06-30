
import requests

import telegram.botapi.util as util

DEFAULT_ENDPOINT_URL = "https://api.telegram.org/bot"

class Connector(object):
    default_longpolling_timeout = 120

    get_updates_method = "getUpdates"
    send_message_method = "sendMessage"

    def __init__(self, api_key, endpoint_url=DEFAULT_ENDPOINT_URL):
        self.last_update_id = 0
        self.longpolling_timeout = Connector.default_longpolling_timeout
        self.base_url = endpoint_url + api_key + "/"
        self.get_updates_url = self.base_url + Connector.get_updates_method
        self.send_message_url = self.base_url + Connector.send_message_method

    def get_raw_updates(self):
        params = {"timeout": self.longpolling_timeout}
        response = requests.get(self.get_updates_url, \
                                params=params, \
                                timeout=self.longpolling_timeout)
        print(response.text)
        return util.fromjson(response.text)

    def get_updates(self):
        params = {  "timeout": self.longpolling_timeout, \
                    "offset": (self.last_update_id + 1) }
        response = requests.get(self.get_updates_url, \
                                params=params, \
                                timeout=self.longpolling_timeout)
        jobj = util.fromjson(response.text)
        if not jobj.ok:
            pass
            #TODO: raise
        if not jobj.result or len(jobj.result) == 0:
            return []
        updates = sorted(jobj.result, key=lambda update: update.update_id)
        self.last_update_id = updates[-1].update_id
        return [update.message for update in updates]

    def stream_updates(self):
        while True:
            for update in self.get_updates():
                yield update

    def send_message(self, chat_id, message):
        params = {"chat_id": str(chat_id), "text": message}
        response = requests.post(self.send_message_url, params=params)
        return util.fromjson(response.text)
