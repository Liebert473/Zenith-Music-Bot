"""
Custom emoji registry — IDs are provided manually; there is no API lookup.

How to add a new animated emoji
────────────────────────────────
1.  Find the document_id (e.g. via @stickers bot ➜ Custom Emoji ➜ Details,
    or the Telegram client emoji picker "copy link").
2.  Add an entry to _IDS:
        "CHAR": DOCUMENT_ID_AS_INT,
    e.g.  "🎵": 5046509860389126442,
3.  Optionally give it a semantic name in _EMOJI_CHARS so you can reference
    it by name instead of by Unicode character:
        "music": "🎵",

Public API
──────────
  enhance_text(html)   → replace plain emoji chars with <tg-emoji> tags
                          (skips chars already inside any existing tag)
  get_id("🎵")         → str doc-id for InlineKeyboardButton.icon_custom_emoji_id
  em("music")          → '<tg-emoji emoji-id="…">🎵</tg-emoji>'  or  "🎵"
  EM["music"]          → same (dict-like proxy, live-resolves per access)
"""
from __future__ import annotations

import re
import logging
from typing import Dict, Optional

_LOG = logging.getLogger(__name__)

# ── Emoji ID table (user-maintained) ────────────────────────────────────────
# Map Unicode emoji char → Telegram custom-emoji document_id (int).
# Leave the dict sparse — chars with no entry fall back to plain Unicode.
_IDS: Dict[str, int] = {
    "📌": 6061980265356466673,   # pin / loop
    # Add more as you get them, e.g.:
    # "🎵": 5046509860389126442,
    # "⚡": 5199885118214255386,
    # "🔥": 5199885118214255386,
}

# ── Semantic name → Unicode char ─────────────────────────────────────────────
# All bot messages should reference emoji by name so a single entry change
# propagates everywhere.  Add names as needed.
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
    "glowing_star": "🌟",
    "dizzy":        "💫",
    "heart":        "❤️",
    "crystal":      "🔮",
    "explosion":    "💥",
    "wave":         "🌊",
    "palette":      "🎨",
    "gamepad":      "🎮",
}

# Pre-compiled: match an emoji char that is NOT the fallback char inside an
# existing <tg-emoji> or <emoji> closing tag, i.e. not immediately followed
# by </tg-emoji> or </emoji>.  This prevents double-wrapping.
_CLOSE_TAG_RE = re.compile(r'</(?:tg-)?emoji>')


def enhance_text(text: str) -> str:
    """Wrap known emoji chars with <tg-emoji emoji-id="…"> tags.

    - Only wraps chars that have a document_id in _IDS.
    - Skips chars already inside an existing <tg-emoji> or <emoji> tag
      (no double-wrapping).
    - Falls back to plain Unicode for any char whose ID is not in _IDS.
    - Safe to call multiple times on the same string.
    """
    if not text or not _IDS:
        return text
    for char, doc_id in _IDS.items():
        if char not in text:
            continue
        replacement = f'<tg-emoji emoji-id="{doc_id}">{char}</tg-emoji>'
        if replacement in text:
            continue                         # already present — skip
        # Replace only occurrences NOT immediately followed by a closing tag
        # (those are fallback chars inside an existing custom-emoji tag).
        text = re.sub(
            re.escape(char) + r'(?!</(?:tg-)?emoji>)',
            replacement,
            text,
        )
    return text


def get_id(emoji: str) -> Optional[str]:
    """Return the str document_id for use as icon_custom_emoji_id, or None."""
    did = _IDS.get(emoji)
    return str(did) if did is not None else None


def em(name: str) -> str:
    """Return the animated <tg-emoji> tag for a named emoji, or the plain char.

    If the ID is not yet in _IDS the plain Unicode character is returned so
    messages always display something sensible.

    Usage anywhere in bot code:
        f"{em('ok')} Saved!"
        f"{em('music')} Now playing…"
    """
    char = _EMOJI_CHARS.get(name, name)   # unknown name → use the name itself
    doc_id = _IDS.get(char)
    if doc_id:
        return f'<tg-emoji emoji-id="{doc_id}">{char}</tg-emoji>'
    return char


class _EMProxy(dict):
    """Live-resolving dict-like so EM["music"] stays fresh after _IDS changes."""
    def __getitem__(self, key: str) -> str:
        return em(key)

    def __contains__(self, key: object) -> bool:
        return key in _EMOJI_CHARS

    def get(self, key: str, default: str = "") -> str:   # type: ignore[override]
        return em(key) if key in _EMOJI_CHARS else default


EM: Dict[str, str] = _EMProxy()
