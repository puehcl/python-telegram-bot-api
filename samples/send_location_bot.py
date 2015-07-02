#!/usr/bin/python3

import random

import telegram.botapi.botbuilder as botbuilder


def match_all(update):
    return True

def logger(update):
    print("got update:", update)

def get_random_location(update):
    latitude = get_random_latitude()
    longitude = get_random_longitude()
    return latitude, longitude

def get_random_latitude():
    return random.randrange(-90, 90)

def get_random_longitude():
    return random.randrange(-180, 180)

if __name__ == "__main__":
    botbuilder.BotBuilder(apikey_file="api_key.txt") \
        .do_when(match_all, logger, botbuilder.DO_NOT_CONSUME) \
        .send_location_when("location", get_random_location) \
        .send_location_when("tuple", (20,50)) \
        .build().start()
