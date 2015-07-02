
import telegram.botapi.util as util
import telegram.botapi.actions as actions
import telegram.botapi.bot as bot
import telegram.botapi.connector as connector

CONSUME = True
DO_NOT_CONSUME = False

class BotBuilder(object):

    def __init__(self, apikey=None, apikey_file=None):
        key = None
        if not apikey:
            if not apikey_file:
                raise ValueError("Either apikey or apikey_file must be specified")
            else:
                with open(apikey_file, "r") as kf:
                    key = kf.readline()[:-1]
        else:
            key = apikey
        self.bot = bot.TelegramBot(apikey=key)

    def do_when(self, cmd_or_predicate, function, consume):
        matcher = self._get_matcher(cmd_or_predicate)
        self.bot.add_action(matcher, actions.Action(function), consume)
        return self

    def send_message_when(  self, cmd_or_predicate, msg_or_function, \
                            consume=True, optionals={}):
        matcher = self._get_matcher(cmd_or_predicate)
        generator = self._get_generator(msg_or_function, optionals)
        self.bot.add_action(matcher, \
                            actions.SendMessageAction(\
                                generator, \
                                self.bot.connector), \
                            consume)
        return self

    def forward_message_when(   self, cmd_or_predicate, msg_or_function, \
                                consume=True, optionals={}):
        matcher = self._get_matcher(cmd_or_predicate)
        generator = self._get_generator(msg_or_function, optionals)
        self.bot.add_action(matcher, \
                            actions.ForwardMessageAction(\
                                generator, \
                                self.bot.connector), \
                            consume)
        return self

    def send_photo_when(self, cmd_or_predicate, msg_or_function, \
                        is_id=False, consume=True, optionals={}):
        matcher = self._get_matcher(cmd_or_predicate)
        generator = self._get_generator(msg_or_function, optionals)
        self.bot.add_action(matcher, \
                            actions.SendPhotoAction( \
                                generator, \
                                self.bot.connector, \
                                is_id), \
                            consume)
        return self

    def send_audio_when(self, cmd_or_predicate, msg_or_function, \
                        is_id=False, consume=True, optionals={}):
        matcher = self._get_matcher(cmd_or_predicate)
        generator = self._get_generator(msg_or_function, optionals)
        self.bot.add_action(matcher, \
                            actions.SendAudioAction( \
                                generator, \
                                self.bot.connector, \
                                is_id), \
                            consume)
        return self

    def send_document_when( self, cmd_or_predicate, msg_or_function, \
                            is_id=False, consume=True, optionals={}):
        matcher = self._get_matcher(cmd_or_predicate)
        generator = self._get_generator(msg_or_function, optionals)
        self.bot.add_action(matcher, \
                            actions.SendDocumentAction( \
                                generator, \
                                self.bot.connector, \
                                is_id), \
                            consume)
        return self

    def send_sticker_when(  self, cmd_or_predicate, msg_or_function, \
                            is_id=False, consume=True, optionals={}):
        matcher = self._get_matcher(cmd_or_predicate)
        generator = self._get_generator(msg_or_function, optionals)
        self.bot.add_action(matcher, \
                            actions.SendStickerAction( \
                                generator, \
                                self.bot.connector, \
                                is_id), \
                            consume)
        return self

    def send_video_when(self, cmd_or_predicate, msg_or_function, \
                        is_id=False, consume=True, optionals={}):
        matcher = self._get_matcher(cmd_or_predicate)
        generator = self._get_generator(msg_or_function, optionals)
        self.bot.add_action(matcher, \
                            actions.SendVideoAction( \
                                generator, \
                                self.bot.connector, \
                                is_id), \
                            consume)
        return self

    def send_location_when( self, cmd_or_predicate, msg_or_function, \
                            consume=True, optionals={}):
        matcher = self._get_matcher(cmd_or_predicate)
        generator = self._get_generator(msg_or_function, optionals)
        self.bot.add_action(matcher, \
                            actions.SendLocationAction( \
                                generator, \
                                self.bot.connector), \
                            consume)
        return self

    def build(self):
        return self.bot

    def _get_matcher(self, cmd_or_predicate):
        if util.iscallable(cmd_or_predicate):
            return actions.FunctionMatcher(cmd_or_predicate)
        else:
            return actions.CommandMatcher(cmd_or_predicate)

    def _get_generator(self, str_or_function, optionals):
        if util.iscallable(str_or_function):
            return actions.FunctionGenerator(str_or_function, optionals=optionals)
        else:
            return actions.StringGenerator(str_or_function, optionals=optionals)
