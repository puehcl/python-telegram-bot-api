#!/usr/bin/env python3

from distutils.core import setup

setup(name="Telegram Bot API",
    version="0.1",
    description="A python framework for the Telegram Bot API",
    author="Clemens Puehringer",
    author_email="misc-telegramapi@pueh.at",
    py_modules=   [ "telegram.botapi.util", \
                    "telegram.botapi.connector", \
                    "telegram.botapi.bot", \
                    "telegram.botapi.botbuilder" ],
    )
