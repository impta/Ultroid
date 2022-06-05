# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

"""
✘ فرمان های دردسترس

• `{i}autokick <on/off>`
    on - برای فعال کردن.
    off - برای غیرفعال کردن.
    کاربران جدیدی که به گروه ملحق میشوند به‌طور خودکار حذف شوند.

• `{i}cban`
    فعال یا غیرفعال کردن بن اتوماتیک، ارسال بعنوان چنل در گپ.

• `{i}addwl <یوزرنیم>`
   چنل را به لیست سفید چنل بن اضافه کنید.

• `{i}remwl <یوزرنیم>`
   چنل را از لیست سفید چنل بن حذف کنید.

• `{i}listwl` : لیست تمام چنل های لیست سفید.
"""


from pyUltroid.dB import autoban_db, dnd_db
from pyUltroid.functions.admins import get_update_linked_chat
from telethon import events
from telethon.tl.types import Channel

from . import LOGS, asst, get_string, inline_mention, ultroid_bot, ultroid_cmd


async def dnd_func(event):
    if event.chat_id in dnd_db.get_dnd_chats():
        for user in event.users:
            try:
                await (
                    await event.client.kick_participant(event.chat_id, user)
                ).delete()
            except Exception as ex:
                LOGS.error("Error in DND:")
                LOGS.exception(ex)
        await event.delete()


async def channel_del(event):
    if not autoban_db.is_autoban_enabled(event.chat_id):
        return
    if autoban_db.is_whitelisted(event.chat_id, event.sender_id):
        return
    linked = await get_update_linked_chat(event)
    if linked == event.sender.id:
        return
    if event.chat.creator or event.chat.admin_rights.ban_users:
        try:
            await event.client.edit_permissions(
                event.chat_id, event.sender_id, view_messages=False
            )
        except Exception as er:
            LOGS.exception(er)
    await event.try_delete()


@ultroid_cmd(
    pattern="autokick (on|off)$",
    admins_only=True,
    manager=True,
    require="ban_users",
    fullsudo=True,
)
async def _(event):
    match = event.pattern_match.group(1)
    if match == "on":
        if dnd_db.chat_in_dnd(event.chat_id):
            return await event.eor("`گپ از قبل در حالت مزاحم نشوید هستش.`", time=3)
        dnd_db.add_dnd(event.chat_id)
        event.client.add_handler(
            dnd_func, events.ChatAction(func=lambda x: x.user_joined)
        )
        await event.eor("`حالت مزاحم نشوید برای این گپ فعال شد.`", time=3)
    elif match == "off":
        if not dnd_db.chat_in_dnd(event.chat_id):
            return await event.eor("`چت رفت ب حالت مزاحم نشوید.`", time=3)
        dnd_db.del_dnd(event.chat_id)
        await event.eor("`حالت مزاحم نشوید برای این گپ غیرفعال شد.`", time=3)


@ultroid_cmd(pattern="cban$", admins_only=True)
async def ban_cha(ult):
    if autoban_db.is_autoban_enabled(ult.chat_id):
        autoban_db.del_channel(ult.chat_id)
        return await ult.eor("`غیرفعال کردنه چنل بنه اتوماتیک...`")
    if not (
        ult.chat.creator
        or (ult.chat.admin_rights.delete_messages or ult.chat.admin_rights.ban_users)
    ):
        return await ult.eor(
            "شما حقوق لازم برای ادمینی را ندارید!\nشما نمی توانید از چنل بن بدون تیکه Ban/del استفاده کنید..`"
        )
    autoban_db.add_channel(ult.chat_id)
    await ult.eor("`چنل بن با موفقیت فعال شد!`")
    ult.client.add_handler(
        channel_del,
        events.NewMessage(
            func=lambda x: not x.is_private and isinstance(x.sender, Channel)
        ),
    )


@ultroid_cmd(pattern="(list|add|rem)wl( (.*)|$)")
async def do_magic(event):
    match = event.pattern_match.group(1)
    msg = await event.eor(get_string("com_1"))
    if match == "list":
        cha = autoban_db.get_whitelisted_channels(event.chat_id)
        if not cha:
            return await msg.edit("`هیچ چنلی در لیست سفید برای گپ فعلی وجود ندارد.`")
        Msg = "**لیست سفید چنل ها در چت فعلی**\n\n"
        for ch in cha:
            Msg += f"(`{ch}`) "
            try:
                Msg += inline_mention(await event.client.get_entity(ch))
            except Exception:
                Msg += "\n"
        return await msg.edit(Msg)
    usea = event.pattern_match.group(2).strip()
    if not usea:
        return await Msg.edit(
            "`لطفاً یک نام کاربری/شناسه چنل برای افزودن/حذف به/از لیست سفید ارائه دهید..`"
        )
    try:
        u_id = await event.client.parse_id(usea)
        cha = await event.client.get_entity(u_id)
    except Exception as er:
        LOGS.exception(er)
        return await msg.edit(f"خطا رخ داد!\n`{er}`")
    if match == "add":
        autoban_db.add_to_whitelist(event.chat_id, u_id)
        return await msg.edit(f"`اضافه شد` {inline_mention(cha)} `ب لیست سفید..`")
    autoban_db.del_from_whitelist(event.chat_id, u_id)
    await msg.edit(f"`حذف شد` {inline_mention(cha)} `از لیست سفید.`")


if dnd_db.get_dnd_chats():
    ultroid_bot.add_handler(dnd_func, events.ChatAction(func=lambda x: x.user_joined))
    asst.add_handler(dnd_func, events.ChatAction(func=lambda x: x.user_joined))

if autoban_db.get_all_channels():
    ultroid_bot.add_handler(
        channel_del,
        events.NewMessage(
            func=lambda x: not x.is_private and isinstance(x.sender, Channel)
        ),
    )
