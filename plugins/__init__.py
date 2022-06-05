# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.


import asyncio
import os
import time
from random import choice

import requests
from pyUltroid import *
from pyUltroid._misc._assistant import asst_cmd, callback, in_pattern
from pyUltroid._misc._decorators import ultroid_cmd
from pyUltroid._misc._wrappers import eod, eor
from pyUltroid.dB import DEVLIST, ULTROID_IMAGES
from pyUltroid.functions.helper import *
from pyUltroid.functions.info import *
from pyUltroid.functions.misc import *
from pyUltroid.functions.tools import *
from pyUltroid.version import __version__, ultroid_version
from telethon import Button, events
from telethon.tl import functions, types

from strings import get_string

Redis = udB.get_key
con = TgConverter
quotly = Quotly()
OWNER_NAME = ultroid_bot.full_name
OWNER_ID = ultroid_bot.uid

LOG_CHANNEL = udB.get_key("LOG_CHANNEL")

INLINE_PIC = udB.get_key("INLINE_PIC")

if INLINE_PIC is None:
    INLINE_PIC = choice(ULTROID_IMAGES)
elif INLINE_PIC == False:
    INLINE_PIC = None

Telegraph = telegraph_client()

List = []
Dict = {}
N = 0

STUFF = {}

# Chats, which needs to be ignore for some cases
# Considerably, there can be many
# Feel Free to Add Any other...

NOSPAM_CHAT = [
    -1001327032795,  # UltroidSupport
    -1001387666944,  # PyrogramChat
    -1001109500936,  # TelethonChat
    -1001050982793,  # Python
    -1001256902287,  # DurovsChat
    -1001473548283,  # SharingUserbot
]

KANGING_STR = [
    "استفاده از Witchery برای چسباندن این استیکر...",
    "سرقت ادبی هه...",
    "اضافه کردنه این استیکر به پکه من ...",
    "چسباندن این استیکر...",
    "هی این استیکره جذابیه\nحواست باشه اسکی نرم!؟",
    "هه استیکرتو دزدیدم..",
    "اینجارو باش (☉｡☉)!→\nقیافت اینجوری میشه وقتی استیکرتو بدزدم",
    "بلا بلا بلا، با اضافه کردنه این استیکر، پکم خفن میشه",
    "زندونی کردنه این استیکر...",
    "من درحاله دزدیدنه این استیکر... ",
]

ATRA_COL = [
    "DarkCyan",
    "DeepSkyBlue",
    "DarkTurquoise",
    "Cyan",
    "LightSkyBlue",
    "Turquoise",
    "MediumVioletRed",
    "Aquamarine",
    "Lightcyan",
    "Azure",
    "Moccasin",
    "PowderBlue",
]
