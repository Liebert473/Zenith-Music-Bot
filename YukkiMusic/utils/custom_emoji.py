"""
Custom emoji ID cache — populated once at startup via init_custom_emoji(client).

Usage:
    enhance_text(html_str) → wraps selected emoji in <tg-emoji> tags
    get_id("🎵")           → str document_id for icon_custom_emoji_id, or None
"""
from __future__ import annotations

import logging
from typing import Dict, Optional

_LOG = logging.getLogger(__name__)

# emoji char → document_id (int), filled at startup
_IDS: Dict[str, int] = {}

# Emoji we want to animate in UI messages / button icons.
# Must be a subset of what Telegram's built-in animated sets contain.
_WANTED = frozenset({
    "🎵", "🎶", "🎧", "⚡", "🔥", "✨", "🛸",
    "🎉", "👾", "🤖", "📡", "⭐", "👑", "💎",
    "🌟", "💫", "🎯", "🏆", "🚀", "❤️", "💙",
    "💚", "🔮", "💥", "🌊", "🎨", "📨", "🌐",
})

_STICKER_SETS = None  # lazy-imported to avoid circular at module level


async def init_custom_emoji(client) -> None:
    """Fetch custom emoji document IDs from Telegram's built-in animated sets."""
    from pyrogram.raw.functions.messages import GetStickerSet
    from pyrogram.raw.types import (
        InputStickerSetAnimatedEmoji,
        InputStickerSetEmojiGenericAnimations,
    )

    sets = [
        InputStickerSetAnimatedEmoji(),
        InputStickerSetEmojiGenericAnimations(),
    ]

    fetched = 0
    for sticker_set in sets:
        try:
            result = await client.invoke(
                GetStickerSet(stickerset=sticker_set, hash=0)
            )
            for doc in result.documents:
                for attr in doc.attributes:
                    alt = getattr(attr, "alt", None)
                    if alt and alt in _WANTED and alt not in _IDS:
                        _IDS[alt] = doc.id
                        fetched += 1
        except Exception as exc:
            _LOG.warning(
                "custom emoji fetch skipped [%s]: %s",
                type(sticker_set).__name__, exc,
            )

    _LOG.info("Custom emoji: %d IDs loaded (%d wanted)", fetched, len(_WANTED))


def get_id(emoji: str) -> Optional[str]:
    """Return str(document_id) for use in icon_custom_emoji_id, or None."""
    did = _IDS.get(emoji)
    return str(did) if did is not None else None


def enhance_text(text: str) -> str:
    """Wrap known animated emoji in HTML text with <tg-emoji> tags.

    Safe to call once per string before sending.  Does NOT double-wrap
    because YAML source strings never contain <tg-emoji> tags.
    Premium clients see the animated version; others see the fallback char.
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
