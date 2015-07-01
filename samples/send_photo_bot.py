#!/usr/bin/python3

import telegram.botapi.botbuilder as botbuilder


def match_all(update):
    return True

def logger(update):
    print("got update:", update)

def get_filehandle(update):
    return open("cat1.jpeg", "rb")

def get_filehandle_and_caption(update):
    print("cat1 with caption")
    optionals = {"caption": "omg catz!"}
    return open("cat1.jpeg", "rb"), optionals

if __name__ == "__main__":
    optionals = {"caption": "so sweet!!!"}

    botbuilder.BotBuilder(apikey_file="api_key.txt") \
        .do_when(match_all, logger, botbuilder.DO_NOT_CONSUME) \
        .send_photo_when("cat1caption", get_filehandle_and_caption, ) \
        .send_photo_when("cat2caption", "cat2.jpeg", optionals=optionals) \
        .send_photo_when("cat1", get_filehandle, botbuilder.CONSUME) \
        .send_photo_when("cat2", "cat2.jpeg") \
        .build().start()
