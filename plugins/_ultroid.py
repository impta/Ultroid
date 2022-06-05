# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from telethon.errors import (
    BotMethodInvalidError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
)

from . import LOG_CHANNEL, LOGS, Button, asst, eor, get_string, ultroid_cmd

REPOMSG = """
• **ElenLiL USERBOT** •\n
• Portal - [Click Here](https://t.me/ElenLiLBoT)
• Creator - [Click Here](https://t.me/ElenLiL)
• Support - @ElenLiL
"""

RP_BUTTONS = [
    [
        Button.url(get_string("bot_3"), "https://t.me/ElenLiLBoT"),
        Button.url("Creator", "https://t.me/ElenLiL"),
    ],
    [Button.url("Support Group", "t.me/GapemooN")],
]

ULTSTRING = """🎇 **ممنونم بابت اینکه از ربات من استفاده میکنید**

• در اینجا، برخی از موارد اساسی وجود دارد، که می توانید در مورد استفاده از آن بدانید"""


@ultroid_cmd(
    pattern="repo$",
    manager=True,
)
async def repify(e):
    try:
        q = await e.client.inline_query(asst.me.username, "")
        await q[0].click(e.chat_id)
        return await e.delete()
    except (
        ChatSendInlineForbiddenError,
        ChatSendMediaForbiddenError,
        BotMethodInvalidError,
    ):
        pass
    except Exception as er:
        LOGS.info("Error while repo command : " + str(er))
    await e.eor(REPOMSG)


@ultroid_cmd(pattern="ultroid$")
async def useUltroid(rs):
    button = Button.inline("شروع >>", "initft_2")
    msg = await asst.send_message(
        LOG_CHANNEL,
        ULTSTRING,
        file="https://telegra.ph/file/485b76bfd13813829655b.jpg",
        buttons=button,
    )
    if not (rs.chat_id == LOG_CHANNEL and rs.client._bot):
        await eor(rs, f"**[Click Here]({msg.message_link})**")
