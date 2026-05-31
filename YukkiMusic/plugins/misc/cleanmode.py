#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import re
from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ParseMode
from pyrogram.errors import FloodWait
from pyrogram.raw import types

import config
from config import adminlist, chatstats, clean, userstats
from strings import get_command
from YukkiMusic import app, userbot
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import (get_active_chats,
                                       get_authuser_names, get_client,
                                       get_particular_top,
                                       get_served_chats,
                                       get_served_users, get_user_top,
                                       is_cleanmode_on, set_queries,
                                       update_particular_top,
                                       update_user_top)
from YukkiMusic.utils.decorators.language import language
from YukkiMusic.utils.formatters import alpha_to_int
from YukkiMusic.utils.tg_send import _fix_tg_emoji

BROADCAST_COMMAND = get_command("BROADCAST_COMMAND")
AUTO_DELETE = config.CLEANMODE_DELETE_MINS
AUTO_SLEEP = 5
IS_BROADCASTING = False
cleanmode_group = 15


@app.on_raw_update(group=cleanmode_group)
async def clean_mode(client, update, users, chats):
    global IS_BROADCASTING
    if IS_BROADCASTING:
        return
    try:
        if not isinstance(update, types.UpdateReadChannelOutbox):
            return
    except:
        return
    if users:
        return
    if chats:
        return
    message_id = update.max_id
    chat_id = int(f"-100{update.channel_id}")
    if not await is_cleanmode_on(chat_id):
        return
    if chat_id not in clean:
        clean[chat_id] = []
    time_now = datetime.now()
    put = {
        "msg_id": message_id,
        "timer_after": time_now + timedelta(minutes=AUTO_DELETE),
    }
    clean[chat_id].append(put)
    await set_queries(1)


# Broadcast flag order matters: longest first so e.g. "-pinloud" is removed
# before "-pin" (which is a substring of it).
_BROADCAST_FLAGS = (
    "-pinloud", "-forward", "-assistant",
    "-nobot", "-user", "-pin",
)


def _strip_broadcast_flags(s: str) -> str:
    """Remove all known broadcast flags from a text/caption."""
    if not s:
        return ""
    for flag in _BROADCAST_FLAGS:
        s = s.replace(flag, "")
    return " ".join(s.split()).strip()


def _flood_seconds(e: FloodWait) -> int:
    """pyrogram 2.x uses .value; v1 used .x. Be defensive."""
    return int(getattr(e, "value", getattr(e, "x", 0)) or 0)


def _has_media(m) -> bool:
    return bool(
        m.photo or m.video or m.animation or m.document
        or m.audio or m.voice or m.sticker or m.video_note
    )


@app.on_message(filters.command(BROADCAST_COMMAND) & SUDOERS)
@language
async def braodcast_message(client, message, _):
    """
    Broadcast a message to all served chats / users.

    Three input modes:
      1. Reply to any message  →  bot copies that message to every chat.
      2. Upload media (photo, GIF, video, document, etc.) with /broadcast
         in the caption  →  bot copies the media (and cleaned caption) out.
      3. Plain text:  /broadcast Hello everyone  →  bot sends text.

    Flags (any order, anywhere in the text/caption):
      -nobot     skip the bot's own served chats
      -user      also DM every served user
      -assistant also broadcast through assistant accounts
      -pin       silent-pin in each chat
      -pinloud   pin with notification
      -forward   use forward_messages (shows "Forwarded from") instead
                 of the default copy_message (clean look — recommended
                 for advertising / promotional sends)
    """
    global IS_BROADCASTING

    raw = message.text or message.caption or ""
    has_media = _has_media(message)
    has_reply = message.reply_to_message is not None

    # ── Resolve source of the broadcast content ──────────────────────────
    src_chat = None
    src_msg_id = None
    custom_caption = None  # only for media-with-command
    text_only = None       # only for plain-text mode

    if has_reply:
        src_chat = message.chat.id
        src_msg_id = message.reply_to_message.id
    elif has_media:
        # Media uploaded with /broadcast in caption.
        # Use .html so custom-emoji entity IDs survive into the caption copy.
        src_chat = message.chat.id
        src_msg_id = message.id
        cap_html = message.caption.html if (message.caption and hasattr(message.caption, "html")) else (message.caption or "")
        cleaned = _fix_tg_emoji(_strip_broadcast_flags(cap_html))
        # Drop the leading /broadcast[@bot] command token from the HTML string
        cleaned = re.sub(r'^/\S+\s*', '', cleaned, count=1).strip()
        custom_caption = cleaned or None
    else:
        # Plain text — use .html so premium emoji entity IDs are preserved.
        if len(message.command) < 2:
            return await message.reply_text(_["broad_5"])
        raw_html = message.text.html if hasattr(message.text, "html") else str(message.text)
        text_only = _fix_tg_emoji(re.sub(
            r'^/\S+\s*', '',
            _strip_broadcast_flags(raw_html),
            count=1,
        ).strip())
        if not text_only:
            return await message.reply_text(_["broad_6"])

    # ── Parse flags from raw text or caption ─────────────────────────────
    use_forward   = "-forward" in raw
    use_pinloud   = "-pinloud" in raw
    # `-pin` is a substring of `-pinloud`; ignore it if pinloud is present.
    use_pin       = ("-pin" in raw) and not use_pinloud
    to_users      = "-user" in raw
    no_bot        = "-nobot" in raw
    use_assistant = "-assistant" in raw

    async def _send(client_, target_chat_id):
        """Send the resolved broadcast content via the given client.

        text_only and custom_caption are HTML strings (entities preserved as
        <tg-emoji emoji-id="…"> tags).  Pass parse_mode=HTML so Telegram
        renders premium emoji — forwarded/copied messages keep entities natively.
        """
        if src_msg_id is None:
            # Plain-text broadcast — HTML preserves custom emoji entity IDs.
            return await client_.send_message(
                target_chat_id, text=text_only,
                parse_mode=ParseMode.HTML,
            )
        if use_forward:
            return await client_.forward_messages(
                target_chat_id, src_chat, src_msg_id
            )
        # Default: copy_message → no "forwarded from" header.
        # copy_message preserves all entities when caption is not overridden.
        if custom_caption is not None:
            return await client_.copy_message(
                target_chat_id, src_chat, src_msg_id,
                caption=custom_caption,
                parse_mode=ParseMode.HTML,
            )
        return await client_.copy_message(
            target_chat_id, src_chat, src_msg_id
        )

    IS_BROADCASTING = True

    # ── Broadcast inside chats (default) ─────────────────────────────────
    if not no_bot:
        sent = 0
        pin = 0
        schats = await get_served_chats()
        chats = [int(c["chat_id"]) for c in schats]
        for i in chats:
            if i == -1001733534088:
                continue
            try:
                m = await _send(app, i)
                if use_pin or use_pinloud:
                    try:
                        await m.pin(disable_notification=not use_pinloud)
                        pin += 1
                    except Exception:
                        pass
                sent += 1
            except FloodWait as e:
                wait = _flood_seconds(e)
                if wait > 200:
                    continue
                await asyncio.sleep(wait)
            except Exception:
                continue
        try:
            await message.reply_text(_["broad_1"].format(sent, pin))
        except Exception:
            pass

    # ── Direct-message every served user ────────────────────────────────
    if to_users:
        susr = 0
        susers = await get_served_users()
        served_users = [int(u["user_id"]) for u in susers]
        for i in served_users:
            try:
                await _send(app, i)
                susr += 1
            except FloodWait as e:
                wait = _flood_seconds(e)
                if wait > 200:
                    continue
                await asyncio.sleep(wait)
            except Exception:
                pass
        try:
            await message.reply_text(_["broad_7"].format(susr))
        except Exception:
            pass

    # ── Broadcast through assistant userbots ────────────────────────────
    if use_assistant:
        aw = await message.reply_text(_["broad_2"])
        text = _["broad_3"]
        from YukkiMusic.core.userbot import assistants

        for num in assistants:
            sent = 0
            ub = await get_client(num)
            async for dialog in ub.iter_dialogs():
                if dialog.chat.id == -1001733534088:
                    continue
                try:
                    await _send(ub, dialog.chat.id)
                    sent += 1
                except FloodWait as e:
                    wait = _flood_seconds(e)
                    if wait > 200:
                        continue
                    await asyncio.sleep(wait)
                except Exception as e:
                    print(e)
                    continue
            text += _["broad_4"].format(num, sent)
        try:
            await aw.edit_text(text)
        except Exception:
            pass

    IS_BROADCASTING = False


async def auto_clean():
    while not await asyncio.sleep(AUTO_SLEEP):
        try:
            for chat_id in chatstats:
                for dic in chatstats[chat_id]:
                    vidid = dic["vidid"]
                    title = dic["title"]
                    chatstats[chat_id].pop(0)
                    spot = await get_particular_top(chat_id, vidid)
                    if spot:
                        spot = spot["spot"]
                        next_spot = spot + 1
                        new_spot = {"spot": next_spot, "title": title}
                        await update_particular_top(
                            chat_id, vidid, new_spot
                        )
                    else:
                        next_spot = 1
                        new_spot = {"spot": next_spot, "title": title}
                        await update_particular_top(
                            chat_id, vidid, new_spot
                        )
            for user_id in userstats:
                for dic in userstats[user_id]:
                    vidid = dic["vidid"]
                    title = dic["title"]
                    userstats[user_id].pop(0)
                    spot = await get_user_top(user_id, vidid)
                    if spot:
                        spot = spot["spot"]
                        next_spot = spot + 1
                        new_spot = {"spot": next_spot, "title": title}
                        await update_user_top(
                            user_id, vidid, new_spot
                        )
                    else:
                        next_spot = 1
                        new_spot = {"spot": next_spot, "title": title}
                        await update_user_top(
                            user_id, vidid, new_spot
                        )
        except:
            continue
        try:
            for chat_id in clean:
                if chat_id == config.LOG_GROUP_ID:
                    continue
                for x in clean[chat_id]:
                    if datetime.now() > x["timer_after"]:
                        try:
                            await app.delete_messages(
                                chat_id, x["msg_id"]
                            )
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                        except:
                            continue
                    else:
                        continue
        except:
            continue
        try:
            served_chats = await get_active_chats()
            for chat_id in served_chats:
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    async for user in app.get_chat_members(
                        chat_id, filter=ChatMembersFilter.ADMINISTRATORS
                    ):
                        if (user.privileges and user.privileges.can_manage_video_chats):
                            adminlist[chat_id].append(user.user.id)
                    authusers = await get_authuser_names(chat_id)
                    for user in authusers:
                        user_id = await alpha_to_int(user)
                        adminlist[chat_id].append(user_id)
        except:
            continue


asyncio.create_task(auto_clean())
