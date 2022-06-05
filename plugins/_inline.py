# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import re
import time
from datetime import datetime
from os import remove

from git import Repo
from pyUltroid._misc._assistant import callback, in_pattern
from pyUltroid.dB._core import HELP, LIST
from pyUltroid.functions.helper import gen_chlog, time_formatter, updater
from pyUltroid.functions.misc import split_list
from telethon import Button
from telethon.tl.types import InputWebDocument, Message
from telethon.utils import resolve_bot_file_id

from . import HNDLR, INLINE_PIC, LOGS, OWNER_NAME, asst, get_string, start_time, udB
from ._help import _main_help_menu

# ================================================#

TLINK = INLINE_PIC or "https://telegra.ph/file/74d6259983e0642923fdb.jpg"
helps = get_string("inline_1")

add_ons = udB.get_key("ADDONS")

if add_ons is not False:
    zhelps = get_string("inline_2")
else:
    zhelps = get_string("inline_3")

PLUGINS = HELP.get("Official", [])
ADDONS = HELP.get("Addons", [])
upage = 0
# ============================================#

# --------------------BUTTONS--------------------#

SUP_BUTTONS = [
    [
        Button.url("• Creator •", url="https://t.me/ElenLiL"),
        Button.url("• Portal •", url="t.me/ElenLiLBoT"),
    ],
]

# --------------------BUTTONS--------------------#


@in_pattern(owner=True, func=lambda x: not x.text)
async def inline_alive(o):
    MSG = "• **ElenLiL Userbot •**"
    WEB0 = InputWebDocument(
        "https://telegra.ph/file/0cc0d78edd99ee816b992.jpg", 0, "image/jpg", []
    )
    RES = [
        await o.builder.article(
            type="photo",
            text=MSG,
            include_media=True,
            buttons=SUP_BUTTONS,
            title="ElenLiL Userbot",
            description="Userbot | Telethon",
            url=TLINK,
            thumb=WEB0,
            content=InputWebDocument(TLINK, 0, "image/jpg", []),
        )
    ]
    await o.answer(
        RES,
        private=True,
        cache_time=300,
        switch_pm="👥 ElenLiL PORTAL",
        switch_pm_param="start",
    )


@in_pattern("ultd", owner=True)
async def inline_handler(event):
    z = []
    for x in LIST.values():
        z.extend(x)
    text = get_string("inline_4").format(
        OWNER_NAME,
        len(HELP.get("Official", [])),
        len(HELP.get("Addons", [])),
        len(z),
    )
    if INLINE_PIC:
        result = await event.builder.photo(
            file=INLINE_PIC,
            link_preview=False,
            text=text,
            buttons=_main_help_menu,
        )
    else:
        result = await event.builder.article(
            title="ElenLiL Help Menu", text=text, buttons=_main_help_menu
        )
    await event.answer([result], private=True, cache_time=300, gallery=True)


@in_pattern("pasta", owner=True)
async def _(event):
    ok = event.text.split("-")[1]
    link = "https://spaceb.in/" + ok
    raw = f"https://spaceb.in/api/v1/documents/{ok}/raw"
    result = await event.builder.article(
        title="Paste",
        text="Pasted to Spacebin 🌌",
        buttons=[
            [
                Button.url("SpaceBin", url=link),
                Button.url("Raw", url=raw),
            ],
        ],
    )
    await event.answer([result])


@callback("ownr", owner=True)
async def setting(event):
    z = []
    for x in LIST.values():
        z.extend(x)
    await event.edit(
        get_string("inline_4").format(
            OWNER_NAME,
            len(HELP.get("Official", [])),
            len(HELP.get("Addons", [])),
            len(z),
        ),
        file=INLINE_PIC,
        link_preview=False,
        buttons=[
            [
                Button.inline("•پینگ•", data="pkng"),
                Button.inline("•آپتایم•", data="upp"),
            ],
            [
                Button.inline("•آمار•", data="alive"),
                Button.inline("•آپدیت•", data="doupdate"),
            ],
            [Button.inline("« بازگشت", data="open")],
        ],
    )


_strings = {"Official": helps, "Addons": zhelps, "VCBot": get_string("inline_6")}


@callback(re.compile("uh_(.*)"), owner=True)
async def help_func(ult):
    key, count = ult.data_match.group(1).decode("utf-8").split("_")
    if key == "VCBot" and HELP.get("VCBot") is None:
        return await ult.answer(get_string("help_12"), alert=True)
    elif key == "Addons" and HELP.get("Addons") is None:
        return await ult.answer(get_string("help_13").format(HNDLR), alert=True)
    if "|" in count:
        _, count = count.split("|")
    count = 0 if not count else int(count)
    text = _strings.get(key, "").format(OWNER_NAME, len(HELP.get(key)))
    await ult.edit(
        text, file=INLINE_PIC, buttons=page_num(count, key), link_preview=False
    )


@callback(re.compile("uplugin_(.*)"), owner=True)
async def uptd_plugin(event):
    key, file = event.data_match.group(1).decode("utf-8").split("_")
    index = None
    if "|" in file:
        file, index = file.split("|")
    key_ = HELP.get(key, [])
    hel_p = f"اسم افزونه - `{file}`\n"
    help_ = ""
    try:
        for i in key_[file]:
            help_ += i
    except BaseException:
        if file in LIST:
            help_ = get_string("help_11").format(file)
            for d in LIST[file]:
                help_ += HNDLR + d
                help_ += "\n"
    if not help_:
        help_ = f"{file} هیچ راهنمایی نداره!"
    help_ += "\n© @ElenLiL"
    buttons = []
    if INLINE_PIC:
        data = f"sndplug_{key}_{file}"
        if index is not None:
            data += f"|{index}"
        buttons.append(
            [
                Button.inline(
                    "« ارسال افزونه »",
                    data=data,
                )
            ]
        )
    data = f"uh_{key}_"
    if index is not None:
        data += f"|{index}"
    buttons.append(
        [
            Button.inline("« بازگشت", data=data),
        ]
    )
    try:
        await event.edit(help_, buttons=buttons)
    except Exception as er:
        LOGS.exception(er)
        help = f"انجامش بده `{HNDLR}راهنما {key}` برای دریافت لیست فرمان ها"
        await event.edit(help, buttons=buttons)


@callback(data="doupdate", owner=True)
async def _(event):
    if not await updater():
        return await event.answer(get_string("inline_9"), cache_time=0, alert=True)
    if not INLINE_PIC:
        return await event.answer(f"Do '{HNDLR}update' to update..")
    repo = Repo.init()
    changelog, tl_chnglog = await gen_chlog(
        repo, f"HEAD..upstream/{repo.active_branch}"
    )
    changelog_str = changelog + "\n\n" + get_string("inline_8")
    if len(changelog_str) > 1024:
        await event.edit(get_string("upd_4"))
        with open("ultroid_updates.txt", "w+") as file:
            file.write(tl_chnglog)
        await event.edit(
            get_string("upd_5"),
            file="ultroid_updates.txt",
            buttons=[
                [Button.inline("• بروز رسانی •", data="updatenow")],
                [Button.inline("« بازگشت", data="ownr")],
            ],
        )
        remove("ultroid_updates.txt")
    else:
        await event.edit(
            changelog_str,
            buttons=[
                [Button.inline("بروز رسانی", data="updatenow")],
                [Button.inline("« بازگشت", data="ownr")],
            ],
            parse_mode="html",
        )


@callback(data="pkng", owner=True)
async def _(event):
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds
    pin = f"🌋پینگ = {ms} میکرو ثانیه"
    await event.answer(pin, cache_time=0, alert=True)


@callback(data="upp", owner=True)
async def _(event):
    uptime = time_formatter((time.time() - start_time) * 1000)
    pin = f"🙋آپتایم = {uptime}"
    await event.answer(pin, cache_time=0, alert=True)


@callback(data="inlone", owner=True)
async def _(e):
    button = [
        [
            Button.switch_inline(
                "برنامه های پلی استور",
                query="app telegram",
                same_peer=True,
            ),
            Button.switch_inline(
                "برنامه های مود شده",
                query="mods minecraft",
                same_peer=True,
            ),
        ],
        [
            Button.switch_inline(
                "جستجو در گوگل",
                query="go ElenLiL",
                same_peer=True,
            ),
            Button.switch_inline(
                "جستجو در اکس دی اِی",
                query="xda telegram",
                same_peer=True,
            ),
        ],
        [
            Button.switch_inline(
                "نجوا",
                query="wspr @username سلام🎉",
                same_peer=True,
            ),
            Button.switch_inline(
                "یوتوب دانلودر",
                query="yt Ed Sheeran Perfect",
                same_peer=True,
            ),
        ],
        [
            Button.switch_inline(
                "پیستون ایوال",
                query="run javascript console.log('Hello ElenLiL')",
                same_peer=True,
            ),
            Button.switch_inline(
                "روباه نارنجی🦊",
                query="ofox beryllium",
                same_peer=True,
            ),
        ],
        [
            Button.switch_inline(
                "کاربر توییتر", query="twitter ElenLiL", same_peer=True
            ),
            Button.switch_inline(
                "جستجوی کو", query="koo @ElenLiL", same_peer=True
            ),
        ],
        [
            Button.switch_inline(
                "جستجوی اف دروید", query="fdroid telegram", same_peer=True
            ),
            Button.switch_inline("جستجوی ساون", query="saavn", same_peer=True),
        ],
        [
            Button.switch_inline("جستجوی تلگرام", query="tl", same_peer=True),
            Button.switch_inline("فید های گیت هاب", query="gh", same_peer=True),
        ],
        [Button.switch_inline("اومگ اوبونتو", query="omgu cutefish", same_peer=True)],
        [
            Button.inline(
                "« بازگشت",
                data="open",
            ),
        ],
    ]
    await e.edit(buttons=button, link_preview=False)


@callback(data="open", owner=True)
async def opner(event):
    z = []
    for x in LIST.values():
        z.extend(x)
    await event.edit(
        get_string("inline_4").format(
            OWNER_NAME,
            len(HELP.get("Official", [])),
            len(HELP.get("Addons", [])),
            len(z),
        ),
        buttons=_main_help_menu,
        link_preview=False,
    )


@callback(data="close", owner=True)
async def on_plug_in_callback_query_handler(event):
    await event.edit(
        get_string("inline_5"),
        buttons=Button.inline("بازکردن مجدد", data="open"),
    )


def page_num(index, key):
    rows = udB.get_key("HELP_ROWS") or 5
    cols = udB.get_key("HELP_COLUMNS") or 2
    loaded = HELP.get(key, [])
    emoji = udB.get_key("EMOJI_IN_HELP") or "✘"
    List = [
        Button.inline(f"{emoji} {x} {emoji}", data=f"uplugin_{key}_{x}|{index}")
        for x in sorted(loaded)
    ]
    all_ = split_list(List, cols)
    fl_ = split_list(all_, rows)
    try:
        new_ = fl_[index]
    except IndexError:
        new_ = fl_[0] if fl_ else []
        index = 0
    if index == 0 and len(fl_) == 1:
        new_.append([Button.inline("« بازگشت »", data="open")])
    else:
        new_.append(
            [
                Button.inline(
                    "« قبلی",
                    data=f"uh_{key}_{index-1}",
                ),
                Button.inline("« بازگشت »", data="open"),
                Button.inline(
                    "بعدی »",
                    data=f"uh_{key}_{index+1}",
                ),
            ]
        )
    return new_


# --------------------------------------------------------------------------------- #


STUFF = {}


@in_pattern("stf(.*)", owner=True)
async def ibuild(e):
    n = e.pattern_match.group(1).strip()
    builder = e.builder
    if not (n and n.isdigit()):
        return
    ok = STUFF.get(int(n))
    txt = ok.get("msg")
    pic = ok.get("media")
    btn = ok.get("button")
    if not (pic or txt):
        txt = "هی!"
    if pic:
        try:
            include_media = True
            mime_type, _pic = None, None
            cont, results = None, None
            try:
                ext = str(pic).split(".")[-1].lower()
            except BaseException:
                ext = None
            if ext in ["img", "jpg", "png"]:
                _type = "photo"
                mime_type = "image/jpg"
            elif ext in ["mp4", "mkv", "gif"]:
                mime_type = "video/mp4"
                _type = "gif"
            else:
                try:
                    if "telethon.tl.types" in str(type(pic)):
                        _pic = pic
                    else:
                        _pic = resolve_bot_file_id(pic)
                except BaseException:
                    pass
                if _pic:
                    results = [
                        await builder.document(
                            _pic,
                            title="Ultroid Op",
                            text=txt,
                            description="@ElenLiL",
                            buttons=btn,
                            link_preview=False,
                        )
                    ]
                else:
                    _type = "article"
                    include_media = False
            if not results:
                if include_media:
                    cont = InputWebDocument(pic, 0, mime_type, [])
                results = [
                    await builder.article(
                        title="Ultroid Op",
                        type=_type,
                        text=txt,
                        description="@ElenLiL",
                        include_media=include_media,
                        buttons=btn,
                        thumb=cont,
                        content=cont,
                        link_preview=False,
                    )
                ]
            return await e.answer(results)
        except Exception as er:
            LOGS.exception(er)
    result = [
        await builder.article("Ultroid Op", text=txt, link_preview=False, buttons=btn)
    ]
    await e.answer(result)


async def something(e, msg, media, button, reply=True, chat=None):
    if e.client._bot:
        return await e.reply(msg, file=media, buttons=button)
    num = len(STUFF) + 1
    STUFF.update({num: {"msg": msg, "media": media, "button": button}})
    try:
        res = await e.client.inline_query(asst.me.username, f"stf{num}")
        return await res[0].click(
            chat or e.chat_id,
            reply_to=bool(isinstance(e, Message) and reply),
            hide_via=True,
            silent=True,
        )

    except Exception as er:
        LOGS.exception(er)
