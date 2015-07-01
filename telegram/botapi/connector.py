
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
        return self._do_get(    api.get_updates_url(self.base_url), \
                                params, \
                                timeout=self.longpolling_timeout)

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

    def get_me(self):
        return self._do_get(api.get_me_url(self.base_url), {})

    def get_user_profile_photos(self, user_id, optionals={}):
        params = {"user_id": str(user_id)}
        params.update(optionals)
        return self._do_get(api.get_user_profile_photos_url(self.base_url), params)

    def forward_message(self, chat_id, from_chat_id, message_id):
        params = self._default_params(chat_id)
        params["from_chat_id"] = from_chat_id
        params["message_id"] = message_id
        return self._do_post(api.forward_message_url(self.base_url), params)

    def send_message(self, chat_id, message, optionals={}):
        params = self._default_params(chat_id, optionals)
        params["text"] = message
        return self._do_post(api.send_message_url(self.base_url), params)

    def send_photo(self, chat_id, file_or_filename=None, photo_id=None, optionals={}):
        return self._do_multipart_post( api.send_photo_url(self.base_url), \
                                        chat_id, "photo", file_or_filename, \
                                        photo_id, optionals)

    def send_audio(self, chat_id, file_or_filename=None, audio_id=None, optionals={}):
        return self._do_multipart_post( api.send_audio_url(self.base_url), \
                                        chat_id, "audio", file_or_filename, \
                                        audio_id, optionals)

    def send_document(self, chat_id, file_or_filename=None, doc_id=None, optionals={}):
        return self._do_multipart_post( api.send_document_url(self.base_url), \
                                        chat_id, "document", file_or_filename, \
                                        doc_id, optionals)

    def send_sticker(self, chat_id, file_or_filename=None, sticker_id=None, optionals={}):
        return self._do_multipart_post( api.send_sticker_url(self.base_url), \
                                        chat_id, "sticker", file_or_filename, \
                                        sticker_id, optionals)

    def send_video(self, chat_id, file_or_filename=None, video_id=None, optionals={}):
        return self._do_multipart_post( api.send_video_url(self.base_url), \
                                        chat_id, "video", file_or_filename, \
                                        video_id, optionals)

    def send_location(self, chat_id, latitude, longitude, optionals={}):
        params = self._default_params(chat_id, optionals)
        params["latitude"] = latitude
        params["longitude"] = longitude
        return self._do_post(api.send_location_url(self.base_url), params)

    def _do_get(self, url, params, timeout=0):
        json_response = requests.get(url, params=params, timeout=timeout).json()
        return util.fromjson(json_response)

    def _do_post(self, url, params, files={}):
        json_response = requests.post(url, params=params, files=files).json()
        return util.fromjson(json_response)

    def _do_multipart_post( self,  url, chat_id, param_name, \
                            file_or_filename=None, file_id=None, \
                            optionals={}):
        fil = util.getfile(file_or_filename)
        multipart_data = util.getmultipart(param_name, fil)
        params = self._default_params(chat_id, optionals)
        params.update(util.getparam(param_name, file_id))
        return self._do_post(url, params, files=multipart_data)

    def _default_params(self, chat_id, extra_params={}):
        params = {"chat_id": str(chat_id)}
        params.update(extra_params)
        return params
