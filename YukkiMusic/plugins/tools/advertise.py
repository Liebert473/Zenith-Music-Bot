#
# /advertise  — public reach/stats card for advertisers.
# Shows serving group chats, total users, tracks played, live voice chats.
# Results are cached for CACHE_TTL seconds to avoid hammering MongoDB.
#

import time

from pyrogram import filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                             InlineKeyboardMarkup, Message)

import config
from config import BANNED_USERS, MUSIC_BOT_NAME
from strings import get_command, get_string
from YukkiMusic import app
from YukkiMusic.utils.database import (get_active_chats,
                                        get_active_video_chats,
                                        get_lang, get_queries,
                                        get_served_chats,
                                        get_served_users)

CACHE_TTL = 300  # seconds (5 min)
_cache: dict = {"data": None, "ts": 0.0}

# ── Localized message templates ─────────────────────────────────────────────
# Placeholders: {bot} {groups} {users} {plays} {live}
_MSG = {
    "en": (
        "📡 **{bot} — Reach Statistics**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🌐  **Serving Group Chats:** `{groups:,}`\n"
        "👥  **Total Bot Users:**     `{users:,}`\n"
        "🎵  **Tracks Played:**       `{plays:,}`\n"
        "🔊  **Live Voice Chats:**    `{live}`\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "_Interested in advertising or promoting your channel / group?\n"
        "Tap **Contact Owner** below._"
    ),
    "cn": (
        "📡 **{bot} — 覆盖统计**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🌐  **服务群组数量：** `{groups:,}`\n"
        "👥  **总用户数量：**   `{users:,}`\n"
        "🎵  **总播放次数：**   `{plays:,}`\n"
        "🔊  **当前语音聊天：** `{live}`\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "_有意在此机器人投放广告或推广您的频道/群组？\n"
        "请点击下方「联系主人」按钮。_"
    ),
    "my": (
        "📡 **[{bot} :: REACH STATS]**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🌐  **[GROUPS SERVED]:**   `{groups:,}`\n"
        "👥  **[USERS ONLINE]:**    `{users:,}`\n"
        "🎵  **[TRACKS PLAYED]:**   `{plays:,}`\n"
        "🔊  **[LIVE STREAMS]:**    `{live}`\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "_Advertisement / promotion လုပ်ချင်ပါက\n"
        "**Contact Owner** ကို နှိပ်ပါ_"
    ),
}

_BTN_CONTACT = {"en": "📩 Contact Owner", "cn": "📩 联系主人", "my": "📩 Owner ကို ဆက်သွယ်ပါ"}
_BTN_REFRESH = {"en": "🔄 Refresh", "cn": "🔄 刷新", "my": "🔄 Refresh"}
_BTN_CLOSE   = {"en": "✖ Close",   "cn": "✖ 关闭",  "my": "✖ ပိတ်ပါ"}


async def _fetch_stats() -> dict:
    """Fetch (or return cached) reach numbers."""
    now = time.monotonic()
    if _cache["data"] is not None and (now - _cache["ts"]) < CACHE_TTL:
        return _cache["data"]
    groups = len(await get_served_chats())
    users  = len(await get_served_users())
    plays  = await get_queries()
    audio_live = len(await get_active_chats())
    video_live = len(await get_active_video_chats())
    live = audio_live + video_live
    data = {"groups": groups, "users": users, "plays": plays, "live": live}
    _cache["data"] = data
    _cache["ts"]   = now
    return data


def _build_keyboard(lang: str) -> InlineKeyboardMarkup:
    lk = lang if lang in _BTN_CONTACT else "en"
    rows: list = []
    if config.OWNER_ID:
        rows.append([
            InlineKeyboardButton(
                text=_BTN_CONTACT[lk],
                user_id=config.OWNER_ID[0],
            )
        ])
    rows.append([
        InlineKeyboardButton(
            text=_BTN_REFRESH[lk],
            callback_data="advertise_refresh",
        ),
        InlineKeyboardButton(
            text=_BTN_CLOSE[lk],
            callback_data="close",
        ),
    ])
    return InlineKeyboardMarkup(rows)


def _build_text(lang: str, stats: dict) -> str:
    lk = lang if lang in _MSG else "en"
    return _MSG[lk].format(bot=MUSIC_BOT_NAME, **stats)


# ── Command handler ──────────────────────────────────────────────────────────

@app.on_message(
    filters.command(["advertise", "reach", "botstats"])
    & (filters.private | filters.group)
    & ~BANNED_USERS
)
async def advertise_cmd(client, message: Message):
    lang = await get_lang(message.chat.id)
    # map repo 'cn' → 'cn' (template key), everything else → 'en' fallback
    lk = lang if lang in _MSG else "en"
    m = await message.reply_text("🔎 _Fetching stats…_")
    try:
        stats = await _fetch_stats()
    except Exception as e:
        return await m.edit_text(f"❌ Failed to fetch stats: {e}")
    await m.edit_text(
        _build_text(lk, stats),
        reply_markup=_build_keyboard(lk),
    )


# ── Refresh callback ─────────────────────────────────────────────────────────

@app.on_callback_query(
    filters.regex("advertise_refresh") & ~BANNED_USERS
)
async def advertise_refresh_cb(client, cb: CallbackQuery):
    lang = await get_lang(cb.message.chat.id)
    lk = lang if lang in _MSG else "en"
    # Force-bust the cache so refresh shows fresh numbers.
    _cache["ts"] = 0.0
    try:
        stats = await _fetch_stats()
    except Exception as e:
        return await cb.answer(f"Error: {e}", show_alert=True)
    try:
        await cb.edit_message_text(
            _build_text(lk, stats),
            reply_markup=_build_keyboard(lk),
        )
    except Exception:
        pass
    try:
        await cb.answer("✅ Refreshed!", show_alert=False)
    except Exception:
        pass


# ── Inline callback triggered from start panel button ───────────────────────

@app.on_callback_query(
    filters.regex("advertise_stats") & ~BANNED_USERS
)
async def advertise_stats_cb(client, cb: CallbackQuery):
    lang = await get_lang(cb.message.chat.id)
    lk = lang if lang in _MSG else "en"
    try:
        await cb.answer()
    except Exception:
        pass
    try:
        stats = await _fetch_stats()
    except Exception as e:
        return await cb.answer(f"Error: {e}", show_alert=True)
    try:
        await cb.edit_message_text(
            _build_text(lk, stats),
            reply_markup=_build_keyboard(lk),
        )
    except Exception:
        pass
