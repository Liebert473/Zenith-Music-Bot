"""
Custom emoji ID cache — populated once at startup via init_custom_emoji(client).

Usage
─────
  enhance_text(html_str)     → wraps all _IDS emoji chars in <tg-emoji> tags
  get_id("🎵")               → str document_id for icon_custom_emoji_id, or None
  EM["music"]                → "<tg-emoji emoji-id='…'>🎵</tg-emoji>" (or "🎵")
  em("music")                → same as EM["music"]  (shorthand)

Named-emoji helper (EM / em)
─────────────────────────────
All bot messages that want to show a specific animated emoji should call
em("name") rather than hard-coding the Unicode character.  That way every
language string uses the same glyph AND the same animation, and swapping to
a different document ID only requires changing _EMOJI_CHARS below.

To add a new emoji:
  1. Add  "name": "CHAR"  to _EMOJI_CHARS.
  2. Optionally add  "CHAR": DOC_ID  to _HARDCODED (skips API lookup).
  3. If you want it auto-resolved at startup, add the char to _WANTED.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Dict, Optional

_LOG = logging.getLogger(__name__)

# emoji char → custom-emoji document_id (int), filled at startup
_IDS: Dict[str, int] = {}

# ── Hardcoded custom emoji IDs (user-verified document IDs) ─────────────────
# These bypass the API discovery step so the exact variant is always used.
_HARDCODED: Dict[str, int] = {
    "📌": 6061980265356466673,  # pin — used on the Loop button
}
_IDS.update(_HARDCODED)

# Emoji we want animated in /start, /help, settings.
# Telegram tends to have custom-emoji matches for most of these.
_WANTED = (
    "🎵", "🎶", "🎧", "⚡", "🔥", "✨", "🛸",
    "🎉", "👾", "🤖", "📡", "⭐", "👑", "💎",
    "🌟", "💫", "🎯", "🏆", "🚀", "❤️",
    "🔮", "💥", "🌊", "🎨", "📨", "🌐",
    "🛡️", "🎮", "✅", "❌", "💡", "⚙️",
)


async def init_custom_emoji(client) -> None:
    """Resolve every wanted emoji char to a custom-emoji document_id
    via messages.searchCustomEmoji.

    Each lookup picks the first match (Telegram orders by relevance/popularity).
    Premium-only emoji are still cached — non-Premium viewers see the
    fallback char from the <tg-emoji> tag.
    """
    from pyrogram.raw.functions.messages import SearchCustomEmoji

    fetched = 0
    skipped = 0
    for emoji_char in _WANTED:
        if emoji_char in _HARDCODED:   # keep the user-verified ID, skip API
            continue
        try:
            result = await client.invoke(
                SearchCustomEmoji(emoticon=emoji_char, hash=0)
            )
            ids = getattr(result, "document_id", None)
            if ids:
                _IDS[emoji_char] = ids[0]
                fetched += 1
            else:
                skipped += 1
        except Exception as exc:
            _LOG.debug("custom emoji search '%s' failed: %s", emoji_char, exc)
            skipped += 1

    _LOG.info(
        "Custom emoji: %d resolved, %d no-match (out of %d wanted)",
        fetched, skipped, len(_WANTED),
    )


def get_id(emoji: str) -> Optional[str]:
    """Return str(document_id) for icon_custom_emoji_id buttons, or None."""
    did = _IDS.get(emoji)
    return str(did) if did is not None else None


def enhance_text(text: str) -> str:
    """Wrap known custom emoji in HTML text with <tg-emoji> animation tags.

    Safe to call once per string before sending — does not double-wrap
    since YAML source strings never contain <tg-emoji>.
    Premium clients see animated; others see the fallback char.
    """
    if not _IDS:
        return text
    for emoji, doc_id in _IDS.items():
        if emoji in text:
            text = text.replace(
                emoji,
                f'<tg-emoji emoji-id="{doc_id}">{emoji}</tg-emoji>',
            )
    return text


# ── Named-emoji map ──────────────────────────────────────────────────────────
# Map a semantic name → the Unicode character used across ALL language strings.
# Changing a char here changes it everywhere at once.
# When _IDS has a document_id for the char, em() returns a full <tg-emoji> tag.

_EMOJI_CHARS: Dict[str, str] = {
    # ── Music / playback ────────────────────────────────────────────────────
    "music":        "🎵",
    "notes":        "🎶",
    "headphones":   "🎧",
    "play":         "▶️",
    "pause":        "⏸",
    "skip":         "⏭",
    "stop":         "⏹",
    "loop":         "🔁",
    "shuffle":      "🔀",
    "mute":         "🔇",
    "volume":       "🔊",
    # ── Status / UI ──────────────────────────────────────────────────────────
    "ok":           "✅",
    "error":        "❌",
    "warning":      "⚠️",
    "info":         "ℹ️",
    "loading":      "⏳",
    "bolt":         "⚡",
    "fire":         "🔥",
    "star":         "⭐",
    "pin":          "📌",
    "sparkles":     "✨",
    "rocket":       "🚀",
    "crown":        "👑",
    "diamond":      "💎",
    "globe":        "🌐",
    "bot":          "🤖",
    "alien":        "👾",
    "ufo":          "🛸",
    "satellite":    "📡",
    "settings":     "⚙️",
    "shield":       "🛡️",
    "bulb":         "💡",
    "mail":         "📨",
    "party":        "🎉",
    "trophy":       "🏆",
    "target":       "🎯",
    "gem":          "🌟",
    "sparkle":      "💫",
    "heart":        "❤️",
    "crystal":      "🔮",
    "explosion":    "💥",
    "wave":         "🌊",
    "palette":      "🎨",
    "gamepad":      "🎮",
}


def em(name: str) -> str:
    """Return the animated <tg-emoji> tag for the named emoji, or the plain char.

    Example:
        em("music")  →  '<tg-emoji emoji-id="5046509860389126442">🎵</tg-emoji>'
                         (or just "🎵" before startup finishes)

    Use this in any bot message string where you want a consistent, potentially
    animated emoji across all languages:
        await message.reply_text(f"{em('ok')} Done!")
    """
    char = _EMOJI_CHARS.get(name, name)   # fall back to name itself if unknown
    doc_id = _IDS.get(char)
    if doc_id:
        return f'<tg-emoji emoji-id="{doc_id}">{char}</tg-emoji>'
    return char


# Pre-built dict — resolved lazily (refreshed after init_custom_emoji runs).
# Access via EM["music"] or em("music") — they return the same value.
class _EMProxy(dict):
    """Dict-like that calls em() on key access so values stay fresh after init."""
    def __getitem__(self, key: str) -> str:
        return em(key)
    def __contains__(self, key: object) -> bool:
        return key in _EMOJI_CHARS

EM: Dict[str, str] = _EMProxy()
# ─────────────────────────────────────────────────────────────────────────────
