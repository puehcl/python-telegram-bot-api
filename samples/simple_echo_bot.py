#!/usr/bin/python3

import telegram.botapi.botbuilder as botbuilder

def match_all(update):
    return True

def match_contains(update):
    return "sweet" in update.text.lower()

def logger(update):
    print("got update:", update)

def message_generator(update):
    return "awesome"

def dude(update):
    return "dude"

if __name__ == "__main__":
    botbuilder.BotBuilder(apikey_file="api_key.txt") \
        .do_when(match_all, logger, botbuilder.DO_NOT_CONSUME) \
        .send_message_when(match_contains, dude, botbuilder.CONSUME) \
        .send_message_when(match_all, message_generator, botbuilder.CONSUME) \
        .build().start()
