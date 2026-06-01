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
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import (BotCommand, BotCommandScopeAllGroupChats,
                             BotCommandScopeAllPrivateChats,
                             BotCommandScopeChat, BotCommandScopeDefault)

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
            parse_mode=ParseMode.HTML,
        )

    # ── Auto-enhance emoji in all outgoing messages ─────────────────────────
    # Only applies when parse_mode is HTML (default).  MARKDOWN sends are
    # left untouched — injecting <emoji> tags into markdown breaks rendering.
    # pyrogram's HTML parser uses <emoji id="…"> (NOT <tg-emoji>), so we use
    # _prepare_pyrogram which outputs the correct format.

    def _should_enhance(self, kwargs) -> bool:
        """Return True if the message will be parsed as HTML."""
        pm = kwargs.get("parse_mode", ParseMode.HTML)
        # ParseMode.DEFAULT means use client default (which is HTML)
        return pm in (ParseMode.HTML, ParseMode.DEFAULT, None)

    async def send_message(self, chat_id, text, *args, **kwargs):
        if text and isinstance(text, str) and self._should_enhance(kwargs):
            from YukkiMusic.utils.tg_send import _prepare_pyrogram
            text = _prepare_pyrogram(text)
            # Force HTML since we've injected <emoji> tags
            if "<emoji " in text:
                kwargs["parse_mode"] = ParseMode.HTML
        return await super().send_message(chat_id, text, *args, **kwargs)

    async def send_photo(self, chat_id, photo, *args, **kwargs):
        if self._should_enhance(kwargs):
            from YukkiMusic.utils.tg_send import _prepare_pyrogram
            caption = kwargs.get("caption")
            if caption and isinstance(caption, str):
                kwargs["caption"] = _prepare_pyrogram(caption)
                if "<emoji " in kwargs["caption"]:
                    kwargs["parse_mode"] = ParseMode.HTML
        return await super().send_photo(chat_id, photo, *args, **kwargs)

    async def edit_message_text(self, chat_id, message_id, text, *args, **kwargs):
        if text and isinstance(text, str) and self._should_enhance(kwargs):
            from YukkiMusic.utils.tg_send import _prepare_pyrogram
            text = _prepare_pyrogram(text)
            if "<emoji " in text:
                kwargs["parse_mode"] = ParseMode.HTML
        return await super().edit_message_text(chat_id, message_id, text, *args, **kwargs)

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        # Warm the peer cache: bots can't use get_dialogs(), so we
        # resolve the log group directly via get_chat() which caches
        # the peer in the SQLite session file.
        try:
            await self.get_chat(config.LOG_GROUP_ID)
            LOGGER(__name__).info(
                f"Log group ({config.LOG_GROUP_ID}) resolved and cached."
            )
        except Exception as e:
            LOGGER(__name__).warning(f"Log group warmup: {e}")

        try:
            await self.send_message(
                config.LOG_GROUP_ID, "Bot Started"
            )
        except Exception as e:
            LOGGER(__name__).error(
                f"Bot has failed to send to log group "
                f"({config.LOG_GROUP_ID}): {e}\n"
                "Make sure the bot is a member of the log group."
            )
        if config.SET_CMDS == str(True):
            # ── Command definitions ─────────────────────────────────────
            # (cmd, en, zh, my)  — descriptions must be <256 chars.

            # Commands shown in GROUP chats — keep short; only the ones
            # people actually type while music is playing.
            _GROUP_CMDS = [
                ("play",       "🎵 Play a song by name or URL",
                               "🎵 通过名称或链接播放歌曲",
                               "🎵 သီချင်းကို ဖွင့်ပါ"),
                ("vplay",      "🎥 Play a video by name or URL",
                               "🎥 播放视频",
                               "🎥 ဗီဒီယိုဖွင့်ပါ"),
                ("playforce",  "⚡ Force-play (skip current, keep queue)",
                               "⚡ 强制播放",
                               "⚡ Force-play"),
                ("pause",      "⏸ Pause",
                               "⏸ 暂停",
                               "⏸ ခဏရပ်ပါ"),
                ("resume",     "▶️ Resume",
                               "▶️ 继续",
                               "▶️ ပြန်ဖွင့်ပါ"),
                ("skip",       "⏭ Skip to next track",
                               "⏭ 跳到下一首",
                               "⏭ ကျော်ပါ"),
                ("end",        "⏹ Stop and leave voice chat",
                               "⏹ 停止并退出",
                               "⏹ ရပ်ပြီး ထွက်ပါ"),
                ("queue",      "📑 Show the queue",
                               "📑 播放队列",
                               "📑 Queue ကြည့်ပါ"),
                ("shuffle",    "🎲 Shuffle the queue",
                               "🎲 随机播放",
                               "🎲 Shuffle"),
                ("settings",   "⚙️ Group settings",
                               "⚙️ 群组设置",
                               "⚙️ Group settings"),
                ("help",       "📜 Command reference",
                               "📜 命令参考",
                               "📜 Commands"),
                ("advertise",  "📊 Bot reach stats",
                               "📊 机器人覆盖统计",
                               "📊 Bot reach stats"),
            ]

            # Commands shown in PRIVATE chats — everything that works in PM.
            _PRIVATE_CMDS = [
                ("start",     "🛸 Open the bot",
                              "🛸 启动机器人",
                              "🛸 Bot ကို ဖွင့်ပါ"),
                ("help",      "📜 Command reference",
                              "📜 命令参考",
                              "📜 Commands"),
                ("ping",      "⚡ Latency / system stats",
                              "⚡ 延迟 / 系统状态",
                              "⚡ Ping"),
                ("stats",     "📊 Bot stats",
                              "📊 机器人统计",
                              "📊 Stats"),
                ("gstats",    "📈 Global play stats",
                              "📈 全局播放统计",
                              "📈 Global stats"),
                ("lyrics",    "📖 Search song lyrics",
                              "📖 搜索歌词",
                              "📖 Lyrics"),
                ("song",      "💾 Download a song from YouTube",
                              "💾 从 YouTube 下载歌曲",
                              "💾 Song ဆွဲချ"),
                ("playlist",  "💾 Your saved playlist",
                              "💾 我的播放列表",
                              "💾 Playlist"),
                ("advertise", "📊 Bot reach stats (for advertisers)",
                              "📊 机器人覆盖统计（广告商专用）",
                              "📊 Bot reach stats [advertisers]"),
            ]

            # Extra commands shown ONLY in the owner's private chat.
            _OWNER_PM_CMDS = _PRIVATE_CMDS + [
                ("setstart",         "✏️ Set custom /start text",
                                     "✏️ 设置自定义欢迎语",
                                     "✏️ /start text သတ်မှတ်ပါ"),
                ("setstartimg",      "🖼 Set custom /start image",
                                     "🖼 设置自定义欢迎图片",
                                     "🖼 /start image သတ်မှတ်ပါ"),
                ("clearstart",       "🗑 Clear custom /start",
                                     "🗑 清除自定义欢迎",
                                     "🗑 Custom /start ဖျက်ပါ"),
                ("viewstart",        "👁 Preview custom /start",
                                     "👁 预览自定义欢迎",
                                     "👁 /start preview"),
                ("setsupportgroup",  "🛡️ Set support group link",
                                     "🛡️ 设置支持群组链接",
                                     "🛡️ Support group link"),
                ("setsupportchannel","📡 Set support channel link",
                                     "📡 设置支持频道链接",
                                     "📡 Support channel link"),
                ("clearsupport",     "🗑 Clear support link overrides",
                                     "🗑 清除支持链接覆盖",
                                     "🗑 Support links ဖျက်ပါ"),
                ("viewsupport",      "👁 View active support links",
                                     "👁 查看当前支持链接",
                                     "👁 Support links ကြည့်ပါ"),
                ("addsudo",          "⭐ Add a sudo user",
                                     "⭐ 添加 sudo 用户",
                                     "⭐ Sudo user ထည့်ပါ"),
                ("delsudo",          "🗑 Remove a sudo user",
                                     "🗑 移除 sudo 用户",
                                     "🗑 Sudo user ဖယ်ပါ"),
                ("broadcast",        "📢 Broadcast a message",
                                     "📢 广播消息",
                                     "📢 Broadcast"),
                ("maintenance",      "🔧 Toggle maintenance mode",
                                     "🔧 切换维护模式",
                                     "🔧 Maintenance mode"),
                ("reboot",           "🔄 Reboot the bot",
                                     "🔄 重启机器人",
                                     "🔄 Bot restart"),
                ("update",           "⬆️ Update the bot",
                                     "⬆️ 更新机器人",
                                     "⬆️ Update"),
                ("gban",             "🚫 Global-ban a user",
                                     "🚫 全局封禁用户",
                                     "🚫 Gban"),
                ("ungban",           "✅ Remove global ban",
                                     "✅ 解除全局封禁",
                                     "✅ Ungban"),
            ]

            def _make(defs, idx):
                return [BotCommand(c[0], c[idx]) for c in defs]

            try:
                for idx, lang in [(1, "en"), (2, "zh"), (3, "my")]:
                    lc = None if lang == "en" else lang
                    kw = {} if lc is None else {"language_code": lc}

                    # Groups: short command list
                    await self.set_bot_commands(
                        _make(_GROUP_CMDS, idx),
                        scope=BotCommandScopeAllGroupChats(),
                        **kw,
                    )
                    # Private: full general list
                    await self.set_bot_commands(
                        _make(_PRIVATE_CMDS, idx),
                        scope=BotCommandScopeAllPrivateChats(),
                        **kw,
                    )
                    # Default fallback (other contexts)
                    await self.set_bot_commands(
                        _make(_GROUP_CMDS, idx),
                        scope=BotCommandScopeDefault(),
                        **kw,
                    )

                # Owner PM: full list including admin/sudo commands.
                # Use the first OWNER_ID; try each language.
                if config.OWNER_ID:
                    owner_id = config.OWNER_ID[0]
                    for idx, lang in [(1, "en"), (2, "zh"), (3, "my")]:
                        lc = None if lang == "en" else lang
                        kw = {} if lc is None else {"language_code": lc}
                        try:
                            await self.set_bot_commands(
                                _make(_OWNER_PM_CMDS, idx),
                                scope=BotCommandScopeChat(chat_id=owner_id),
                                **kw,
                            )
                        except Exception:
                            pass  # owner may not have started the bot yet

                LOGGER(__name__).info(
                    "Bot command menu registered (group/private/owner scopes, en/zh/my)"
                )
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
