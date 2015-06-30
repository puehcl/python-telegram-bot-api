
import requests

import telegram.botapi.util as util
import telegram.botapi.api as api

DEFAULT_ENDPOINT_URL = "https://api.telegram.org/bot"
DEFAULT_LONGPOLLING_TIMEOUT = 120

class Connector(object):

    def __init__(self, api_key, endpoint_url=DEFAULT_ENDPOINT_URL):
        self.last_update_id = -1
        self.longpolling_timeout = DEFAULT_LONGPOLLING_TIMEOUT
        self.base_url = endpoint_url + api_key + "/"

    def get_raw_updates(self):
        params = {  "timeout": self.longpolling_timeout, \
                    "offset": (self.last_update_id + 1) }
        json_response = requests.get(   api.get_updates_url(self.base_url), \
                                        params=params, \
                                        timeout=self.longpolling_timeout).json()
        return util.fromjson(json_response)

    def get_updates(self):
        jobj = self.get_raw_updates()
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
        json_response = requests.post(  api.send_message_url(self.base_url), \
                                        params=params).json()
        return util.fromjson(json_response)
