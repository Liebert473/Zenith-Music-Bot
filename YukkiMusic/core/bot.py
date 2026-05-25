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
                await self.set_bot_commands(
                    [
                        BotCommand("ping", "Check that bot is alive or dead"),
                        BotCommand("play", "Starts playing the requested song"),
                        BotCommand("skip", "Moves to the next track in queue"),
                        BotCommand("pause", "Pause the current playing song"),
                        BotCommand("resume", "Resume the paused song"),
                        BotCommand("end", "Clear the queue and leave voice chat"),
                        BotCommand("shuffle", "Randomly shuffles the queued playlist."),
                        BotCommand("playmode", "Allows you to change the default playmode for your chat"),
                        BotCommand("settings", "Open the settings of the music bot for your chat.")
                        ]
                    )
            except:
                pass
        else:
            pass
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
