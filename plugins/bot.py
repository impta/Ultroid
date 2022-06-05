# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ فرمان های دردسترس

• `{i}alive` | `{i}alive inline`
    بررسی کنید که آیا ربات شما کار می کند.

• `{i}ping`
    زمان پاسخگویی النلیل را بررسی کنید.

• `{i}update`
    در صورت در دسترس بودن هر گونه به روز رسانی، گزارش تغییرات را مشاهده کنید.

• `{i}cmds`
    مشاهده تمام نام های افزونه ها.

• `{i}restart`
    راه اندازی مجدد ربات.

• `{i}logs (sys)`
    دریافت گزارشای کامل ترمینال.
• `{i}logs carbon`
    دریافت گزارش های سیستمیه کربنی شده.
• `{i}logs heroku`
   دریافت ۱۰۰ خطه اخره گزارش های هیروکو.

• `{i}shutdown`
    خاموش کردن ربات.
"""
import os
import sys
import time
from platform import python_version as pyver
from random import choice

from pyUltroid.version import __version__ as UltVer
from telethon import __version__
from telethon.errors.rpcerrorlist import (
    BotMethodInvalidError,
    ChatSendMediaForbiddenError,
)

from . import HOSTED_ON, LOGS

try:
    from git import Repo
except ImportError:
    LOGS.error("ربات: 'gitpython' ماژول پیدا نشد!")
    Repo = None

from telethon.utils import resolve_bot_file_id

from . import (
    ATRA_COL,
    INLINE_PIC,
    LOGS,
    OWNER_NAME,
    ULTROID_IMAGES,
    Button,
    Carbon,
    Telegraph,
    Var,
    allcmds,
    asst,
    bash,
    call_back,
    callback,
    def_logs,
    eor,
    get_string,
    heroku_logs,
    in_pattern,
    restart,
    shutdown,
    start_time,
    time_formatter,
    udB,
    ultroid_cmd,
    ultroid_version,
    updater,
)

ULTPIC = INLINE_PIC or choice(ULTROID_IMAGES)
buttons = [
    [
        Button.url(get_string("bot_3"), "https://t.me/ElenLiL"),
        Button.url(get_string("bot_4"), "t.me/ElenLiLBoT"),
    ]
]

# Will move to strings
alive_txt = """
The ElenLiL Userbot

  ◍ Version - {}
  ◍ Py-Ultroid - {}
  ◍ Telethon - {}
"""

in_alive = "{}\n\n🌀 <b>ورژن ربات -><b> <code>{}</code>\n🌀 <b>پایتون ربات -></b> <code>{}</code>\n🌀 <b>پایتون -></b> <code>{}</code>\n🌀 <b>آپتایم -></b> <code>{}</code>\n🌀 <b>برنچ -></b> [ {} ]\n\n• <b>جوین @ElenLiLBoT</b>"


@callback("alive")
async def alive(event):
    text = alive_txt.format(ultroid_version, UltVer, __version__)
    await event.answer(text, alert=True)


@ultroid_cmd(
    pattern="alive( (.*)|$)",
)
async def lol(ult):
    match = ult.pattern_match.group(1).strip()
    inline = None
    if match in ["inline", "i"]:
        try:
            res = await ult.client.inline_query(asst.me.username, "alive")
            return await res[0].click(ult.chat_id)
        except BotMethodInvalidError:
            pass
        except BaseException as er:
            LOGS.exception(er)
        inline = True
    pic = udB.get_key("ALIVE_PIC")
    if isinstance(pic, list):
        pic = choice(pic)
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get_key("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f" `[{y}]({rep})` "
    if inline:
        kk = f"<a href={rep}>{y}</a>"
        parse = "html"
        als = in_alive.format(
            header,
            ultroid_version + f" [{HOSTED_ON}]",
            UltVer,
            pyver(),
            uptime,
            kk,
        )
        if _e := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("🌀", _e)
    else:
        parse = "md"
        als = (get_string("alive_1")).format(
            header,
            OWNER_NAME,
            ultroid_version + f" [{HOSTED_ON}]",
            UltVer,
            uptime,
            pyver(),
            __version__,
            kk,
        )
        if a := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("✵", a)
    if pic:
        try:
            await ult.reply(
                als,
                file=pic,
                parse_mode=parse,
                link_preview=False,
                buttons=buttons if inline else None,
            )
            return await ult.try_delete()
        except ChatSendMediaForbiddenError:
            pass
        except BaseException as er:
            LOGS.exception(er)
            try:
                await ult.reply(file=pic)
                await ult.reply(
                    als,
                    parse_mode=parse,
                    buttons=buttons if inline else None,
                    link_preview=False,
                )
                return await ult.try_delete()
            except BaseException as er:
                LOGS.exception(er)
    await eor(
        ult,
        als,
        parse_mode=parse,
        link_preview=False,
        buttons=buttons if inline else None,
    )


@ultroid_cmd(pattern="ping$", chats=[], type=["official", "assistant"])
async def _(event):
    start = time.time()
    x = await event.eor("Pong !")
    end = round((time.time() - start) * 1000)
    uptime = time_formatter((time.time() - start_time) * 1000)
    await x.edit(get_string("ping").format(end, uptime))


@ultroid_cmd(
    pattern="cmds$",
)
async def cmds(event):
    await allcmds(event, Telegraph)


heroku_api = Var.HEROKU_API


@ultroid_cmd(
    pattern="restart$",
    fullsudo=True,
)
async def restartbt(ult):
    ok = await ult.eor(get_string("bot_5"))
    call_back()
    who = "bot" if ult.client._bot else "user"
    udB.set_key("_RESTART", f"{who}_{ult.chat_id}_{ok.id}")
    if heroku_api:
        return await restart(ok)
    await bash("git pull && pip3 install -r requirements.txt")
    if len(sys.argv) > 1:
        os.execl(sys.executable, sys.executable, "main.py")
    else:
        os.execl(sys.executable, sys.executable, "-m", "pyUltroid")


@ultroid_cmd(
    pattern="shutdown$",
    fullsudo=True,
)
async def shutdownbot(ult):
    await shutdown(ult)


@ultroid_cmd(
    pattern="logs( (.*)|$)",
    chats=[],
)
async def _(event):
    opt = event.pattern_match.group(1).strip()
    file = f"ultroid{sys.argv[-1]}.log" if len(sys.argv) > 1 else "ultroid.log"
    if opt == "heroku":
        await heroku_logs(event)
    elif opt == "carbon" and Carbon:
        event = await event.eor(get_string("com_1"))
        code = open(file, "r").read()[-2500:]
        file = await Carbon(
            file_name="ultroid-logs",
            code=code,
            backgroundColor=choice(ATRA_COL),
        )
        await event.reply("**گزارشات ربات.**", file=file)
    elif opt == "open":
        file = open("ultroid.log", "r").read()[-4000:]
        return await event.eor(f"`{file}`")
    else:
        await def_logs(event, file)
    await event.try_delete()


@in_pattern("alive", owner=True)
async def inline_alive(ult):
    pic = udB.get_key("ALIVE_PIC")
    if isinstance(pic, list):
        pic = choice(pic)
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get_key("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f"<a href={rep}>{y}</a>"
    als = in_alive.format(
        header,
        ultroid_version + f" [{HOSTED_ON}]",
        UltVer,
        pyver(),
        uptime,
        kk,
    )
    if _e := udB.get_key("ALIVE_EMOJI"):
        als = als.replace("🌀", _e)
    builder = ult.builder
    if pic:
        try:
            if ".jpg" in pic:
                results = [
                    await builder.photo(
                        pic, text=als, parse_mode="html", buttons=buttons
                    )
                ]
            else:
                _pic = resolve_bot_file_id(pic)
                if _pic:
                    pic = _pic
                    buttons.insert(
                        0, [Button.inline(get_string("bot_2"), data="alive")]
                    )
                results = [
                    await builder.document(
                        pic,
                        title="Inline Alive",
                        description="@ElenLiLBoT",
                        parse_mode="html",
                        buttons=buttons,
                    )
                ]
            return await ult.answer(results)
        except BaseException as er:
            LOGS.info(er)
    result = [
        await builder.article(
            "Alive", text=als, parse_mode="html", link_preview=False, buttons=buttons
        )
    ]
    await ult.answer(result)


@ultroid_cmd(pattern="update( (.*)|$)")
async def _(e):
    xx = await e.eor(get_string("upd_1"))
    if HOSTED_ON == "heroku" or (
        e.pattern_match.group(1).strip()
        and (
            "fast" in e.pattern_match.group(1).strip()
            or "soft" in e.pattern_match.group(1).strip()
        )
    ):
        await bash("git pull -f && pip3 install -r requirements.txt")
        call_back()
        await xx.edit(get_string("upd_7"))
        os.execl(sys.executable, "python3", "-m", "pyUltroid")
        return
    m = await updater()
    branch = (Repo.init()).active_branch
    if m:
        x = await asst.send_file(
            udB.get_key("LOG_CHANNEL"),
            ULTPIC,
            caption="• **آپدیت دردسترسه** •",
            force_document=False,
            buttons=Button.inline("گزارشات تغییرات", data="changes"),
        )
        Link = x.message_link
        await xx.edit(
            f'<strong><a href="{Link}">[ChangeLogs]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )
    else:
        await xx.edit(
            f'<code>رباتت هس </code><strong>up-to-date</strong><code> با </code><strong><a href="https://t.me/ElenLiLBoT">[{branch}]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )


@callback("updtavail", owner=True)
async def updava(event):
    await event.delete()
    await asst.send_file(
        udB.get_key("LOG_CHANNEL"),
        ULTPIC,
        caption="• **آپدیت دردسترسه** •",
        force_document=False,
        buttons=Button.inline("Changelogs", data="changes"),
    )
