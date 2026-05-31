"""
Custom emoji ID cache — populated once at startup via init_custom_emoji(client).

The previous implementation fetched regular animated sticker sets
(InputStickerSetAnimatedEmoji) — those documents are NOT custom emoji
type, so their IDs don't render in <tg-emoji> tags.

This version uses messages.searchCustomEmoji which returns actual
custom-emoji document IDs that Telegram clients animate inline in text.

Usage:
    enhance_text(html_str) → wraps selected emoji in <tg-emoji> tags
    get_id("🎵")           → str document_id for icon_custom_emoji_id, or None
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
