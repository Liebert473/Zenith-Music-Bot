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
    """Group /start panel — compact: commands + settings + links + stats."""
    rows = [
        [
            btn(_["S_B_1"], url=f"https://t.me/{app.username}?start=help"),
            btn(_["S_B_2"], callback_data="settings_helper"),
        ],
    ]
    ch, gr = _support_channel(), _support_group()
    if ch and gr:
        rows.append([
            btn(_["S_B_4"], url=ch),
            btn(_["S_B_3"], url=gr),
        ])
    else:
        if ch:
            rows.append([btn(_["S_B_4"], url=ch)])
        if gr:
            rows.append([btn(_["S_B_3"], url=gr)])
    rows.append([
        btn(_["ADV_BUTTON"], callback_data="advertise_stats",
            style=SUCCESS),
    ])
    return rows


def private_panel(_, BOT_USERNAME, OWNER: Union[bool, int] = None):
    """Private /start panel — clean layout, minimal colors.

    Layout (top → bottom):
      1. Add me to your group       — SUCCESS  (primary CTA)
      2. How to Use? Commands Menu  — default
      3. Channel + Support          — default
      4. Bot Owner                  — DANGER   (distinctive contact)
      5. Bot Reach + Git Repo       — default
      6. Language                   — default
    """
    rows = []

    # ── 1. Primary CTA: Add me to your group ──────────────────────────────
    rows.append([
        btn(_["S_B_5"],
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
            style=SUCCESS),
    ])

    # ── 2. Help menu ──────────────────────────────────────────────────────
    rows.append([
        btn(_["S_B_8"], callback_data="settings_back_helper"),
    ])

    # ── 3. Channel + Support ──────────────────────────────────────────────
    ch, gr = _support_channel(), _support_group()
    if ch and gr:
        rows.append([
            btn(_["S_B_4"], url=ch),
            btn(_["S_B_3"], url=gr),
        ])
    else:
        if ch:
            rows.append([btn(_["S_B_4"], url=ch)])
        if gr:
            rows.append([btn(_["S_B_3"], url=gr)])

    # ── 4. Bot Owner (distinctive contact) ────────────────────────────────
    if OWNER:
        rows.append([
            btn(_["S_B_7"], user_id=OWNER, style=DANGER),
        ])

    # ── 5. Bot Reach + Git Repo ───────────────────────────────────────────
    adv_row = [
        btn(_["ADV_BUTTON"], callback_data="advertise_stats"),
    ]
    if GITHUB_REPO:
        adv_row.append(btn(_["S_B_6"], url=GITHUB_REPO))
    rows.append(adv_row)

    # ── 6. Language ───────────────────────────────────────────────────────
    rows.append([
        btn(_["ST_B_6"], callback_data="LG"),
    ])
    return rows


def private_help_panel(_):
    """Group /help redirect — single URL button pointing to bot PM."""
    return [
        [btn(_["S_B_1"],
             url=f"https://t.me/{app.username}?start=help",
             style=SUCCESS)],
    ]
