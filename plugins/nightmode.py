# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ فرمان های دردسترس -

در شب، اجازه ارسال پیام را در همه گروه‌هایی که از طریق «{i}addnight» اضافه کرده‌اید، غیرفعال می‌کند.
 و صبح خودکار را روشن کنید

• `{i}addnm`
   Add NightMode
   برای حالته شبخ اتوماتیک.

• `{i}remnm`
   Remove NightMode
   برای حذف حالت شبه اتوماتیک

• `{i}listnm`
   List NightMode
   لیست تمام گروه هایی ک حالته شب در ان ها فعاله.

• `{i}nmtime <close hour> <close min> <open hour> <open min>`
   NightMode Time
   تو حالته پیشفرض بسته میشه تو ساعته 00:00 , باز میشه تو ساعته 07:00
   از قالب ۲۴ ساعته استفاده کنید
   Ex- `nmtime 01 00 06 30`
"""

from . import LOGS

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
except ImportError:
    LOGS.error("nightmode: 'apscheduler' not Installed!")
    AsyncIOScheduler = None

from pyUltroid.dB.night_db import *
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights

from . import get_string, udB, ultroid_bot, ultroid_cmd


@ultroid_cmd(pattern="nmtime( (.*)|$)")
async def set_time(e):
    if not e.pattern_match.group(1).strip():
        return await e.eor(get_string("nightm_1"))
    try:
        ok = e.text.split(maxsplit=1)[1].split()
        if len(ok) != 4:
            return await e.eor(get_string("nightm_1"))
        tm = [int(x) for x in ok]
        udB.set_key("NIGHT_TIME", str(tm))
        await e.eor(get_string("nightm_2"))
    except BaseException:
        await e.eor(get_string("nightm_1"))


@ultroid_cmd(pattern="addnm( (.*)|$)")
async def add_grp(e):
    pat = e.pattern_match.group(1).strip()
    if pat:
        try:
            add_night((await ultroid_bot.get_entity(pat)).id)
            return await e.eor(f"حله, اضافه شد {pat} ب حالته شب.")
        except BaseException:
            return await e.eor(get_string("nightm_5"), time=5)
    add_night(e.chat_id)
    await e.eor(get_string("nightm_3"))


@ultroid_cmd(pattern="remnm( (.*)|$)")
async def rem_grp(e):
    pat = e.pattern_match.group(1).strip()
    if pat:
        try:
            rem_night((await ultroid_bot.get_entity(pat)).id)
            return await e.eor(f"حله, حذف شد {pat} از حالته شب.")
        except BaseException:
            return await e.eor(get_string("nightm_5"), time=5)
    rem_night(e.chat_id)
    await e.eor(get_string("nightm_4"))


@ultroid_cmd(pattern="listnm$")
async def rem_grp(e):
    chats = night_grps()
    name = "جالته شبه گروه هستش-:\n\n"
    برای x در گپ ها:
        try:
            ok = await ultroid_bot.get_entity(x)
            name += "@" + ok.username if ok.username else ok.title
        except BaseException:
            name += str(x)
    await e.eor(name)


async def open_grp():
    chats = night_grps()
    for chat in chats:
        try:
            await ultroid_bot(
                EditChatDefaultBannedRightsRequest(
                    chat,
                    banned_rights=ChatBannedRights(
                        until_date=None,
                        send_messages=False,
                        send_media=False,
                        send_stickers=False,
                        send_gifs=False,
                        send_games=False,
                        send_inline=False,
                        send_polls=False,
                    ),
                )
            )
            await ultroid_bot.send_message(chat, "**حالته شب خاموشه**\n\nگروه باز شد 🥳.")
        except Exception as er:
            LOGS.info(er)


async def close_grp():
    chats = night_grps()
    h1, m1, h2, m2 = 0, 0, 7, 0
    if udB.get_key("NIGHT_TIME"):
        h1, m1, h2, m2 = eval(udB.get_key("NIGHT_TIME"))
    for chat in chats:
        try:
            await ultroid_bot(
                EditChatDefaultBannedRightsRequest(
                    chat,
                    banned_rights=ChatBannedRights(
                        until_date=None,
                        send_messages=True,
                    ),
                )
            )
            await ultroid_bot.send_message(
                chat, f"**حالته شبه : گروه بسته شد**\n\nGroup Will Open At `{h2}:{m2}`"
            )
        except Exception as er:
            LOGS.info(er)


if AsyncIOScheduler and night_grps():
    try:
        h1, m1, h2, m2 = 0, 0, 7, 0
        if udB.get_key("NIGHT_TIME"):
            h1, m1, h2, m2 = eval(udB.get_key("NIGHT_TIME"))
        sch = AsyncIOScheduler()
        sch.add_job(close_grp, trigger="cron", hour=h1, minute=m1)
        sch.add_job(open_grp, trigger="cron", hour=h2, minute=m2)
        sch.start()
    except Exception as er:
        LOGS.info(er)
