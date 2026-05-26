#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import sys

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import BotCommand

import config

from ..logging import LOGGER


class YukkiBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            "YukkiMusicBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        # Warm the peer cache so numeric chat_ids (LOG_GROUP_ID and any
        # served groups) resolve without ValueError on first /play.
        try:
            count = 0
            async for _d in self.get_dialogs(limit=500):
                count += 1
            LOGGER(__name__).info(f"Bot: cached {count} dialogs")
        except Exception as e:
            LOGGER(__name__).warning(f"Bot dialog warmup failed: {e}")
        try:
            await self.send_message(
                config.LOG_GROUP_ID, "Bot Started"
            )
        except ValueError as e:
            if "Peer id invalid" in str(e):
                # pyrogram 2.x: peer not yet in session cache.
                # This happens on the first run with a fresh session.
                # The bot will cache the log group once it receives the
                # first update from it. After the first successful start
                # the session file is persisted and this won't recur.
                LOGGER(__name__).warning(
                    f"Log group ({config.LOG_GROUP_ID}) not yet in session "
                    "cache. If your bot IS in the log group, this will "
                    "resolve itself on the next restart. Continuing..."
                )
            else:
                LOGGER(__name__).error(
                    "Bot has failed to access the log Group. Make sure "
                    "that you have added your bot to your log channel and "
                    "promoted as admin!"
                )
                sys.exit()
        except Exception:
            LOGGER(__name__).error(
                "Bot has failed to access the log Group. Make sure that "
                "you have added your bot to your log channel and promoted "
                "as admin!"
            )
            sys.exit()
        if config.SET_CMDS == str(True):
            try:
                await self.set_bot_commands([
                    # ── Core playback ──
                    BotCommand("play",      "🎵 Play a song by name or URL"),
                    BotCommand("vplay",     "🎥 Play a video by name or URL"),
                    BotCommand("playforce", "⚡ Force-play (skip current, keep queue)"),
                    BotCommand("song",      "💾 Download a song from YouTube (PM only)"),
                    # ── Playback control ──
                    BotCommand("pause",     "⏸ Pause the current track"),
                    BotCommand("resume",    "▶️ Resume the paused track"),
                    BotCommand("skip",      "⏭ Skip to the next track"),
                    BotCommand("end",       "⏹ Stop playback and leave voice chat"),
                    BotCommand("mute",      "🔇 Mute the voice chat"),
                    BotCommand("unmute",    "🔊 Unmute the voice chat"),
                    BotCommand("loop",      "🔁 Loop the current track"),
                    BotCommand("seek",      "⏩ Seek forward by N seconds"),
                    BotCommand("seekback",  "⏪ Seek backward by N seconds"),
                    BotCommand("shuffle",   "🎲 Shuffle the queue"),
                    BotCommand("queue",     "📑 Show the current queue"),
                    # ── Modes & settings ──
                    BotCommand("playmode",  "🎛️ Change play mode (direct / inline)"),
                    BotCommand("settings",  "⚙️ Open the bot settings panel"),
                    BotCommand("language",  "🌐 Change the bot language"),
                    BotCommand("channelplay", "📡 Link this group to a channel"),
                    # ── Auth & admin ──
                    BotCommand("auth",      "🎩 Add a user to AUL (auth users)"),
                    BotCommand("unauth",    "🗑 Remove a user from AUL"),
                    BotCommand("authusers", "📋 Show AUL"),
                    BotCommand("admincache","🔄 Reload admin cache"),
                    BotCommand("reload",    "🔄 Alias for /admincache"),
                    # ── Info ──
                    BotCommand("help",      "📜 Command reference"),
                    BotCommand("start",     "🛸 Boot the bot"),
                    BotCommand("ping",      "⚡ Latency / system telemetry"),
                    BotCommand("lyrics",    "📖 Search song lyrics"),
                    BotCommand("playlist",  "💾 Your saved server-side playlist"),
                    BotCommand("gstats",    "📊 Global / personal stats"),
                ])
                LOGGER(__name__).info("Bot command menu registered")
            except Exception as e:
                LOGGER(__name__).warning(
                    f"Failed to register bot command menu: {e}"
                )
        try:
            a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if a.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
                LOGGER(__name__).error(
                    "Please promote Bot as Admin in Logger Group"
                )
                sys.exit()
        except ValueError as e:
            if "Peer id invalid" in str(e):
                LOGGER(__name__).warning(
                    "Skipping admin check — log group not yet in session "
                    "cache. Will be checked on next restart."
                )
            else:
                raise
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"MusicBot Started as {self.name}")
