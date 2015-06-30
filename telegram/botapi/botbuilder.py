
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
        transformer = bot.FunctionTransformer(function)
        self.bot.add_action(matcher, bot.Action(transformer), consume)
        return self

    def send_message_when(self, cmd_or_predicate, msg_or_function, consume):
        matcher = self._get_matcher(cmd_or_predicate)
        transformer = self._get_transformer(msg_or_function)
        self.bot.add_action(matcher, bot.SendMessageAction(transformer, self.bot.connector), consume)
        return self

    def build(self):
        return self.bot

    def _get_matcher(self, cmd_or_predicate):
        if hasattr(cmd_or_predicate, "__call__"):
            return bot.FunctionMatcher(cmd_or_predicate)
        else:
            return bot.CommandMatcher(cmd_or_predicate)

    def _get_transformer(self, str_or_function):
        if hasattr(str_or_function, "__call__"):
            return bot.FunctionTransformer(str_or_function)
        else:
            return bot.StringTransformer(str_or_function)
