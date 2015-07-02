#!/usr/bin/python3

import os

import telegram.botapi.botbuilder as botbuilder


def match_all(update):
    return True

def logger(update):
    print("got update:", update)

def get_filehandle(update):
    return open(os.path.join("files", "sample1.odt"), "rb")

if __name__ == "__main__":
    botbuilder.BotBuilder(apikey_file="api_key.txt") \
        .do_when(match_all, logger, botbuilder.DO_NOT_CONSUME) \
        .send_document_when("doc1", get_filehandle) \
        .send_document_when("doc2", os.path.join("files", "sample2.ods")) \
        .build().start()
