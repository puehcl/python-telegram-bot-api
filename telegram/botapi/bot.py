import math

import telegram.botapi.connector as connector
import telegram.botapi.util as util



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
