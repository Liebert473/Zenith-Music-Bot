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
            # Localized command menu. Telegram picks the version that
            # matches the user's Telegram client language; the no-
            # language_code call is the fallback for everyone else.
            # (cmd, en, zh, my) — keep descriptions <256 chars.
            _CMDS = [
                # ── Core playback ──
                ("play",        "🎵 Play a song by name or URL",
                                "🎵 通过名称或链接播放歌曲",
                                "🎵 သီချင်းအမည် သို့မဟုတ် URL ဖြင့် ဖွင့်ပါ"),
                ("vplay",       "🎥 Play a video by name or URL",
                                "🎥 通过名称或链接播放视频",
                                "🎥 ဗီဒီယိုကို အမည် သို့မဟုတ် URL ဖြင့် ဖွင့်ပါ"),
                ("playforce",   "⚡ Force-play (skip current, keep queue)",
                                "⚡ 强制播放（跳过当前曲目，保留队列）",
                                "⚡ Force-play [လက်ရှိ track ကို ကျော်၊ queue မထိ]"),
                ("song",        "💾 Download a song from YouTube (PM only)",
                                "💾 从 YouTube 下载歌曲（仅私聊）",
                                "💾 YouTube မှ song ဆွဲချ [PM သာ]"),
                # ── Playback control ──
                ("pause",       "⏸ Pause the current track",
                                "⏸ 暂停当前曲目",
                                "⏸ လက်ရှိ track ကို ခဏရပ်ပါ"),
                ("resume",      "▶️ Resume the paused track",
                                "▶️ 恢复播放",
                                "▶️ ပြန်ဖွင့်ပါ"),
                ("skip",        "⏭ Skip to the next track",
                                "⏭ 跳到下一首",
                                "⏭ နောက် track သို့ ကျော်ပါ"),
                ("end",         "⏹ Stop playback and leave voice chat",
                                "⏹ 停止播放并退出语音聊天",
                                "⏹ Stream ရပ်ပြီး voice chat မှ ထွက်ပါ"),
                ("mute",        "🔇 Mute the voice chat",
                                "🔇 静音语音聊天",
                                "🔇 Voice chat ကို mute ပြုလုပ်ပါ"),
                ("unmute",      "🔊 Unmute the voice chat",
                                "🔊 取消静音",
                                "🔊 Voice chat ကို unmute ပြုလုပ်ပါ"),
                ("loop",        "🔁 Loop the current track",
                                "🔁 循环播放当前曲目",
                                "🔁 လက်ရှိ track ကို loop ပြုလုပ်ပါ"),
                ("seek",        "⏩ Seek forward by N seconds",
                                "⏩ 快进 N 秒",
                                "⏩ N စက္ကန့် ရှေ့သို့ ရွှေ့ပါ"),
                ("seekback",    "⏪ Seek backward by N seconds",
                                "⏪ 后退 N 秒",
                                "⏪ N စက္ကန့် နောက်သို့ ပြန်ရွှေ့ပါ"),
                ("shuffle",     "🎲 Shuffle the queue",
                                "🎲 随机播放队列",
                                "🎲 Queue ကို shuffle ပြုလုပ်ပါ"),
                ("queue",       "📑 Show the current queue",
                                "📑 显示当前播放队列",
                                "📑 လက်ရှိ queue ကို ပြသပါ"),
                # ── Modes & settings ──
                ("playmode",    "🎛️ Change play mode (direct / inline)",
                                "🎛️ 更改播放模式（直接 / 内联）",
                                "🎛️ Play mode ပြောင်းပါ [direct / inline]"),
                ("settings",    "⚙️ Open the bot settings panel",
                                "⚙️ 打开机器人设置面板",
                                "⚙️ Bot ၏ settings panel ကို ဖွင့်ပါ"),
                ("language",    "🌐 Change the bot language",
                                "🌐 更改机器人语言",
                                "🌐 Bot ၏ ဘာသာစကား ပြောင်းပါ"),
                ("channelplay", "📡 Link this group to a channel",
                                "📡 将此群组链接到频道",
                                "📡 ဤ group ကို channel တစ်ခုနှင့် ချိတ်ဆက်ပါ"),
                # ── Auth & admin ──
                ("auth",        "🎩 Add a user to AUL (auth users)",
                                "🎩 将用户添加到 AUL（授权用户名单）",
                                "🎩 AUL ထဲသို့ user တစ်ဦး ထည့်ပါ"),
                ("unauth",      "🗑 Remove a user from AUL",
                                "🗑 从 AUL 中移除用户",
                                "🗑 AUL မှ user တစ်ဦးကို ဖယ်ရှားပါ"),
                ("authusers",   "📋 Show AUL",
                                "📋 显示授权用户名单",
                                "📋 AUL ကို ပြသပါ"),
                ("admincache",  "🔄 Reload admin cache",
                                "🔄 重新加载管理员缓存",
                                "🔄 Admin cache ကို ပြန် sync ပါ"),
                ("reload",      "🔄 Alias for /admincache",
                                "🔄 /admincache 的别名",
                                "🔄 /admincache ၏ alias"),
                # ── Info ──
                ("help",        "📜 Command reference",
                                "📜 命令参考",
                                "📜 Commands ၏ စာရင်း"),
                ("start",       "🛸 Boot the bot",
                                "🛸 启动机器人",
                                "🛸 Bot ကို စတင်ပါ"),
                ("ping",        "⚡ Latency / system telemetry",
                                "⚡ 延迟 / 系统遥测",
                                "⚡ Latency နှင့် system telemetry"),
                ("lyrics",      "📖 Search song lyrics",
                                "📖 搜索歌词",
                                "📖 သီချင်း၏ lyrics ရှာပါ"),
                ("playlist",    "💾 Your saved server-side playlist",
                                "💾 您保存的服务器端播放列表",
                                "💾 သင်၏ server-side playlist"),
                ("gstats",      "📊 Global / personal stats",
                                "📊 全局 / 个人统计",
                                "📊 Global / Personal stats"),
            ]
            try:
                # tuple index 1=en (default/fallback), 2=zh, 3=my
                for idx, lang in [(1, "en"), (2, "zh"), (3, "my")]:
                    cmds = [BotCommand(c[0], c[idx]) for c in _CMDS]
                    if lang == "en":
                        # Default scope, no language_code — fallback for
                        # everyone whose client language isn't zh/my.
                        await self.set_bot_commands(cmds)
                    else:
                        await self.set_bot_commands(
                            cmds, language_code=lang
                        )
                LOGGER(__name__).info(
                    "Bot command menu registered (en/zh/my)"
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
