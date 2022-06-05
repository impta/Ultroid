# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ فرمان های دردسترس -

• `{i}ftyping <time/in secs>`
    `تایپ فیک.`

• `{i}faudio <time/in secs>`
    `وویس فیک.`

• `{i}fvideo <time/in secs>`
    `ویدیوی فیک.`

• `{i}fgame <time/in secs>`
    `بازی کردنه فیک.`

• `{i}fsticker <time/in secs>`
    `انتخابه استیکره فیک`

• `{i}flocation <time/in secs>`
    `لوکیشن فرستادنه فیک`

• `{i}fcontact <time/in secs>`
    `انتخابه مخاطبه فیک`

• `{i}fround <time/in secs>`
    `ویدیو مسیج فیک`

• `{i}fphoto <time/in secs>`
    `ارسال عکس فیک`

• `{i}fdocument <time/in secs>`
    `ارسال اسناد فیک`
"""
import math
import time

from pyUltroid.functions.admins import ban_time

from . import asyncio, get_string, ultroid_cmd


@ultroid_cmd(
    pattern="f(typing|audio|contact|document|game|location|sticker|photo|round|video)( (.*)|$)"
)
async def _(e):
    act = e.pattern_match.group(1).strip()
    t = e.pattern_match.group(2)
    if act in ["audio", "round", "video"]:
        act = "record-" + act
    if t.isdigit():
        t = int(t)
    elif t.endswith(("s", "h", "d", "m")):
        t = math.ceil((ban_time(e, t)) - time.time())
    else:
        t = 60
    await e.eor(get_string("fka_1").format(str(t)), time=5)
    async with e.client.action(e.chat_id, act):
        await asyncio.sleep(t)
