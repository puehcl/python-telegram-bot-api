#!/usr/bin/python3

import os

import telegram.botapi.botbuilder as botbuilder


def match_all(update):
    return True

def logger(update):
    print("got update:", update)

def get_filehandle(update):
    return open(os.path.join("files", "bubblegum.png"), "rb")

if __name__ == "__main__":
    botbuilder.BotBuilder(apikey_file="api_key.txt") \
        .do_when(match_all, logger, botbuilder.DO_NOT_CONSUME) \
        .send_sticker_when("bubblegum", get_filehandle) \
        .send_sticker_when("gunter", os.path.join("files", "gunter.png")) \
        .build().start()
