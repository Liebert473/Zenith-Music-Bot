#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from typing import Union

from config import GITHUB_REPO, SUPPORT_CHANNEL, SUPPORT_GROUP
from YukkiMusic import app
from YukkiMusic.utils.tg_send import PRIMARY, SUCCESS, DANGER, btn

# ── Owner-override support-link cache ────────────────────────────────────────
_owner_links_cache = {
    "support_group": None,
    "support_channel": None,
}


def update_owner_links_cache(*, support_group=None, support_channel=None):
    if support_group is not None:
        _owner_links_cache["support_group"] = support_group or None
    if support_channel is not None:
        _owner_links_cache["support_channel"] = support_channel or None


def _resolve(key: str, env_default):
    return _owner_links_cache.get(key) or env_default


async def load_owner_links_cache():
    from YukkiMusic.utils.database import get_owner_links
    try:
        doc = await get_owner_links()
    except Exception:
        return
    _owner_links_cache["support_group"] = doc.get("support_group")
    _owner_links_cache["support_channel"] = doc.get("support_channel")


def _support_group():
    return _resolve("support_group", SUPPORT_GROUP)


def _support_channel():
    return _resolve("support_channel", SUPPORT_CHANNEL)


# ── Button builders ───────────────────────────────────────────────────────────
# All builders return List[List[dict]] (colored row format).
# • Pass directly to tg_send.send_message / tg_send.send_photo for HTTP API.
# • Wrap with tg_send.to_markup(rows) for pyrogram InlineKeyboardMarkup.


def start_pannel(_):
    """Group /start panel — compact command+settings row + support links."""
    rows = [
        [
            btn(_["S_B_1"], url=f"https://t.me/{app.username}?start=help",
                style=SUCCESS, icon_emoji="🎵"),
            btn(_["S_B_2"], callback_data="settings_helper",
                style=PRIMARY, icon_emoji="⚡"),
        ],
    ]
    ch, gr = _support_channel(), _support_group()
    if ch and gr:
        rows.append([
            btn(_["S_B_4"], url=ch, style=PRIMARY, icon_emoji="📡"),
            btn(_["S_B_3"], url=gr, style=PRIMARY, icon_emoji="📨"),
        ])
    else:
        if ch:
            rows.append([btn(_["S_B_4"], url=ch, style=PRIMARY, icon_emoji="📡")])
        if gr:
            rows.append([btn(_["S_B_3"], url=gr, style=PRIMARY, icon_emoji="📨")])
    rows.append([
        btn(_["ADV_BUTTON"], callback_data="advertise_stats",
            style=SUCCESS, icon_emoji="⭐"),
    ])
    return rows


def private_panel(_, BOT_USERNAME, OWNER: Union[bool, int] = None):
    """Private /start panel — full feature set."""
    rows = [
        [btn(_["S_B_8"], callback_data="settings_back_helper",
             style=SUCCESS, icon_emoji="🎵")],
    ]
    ch, gr = _support_channel(), _support_group()
    if ch and gr:
        rows.append([
            btn(_["S_B_4"], url=ch, style=PRIMARY, icon_emoji="📡"),
            btn(_["S_B_3"], url=gr, style=PRIMARY, icon_emoji="📨"),
        ])
    else:
        if ch:
            rows.append([btn(_["S_B_4"], url=ch, style=PRIMARY, icon_emoji="📡")])
        if gr:
            rows.append([btn(_["S_B_3"], url=gr, style=PRIMARY, icon_emoji="📨")])

    rows.append([
        btn(_["S_B_5"],
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
            style=SUCCESS, icon_emoji="🛸"),
    ])

    if GITHUB_REPO and OWNER:
        rows.append([
            btn(_["S_B_7"], user_id=OWNER, style=DANGER, icon_emoji="👑"),
            btn(_["S_B_6"], url=GITHUB_REPO, style=PRIMARY, icon_emoji="💎"),
        ])
    else:
        if GITHUB_REPO:
            rows.append([btn(_["S_B_6"], url=GITHUB_REPO,
                             style=PRIMARY, icon_emoji="💎")])
        if OWNER:
            rows.append([btn(_["S_B_7"], user_id=OWNER,
                             style=DANGER, icon_emoji="👑")])

    rows.append([
        btn(_["ADV_BUTTON"], callback_data="advertise_stats",
            style=SUCCESS, icon_emoji="⭐"),
    ])
    rows.append([
        btn(_["ST_B_6"], callback_data="LG", style=PRIMARY),
    ])
    return rows


def private_help_panel(_):
    """Group /help redirect — single URL button pointing to bot PM."""
    return [
        [btn(_["S_B_1"],
             url=f"https://t.me/{app.username}?start=help",
             style=SUCCESS, icon_emoji="🎵")],
    ]
