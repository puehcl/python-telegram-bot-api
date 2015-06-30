import math

import telegram.botapi.connector as connector
import telegram.botapi.util as util

class UpdateMatcher(object):
    def matches(self, update):
        pass

class FunctionMatcher(UpdateMatcher):
    def __init__(self, function):
        self.function = function
    def matches(self, update):
        return self.function(update)

class CommandMatcher(UpdateMatcher):
    def __init__(self, commandstr):
        self.commandstr = str(commandstr)
    def matches(self, update):
        if update.text:
            return update.text.lower().startswith("/" + self.commandstr)
        return False

class Transformer(object):
    def transform(self, update):
        pass

class StringTransformer(object):
    def __init__(self, obj):
        self.obj = obj
    def transform(self, update):
        return str(self.obj)

class FunctionTransformer(object):
    def __init__(self, function):
        self.function = function
    def transform(self, update):
        return self.function(update)

class Action(object):
    def __init__(self, transformer):
        self.transformer = transformer
    def execute(self, update):
        return self.transformer.transform(update)

class SendAction(Action):
    def __init__(self, transformer, connector):
        super().__init__(transformer)
        self.connector = connector
    def execute(self, update):
        return None

class SendMessageAction(SendAction):
    def __init__(self, transformer, connector):
        super().__init__(transformer, connector)
    def execute(self, update):
        message = self.transformer.transform(update)
        return self.connector.send_message(update.chat.id, message)

class TelegramBot(object):

    def __init__(self, apikey=None, connector_=None):
        if not connector_:
            if not apikey:
                raise
            self.connector = connector.Connector(apikey)
        else:
            self.connector = connector_
        self.actions = []

    def add_action(self, matcher, action, consume=True):
            self.actions.append((matcher, action, consume))

    def start(self):
        for update in self.connector.stream_updates():
            self._execute_actions(update)

    def _execute_actions(self, update):
        for (matcher, action, consume) in self.actions:
            if matcher.matches(update):
                result = action.execute(update)
                print(result)
                if consume:
                    return
