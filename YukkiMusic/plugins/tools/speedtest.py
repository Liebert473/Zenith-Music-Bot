#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import html as _html

import speedtest
from pyrogram import filters

from strings import get_command
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS

# Commands
SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def _run_speedtest() -> dict:
    """Run the speed test synchronously (executed in a thread executor).

    Returns the result dict, or raises on failure — the caller handles
    exceptions.  No message editing happens here: this runs in a worker
    thread where awaiting pyrogram coroutines is not possible.
    """
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    return test.results.dict()


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("🔎 Running Speed test... Please wait.")
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(None, _run_speedtest)
    except Exception as e:
        return await m.edit_text(
            f"❌ <b>Speedtest failed:</b> <code>{_html.escape(str(e))}</code>"
        )

    def esc(*keys):
        ref = result
        try:
            for k in keys:
                ref = ref[k]
            return _html.escape(str(ref))
        except Exception:
            return "N/A"

    output = (
        "<b>Speedtest Results</b>\n\n"
        "<u><b>Client:</b></u>\n"
        f"<b>ISP:</b> {esc('client', 'isp')}\n"
        f"<b>Country:</b> {esc('client', 'country')}\n\n"
        "<u><b>Server:</b></u>\n"
        f"<b>Name:</b> {esc('server', 'name')}\n"
        f"<b>Country:</b> {esc('server', 'country')}, {esc('server', 'cc')}\n"
        f"<b>Sponsor:</b> {esc('server', 'sponsor')}\n"
        f"<b>Latency:</b> {esc('server', 'latency')}\n"
        f"<b>Ping:</b> {esc('ping')}"
    )
    try:
        await app.send_photo(
            chat_id=message.chat.id,
            photo=result["share"],
            caption=output,
        )
        await m.delete()
    except Exception:
        # Fall back to a text-only result if the share image fails.
        await m.edit_text(output)
