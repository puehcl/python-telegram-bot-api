#!/usr/bin/python3

import os

import telegram.botapi.botbuilder as botbuilder


def match_all(update):
    return True

def logger(update):
    print("got update:", update)

def get_filehandle(update):
    return open(os.path.join("files", "ACDC_back_in_black_sample.ogg"), "rb")

if __name__ == "__main__":
    botbuilder.BotBuilder(apikey_file="api_key.txt") \
        .do_when(match_all, logger, botbuilder.DO_NOT_CONSUME) \
        .send_audio_when("bib", get_filehandle) \
        .send_audio_when("anotherday", os.path.join("files", "another_day_in_paradise_sample.ogg")) \
        .build().start()
