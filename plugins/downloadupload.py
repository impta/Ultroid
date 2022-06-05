# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

"""
✘ فرمان های دردسترس -

• `{i}ul <path/to/file>`
    آپلود کردن فایل به تلگرام.
    طبق نیاز از آرگومان های زیر قبل یا بعد از نام فایل استفاده کنید:
      `--stream` برای آپلود بعنوان استریم.
      `--delete` برای حذف فایل اپلود شده.
      `--no-thumb` برای اپلود بدون تامبنیل.

• `{i}dl <filename(optional)>`
    برای دانلود رو فایل ریپلای بزنید.

• `{i}download <DDL> (| filename)`
    دانلود با استفاده از دی دی ال، اگ نام فایل را وارد نکنید، از خودش یچیزی میزنه.
"""

import asyncio
import glob
import os
import time
from datetime import datetime as dt

from aiohttp.client_exceptions import InvalidURL
from pyUltroid.functions.helper import time_formatter
from pyUltroid.functions.tools import set_attributes
from telethon.errors.rpcerrorlist import MessageNotModifiedError

from . import (
    LOGS,
    downloader,
    eor,
    fast_download,
    get_string,
    progress,
    time_formatter,
    ultroid_cmd,
)


@ultroid_cmd(
    pattern="download( (.*)|$)",
)
async def down(event):
    matched = event.pattern_match.group(1).strip()
    msg = await event.eor(get_string("udl_4"))
    if not matched:
        return await eor(msg, get_string("udl_5"), time=5)
    try:
        splited = matched.split(" | ")
        link = splited[0]
        filename = splited[1]
    except IndexError:
        filename = None
    s_time = time.time()
    try:
        filename, d = await fast_download(
            link,
            filename,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d,
                    t,
                    msg,
                    s_time,
                    f"دانلود از {link}",
                )
            ),
        )
    except InvalidURL:
        return await msg.eor("`Invalid URL provided :(`", time=5)
    await msg.eor(f"`{filename}` `دانلود شد در {time_formatter(d*1000)}.`")


@ultroid_cmd(
    pattern="dl( (.*)|$)",
)
async def download(event):
    if not event.reply_to_msg_id:
        return await event.eor(get_string("cvt_3"), time=8)
    xx = await event.eor(get_string("com_1"))
    s = dt.now()
    k = time.time()
    if event.reply_to_msg_id:
        ok = await event.get_reply_message()
        if not ok.media:
            return await xx.eor(get_string("udl_1"), time=5)
        if hasattr(ok.media, "document"):
            file = ok.media.document
            mime_type = file.mime_type
            filename = event.pattern_match.group(1).strip() or ok.file.name
            if not filename:
                if "audio" in mime_type:
                    filename = "audio_" + dt.now().isoformat("_", "seconds") + ".ogg"
                elif "video" in mime_type:
                    filename = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
            try:
                result = await downloader(
                    "resources/downloads/" + filename,
                    file,
                    xx,
                    k,
                    "دانلود " + filename + "...",
                )
            except MessageNotModifiedError as err:
                return await xx.edit(str(err))
            file_name = result.name
        else:
            d = "resources/downloads/"
            file_name = await event.client.download_media(
                ok,
                d,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d,
                        t,
                        xx,
                        k,
                        get_string("com_5"),
                    ),
                ),
            )
    e = dt.now()
    t = time_formatter(((e - s).seconds) * 1000)
    await xx.eor(get_string("udl_2").format(file_name, t))


@ultroid_cmd(
    pattern="ul( (.*)|$)",
)
async def _(event):
    msg = await event.eor(get_string("com_1"))
    match = event.pattern_match.group(1)
    if match:
        match = match.strip()
    if not event.out and match == ".env":
        return await event.reply("`نمیتونی اینکارو بکنی...`")
    stream, force_doc, delete, thumb = (
        False,
        True,
        False,
        "resources/extras/ultroid.jpg",
    )
    if "--stream" in match:
        stream = True
        force_doc = False
    if "--delete" in match:
        delete = True
    if "--no-thumb" in match:
        thumb = None
    arguments = ["--stream", "--delete", "--no-thumb"]
    if any(item in match for item in arguments):
        match = (
            match.replace("--stream", "")
            .replace("--delete", "")
            .replace("--no-thumb", "")
            .strip()
        )
    if match.endswith("/"):
        match += "*"
    results = glob.glob(match)
    if not results and os.path.exists(match):
        results = [match]
    if not results:
        try:
            await event.reply(file=match)
            return await event.try_delete()
        except Exception as er:
            LOGS.exception(er)
        return await msg.eor("`فایل وجود نداره یا مسیر نامعتبره!`")
    for result in results:
        if os.path.isdir(result):
            c, s = 0, 0
            for files in sorted(glob.glob(result + "/*")):
                attributes = None
                if stream:
                    try:
                        attributes = await set_attributes(files)
                    except KeyError as er:
                        LOGS.exception(er)
                try:
                    file, _ = await event.client.fast_uploader(
                        files, show_progress=True, event=msg, to_delete=delete
                    )
                    await event.client.send_file(
                        event.chat_id,
                        file,
                        supports_streaming=stream,
                        force_document=force_doc,
                        thumb=thumb,
                        attributes=attributes,
                        caption=f"`آپلود شد` `{files}` `در {time_formatter(_*1000)}`",
                        reply_to=event.reply_to_msg_id or event,
                    )
                    s += 1
                except (ValueError, IsADirectoryError):
                    c += 1
            break
        attributes = None
        if stream:
            try:
                attributes = await set_attributes(result)
            except KeyError as er:
                LOGS.exception(er)
        file, _ = await event.client.fast_uploader(
            result, show_progress=True, event=msg, to_delete=delete
        )
        await event.client.send_file(
            event.chat_id,
            file,
            supports_streaming=stream,
            force_document=force_doc,
            thumb=thumb,
            attributes=attributes,
            caption=f"`آپلود شد` `{result}` `در {time_formatter(_*1000)}`",
            reply_to=event.reply_to_msg_id or event,
        )
    await msg.try_delete()
