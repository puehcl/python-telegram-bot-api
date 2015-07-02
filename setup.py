#!/usr/bin/env python3

from distutils.core import setup

setup(  name            = "telegram-bot-api",
        version         = "0.2",
        description     = "A python wrapper and bot builder for the Telegram Bot API",
        url             = "https://github.com/puehcl/python-telegram-bot-api",
        author          = "Clemens Puehringer",
        author_email    = "misc-telegramapi@pueh.at",
        py_modules      = [ "telegram.botapi.util", \
                            "telegram.botapi.api", \
                            "telegram.botapi.actions", \
                            "telegram.botapi.connector", \
                            "telegram.botapi.bot", \
                            "telegram.botapi.botbuilder"],

        keywords        = [ "telegram", \
                            "bot", \
                            "api", \
                            "builder"],

        classifiers     = [ "Development Status :: 4 - Beta",
                            "Intended Audience :: Developers",
                            "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
                            "Operating System :: OS Independent",
                            "Topic :: Communications :: Chat",
                            "Topic :: Internet",
                            "Programming Language :: Python :: 3 :: Only",
                            "Programming Language :: Python :: 3",
                            "Programming Language :: Python :: 3.4"]
    )
