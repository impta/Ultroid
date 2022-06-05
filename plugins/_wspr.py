# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import re

from telethon import Button
from telethon.errors.rpcerrorlist import (
    BotInlineDisabledError,
    BotResponseTimeoutError,
    MessageNotModifiedError,
)
from telethon.tl import types
from telethon.tl.functions.users import GetFullUserRequest as gu

from . import (
    HNDLR,
    LOGS,
    asst,
    callback,
    get_string,
    in_pattern,
    inline_mention,
    ultroid_bot,
    ultroid_cmd,
)

buddhhu = {}


@ultroid_cmd(
    pattern="wspr( (.*)|$)",
)
async def _(e):
    if e.reply_to_msg_id:
        okk = await e.get_reply_message()
        if okk.sender.username:
            put = f"@{okk.sender.username}"
        put = okk.sender_id
    else:
        put = e.pattern_match.group(1).strip()
    if put:
        try:
            results = await e.client.inline_query(asst.me.username, f"msg {put}")
        except BotResponseTimeoutError:
            return await e.eor(
                get_string("help_2").format(HNDLR),
            )
        except BotInlineDisabledError:
            return await e.eor(get_string("help_3"))
        await results[0].click(e.chat_id, reply_to=e.reply_to_msg_id, hide_via=True)
        return await e.delete()
    await e.eor(get_string("wspr_3"))


@in_pattern("wspr", owner=True)
async def _(e):
    iuser = e.query.user_id
    zzz = e.text.split(maxsplit=2)
    try:
        query = zzz[1]
        if query.isdigit():
            query = int(query)
        logi = await ultroid_bot.get_entity(query)
    except IndexError:
        sur = e.builder.article(
            title="ای دی رو وارد کن",
            description="یوزرنیم یا ای دی ای رو تایپ نکردی",
            text="ای دی یا یوزرنیمی رو تایپ نکردی",
        )
        return await e.answer([sur])
    except ValueError:
        sur = e.builder.article(
            title="یارو پیدا نشد",
            description="چک کن ک یوزرنیم یا ای دی رو درست زدی",
            text="چک کن ک یوزرنیم یا ای دی رو درست زدی",
        )
        return await e.answer([sur])
    try:
        desc = zzz[2]
    except IndexError:
        sur = e.builder.article(title="پیامتو بنویس", text="پیامتو ننوشتی")
        return await e.answer([sur])
    button = [
        Button.inline("پیام مخفی", data=f"dd_{e.id}"),
        Button.inline("حذف پیام", data=f"del_{e.id}"),
    ]
    us = logi.username or logi.first_name
    sur = e.builder.article(
        title=logi.first_name,
        description=desc,
        text=get_string("wspr_1").format(us),
        buttons=button,
    )
    buddhhu.update({e.id: [logi.id, iuser, desc]})
    await e.answer([sur])


@in_pattern("msg", owner=True)
async def _(e):
    zzz = e.text.split(maxsplit=1)
    desc = "بمال روم"
    try:
        query = zzz[1]
        if query.isdigit():
            query = int(query)
        logi = await ultroid_bot(gu(id=query))
        user = logi.users[0]
        mention = inline_mention(user)
        x = user.status
        if isinstance(x, types.UserStatusOnline):
            status = "آنلاین"
        elif isinstance(x, types.UserStatusOffline):
            status = "آفلاین"
        elif isinstance(x, types.UserStatusRecently):
            status = "آخرین بازدید اخیرن"
        elif isinstance(x, types.UserStatusLastMonth):
            status = "آخرین بازدید چن ماه پیش"
        elif isinstance(x, types.UserStatusLastWeek):
            status = "آخرین بازدید چن هفته پیش"
        else:
            status = "نمیتونم بگم"
        text = f"**نام:**    `{user.first_name}`\n"
        text += f"**آی دی:**    `{user.id}`\n"
        if user.username:
            text += f"**یوزرنیم:**    `{user.username}`\n"
            url = f"https://t.me/{user.username}"
        else:
            text += f"**منشن:**    `{mention}`\n"
            url = f"tg://user?id={user.id}"
        text += f"**وضعیت:**    `{status}`\n"
        text += f"**درباره:**    `{logi.full_user.about}`"
        button = [
            Button.url("Private", url=url),
            Button.switch_inline(
                "پیام مخفی",
                query=f"wspr {query} سلام 👋",
                same_peer=True,
            ),
        ]
        sur = e.builder.document(
            title=user.first_name,
            description=desc,
            file=logi.full_user.profile_photo,
            include_media=False,
            text=text,
            buttons=button,
        )
    except IndexError:
        sur = e.builder.article(
            title="Give Username",
            description="You Didn't Type Username or id.",
            text="You Didn't Type Username or id.",
        )
    except BaseException as er:
        LOGS.exception(er)
        name = get_string("wspr_4").format(query)
        sur = e.builder.article(
            title=name,
            text=name,
        )

    await e.answer([sur])


@callback(
    re.compile(
        "dd_(.*)",
    ),
)
async def _(e):
    ids = int(e.pattern_match.group(1).strip().decode("UTF-8"))
    if buddhhu.get(ids):
        if e.sender_id in buddhhu[ids]:
            await e.answer(buddhhu[ids][-1], alert=True)
        else:
            await e.answer("برا ت نی", alert=True)
    else:
        await e.answer(get_string("wspr_2"), alert=True)


@callback(re.compile("del_(.*)"))
async def _(e):
    ids = int(e.pattern_match.group(1).strip().decode("UTF-8"))
    if buddhhu.get(ids):
        if e.sender_id in buddhhu[ids]:
            buddhhu.pop(ids)
            try:
                await e.edit(get_string("wspr_2"))
            except MessageNotModifiedError:
                pass
        else:
            await e.answer(get_string("wspr_5"), alert=True)
