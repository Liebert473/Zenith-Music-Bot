"""
Async HTTP Bot API helpers that unlock Bot API 9.4 button features:
  - InlineKeyboardButton.style            ("primary" | "success" | "danger")
  - InlineKeyboardButton.icon_custom_emoji_id

These are not yet in pyrogram 2.0.106 (MTProto layer 158), so we call
api.telegram.org directly via aiohttp alongside the existing pyrogram client.

Button row format  List[List[dict]]:
    [
        [btn("▶ Play",  callback_data="play",  style=SUCCESS, icon_emoji="🎵")],
        [btn("Support", url="https://t.me/…", style=PRIMARY, icon_emoji="📨")],
    ]

Public helpers
--------------
  btn(text, *, callback_data, url, user_id, style, icon_emoji) → dict
  to_markup(rows)          → pyrogram InlineKeyboardMarkup (strips 9.4 fields)
  send_message(…)          → message_id | None
  send_photo(…)            → message_id | None
  edit_message(…)          → bool
  delete_message(…)        → bool

Style constants:  PRIMARY  SUCCESS  DANGER
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

import aiohttp
import config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

_LOG = logging.getLogger(__name__)
_API = f"https://api.telegram.org/bot{config.BOT_TOKEN}"
_TIMEOUT = aiohttp.ClientTimeout(total=15)

# ── Style constants ──────────────────────────────────────────────────────────
PRIMARY = "primary"   # blue (Telegram default button colour)
SUCCESS = "success"   # green
DANGER  = "danger"    # red


# ── Button factory ───────────────────────────────────────────────────────────
def btn(
    text: str,
    *,
    callback_data: str = None,
    url: str = None,
    user_id: int = None,
    style: str = None,
    icon_emoji: str = None,
) -> dict:
    """Build a colored button dict for use with tg_send helpers."""
    b: dict = {"text": text}
    if callback_data is not None:
        b["callback_data"] = callback_data
    if url is not None:
        b["url"] = url
    if user_id is not None:
        # HTTP Bot API has no native user_id field; deep-link works everywhere
        b["url"] = f"tg://user?id={user_id}"
    if style is not None:
        b["style"] = style
    if icon_emoji is not None:
        from .custom_emoji import get_id
        eid = get_id(icon_emoji)
        if eid:
            b["icon_custom_emoji_id"] = eid
    return b


# ── Pyrogram compat ──────────────────────────────────────────────────────────
def to_markup(rows: List[List[dict]]) -> InlineKeyboardMarkup:
    """Convert colored row dicts → pyrogram InlineKeyboardMarkup.

    Strips style / icon_custom_emoji_id which pyrogram 2.0.106 doesn't
    support.  Used for group messages / new-chat-member events that still
    go through pyrogram's MTProto path.
    """
    out = []
    for row in rows:
        r = []
        for b in row:
            text = b.get("text", "")
            if "callback_data" in b:
                r.append(InlineKeyboardButton(
                    text=text, callback_data=b["callback_data"]
                ))
            elif "url" in b:
                r.append(InlineKeyboardButton(text=text, url=b["url"]))
        if r:
            out.append(r)
    return InlineKeyboardMarkup(out)


# ── Internal HTTP helper ─────────────────────────────────────────────────────
async def _post(endpoint: str, payload: dict) -> dict:
    try:
        async with aiohttp.ClientSession(timeout=_TIMEOUT) as sess:
            async with sess.post(f"{_API}/{endpoint}", json=payload) as r:
                return await r.json()
    except Exception as exc:
        _LOG.warning("tg_send.%s failed: %s", endpoint, exc)
        return {"ok": False, "description": str(exc)}


# ── Public send / edit helpers ───────────────────────────────────────────────
async def send_message(
    chat_id: int,
    text: str,
    rows: List[List[dict]],
    *,
    parse_mode: str = "HTML",
    reply_to: int = None,
    disable_preview: bool = False,
) -> Optional[int]:
    """Send a text message with colored inline keyboard.  Returns message_id.

    Link previews are ENABLED by default (disable_preview=False) so links in
    /start custom text and other messages render their preview card.
    Callers building dense UI panels (e.g. /help) can pass disable_preview=True.
    """
    payload: dict = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "reply_markup": {"inline_keyboard": rows},
        "disable_web_page_preview": disable_preview,
    }
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    res = await _post("sendMessage", payload)
    if res.get("ok"):
        return res["result"]["message_id"]
    _LOG.warning("sendMessage error: %s", res.get("description"))
    return None


async def send_photo(
    chat_id: int,
    photo: str,
    caption: str,
    rows: List[List[dict]],
    *,
    parse_mode: str = "HTML",
    reply_to: int = None,
) -> Optional[int]:
    """Send a photo+caption with colored inline keyboard.  Returns message_id."""
    payload: dict = {
        "chat_id": chat_id,
        "photo": photo,
        "caption": caption,
        "parse_mode": parse_mode,
        "reply_markup": {"inline_keyboard": rows},
    }
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    res = await _post("sendPhoto", payload)
    if res.get("ok"):
        return res["result"]["message_id"]
    _LOG.warning("sendPhoto error: %s", res.get("description"))
    return None


async def edit_message(
    chat_id: int,
    message_id: int,
    text: str,
    rows: List[List[dict]],
    *,
    parse_mode: str = "HTML",
    disable_preview: bool = True,
) -> bool:
    """Edit a message's text and keyboard.  Returns success bool.

    Defaults to disable_preview=True since edits typically happen on dense
    UI panels (/help pagination, settings) where a preview card would
    disrupt the layout.
    """
    res = await _post("editMessageText", {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode,
        "reply_markup": {"inline_keyboard": rows},
        "disable_web_page_preview": disable_preview,
    })
    if not res.get("ok"):
        _LOG.warning("editMessageText error: %s", res.get("description"))
    return res.get("ok", False)


async def edit_reply_markup(
    chat_id: int,
    message_id: int,
    rows: List[List[dict]],
) -> bool:
    """Replace ONLY the inline keyboard of a message via HTTP Bot API.

    Keeps the existing text/caption/photo untouched.
    Supports Bot API 9.4 style + icon_custom_emoji_id — use this instead of
    pyrogram's edit_message_reply_markup when you want colored / icon buttons.
    Errors are logged at DEBUG level (non-fatal: the message is still visible).
    """
    res = await _post("editMessageReplyMarkup", {
        "chat_id": chat_id,
        "message_id": message_id,
        "reply_markup": {"inline_keyboard": rows},
    })
    if not res.get("ok"):
        _LOG.debug("editMessageReplyMarkup: %s", res.get("description"))
    return res.get("ok", False)


async def delete_message(chat_id: int, message_id: int) -> bool:
    """Delete a message.  Returns success bool."""
    res = await _post("deleteMessage", {
        "chat_id": chat_id,
        "message_id": message_id,
    })
    return res.get("ok", False)
