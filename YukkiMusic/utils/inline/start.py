#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from typing import Union

from pyrogram.types import InlineKeyboardButton

from config import GITHUB_REPO, SUPPORT_CHANNEL, SUPPORT_GROUP
from YukkiMusic import app


# Module-level cache for owner-overridden support links. Populated at
# bot startup by load_owner_links_cache() and live-mutated by the
# /setsupport... owner commands. Falls back to env config when empty.
_owner_links_cache = {
    "support_group": None,
    "support_channel": None,
}


def update_owner_links_cache(*, support_group=None, support_channel=None):
    """Live cache update; called by owner /setsupport* commands and
    by the async loader at startup."""
    if support_group is not None:
        _owner_links_cache["support_group"] = support_group or None
    if support_channel is not None:
        _owner_links_cache["support_channel"] = support_channel or None


def _resolve(key: str, env_default):
    """Owner override wins; env config is the fallback."""
    return _owner_links_cache.get(key) or env_default


async def load_owner_links_cache():
    """Pull current overrides from MongoDB into the in-process cache.
    Call once at startup after the database is reachable."""
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


def start_pannel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?start=help",
            ),
            InlineKeyboardButton(
                text=_["S_B_2"], callback_data="settings_helper"
            ),
        ],
    ]
    ch, gr = _support_channel(), _support_group()
    if ch and gr:
        buttons.append(
            [
                InlineKeyboardButton(text=_["S_B_4"], url=f"{ch}"),
                InlineKeyboardButton(text=_["S_B_3"], url=f"{gr}"),
            ]
        )
    else:
        if ch:
            buttons.append([
                InlineKeyboardButton(text=_["S_B_4"], url=f"{ch}")
            ])
        if gr:
            buttons.append([
                InlineKeyboardButton(text=_["S_B_3"], url=f"{gr}")
            ])
    # Advertiser-facing reach stats button
    buttons.append([
        InlineKeyboardButton(
            text=_["ADV_BUTTON"],
            callback_data="advertise_stats",
        )
    ])
    return buttons


def private_panel(_, BOT_USERNAME, OWNER: Union[bool, int] = None):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_8"], callback_data="settings_back_helper"
            )
        ]
    ]
    ch, gr = _support_channel(), _support_group()
    if ch and gr:
        buttons.append(
            [
                InlineKeyboardButton(text=_["S_B_4"], url=f"{ch}"),
                InlineKeyboardButton(text=_["S_B_3"], url=f"{gr}"),
            ]
        )
    else:
        if ch:
            buttons.append([
                InlineKeyboardButton(text=_["S_B_4"], url=f"{ch}")
            ])
        if gr:
            buttons.append([
                InlineKeyboardButton(text=_["S_B_3"], url=f"{gr}")
            ])
    buttons.append(
        [
            InlineKeyboardButton(
                text=_["S_B_5"],
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
            )
        ]
    )
    if GITHUB_REPO and OWNER:
        buttons.append(
            [
                InlineKeyboardButton(text=_["S_B_7"], user_id=OWNER),
                InlineKeyboardButton(text=_["S_B_6"], url=f"{GITHUB_REPO}"),
            ]
        )
    else:
        if GITHUB_REPO:
            buttons.append([
                InlineKeyboardButton(text=_["S_B_6"], url=f"{GITHUB_REPO}")
            ])
        if OWNER:
            buttons.append([
                InlineKeyboardButton(text=_["S_B_7"], user_id=OWNER)
            ])
    buttons.append([
        InlineKeyboardButton(
            text=_["ADV_BUTTON"],
            callback_data="advertise_stats",
        )
    ])
    buttons.append(
        [InlineKeyboardButton(text=_["ST_B_6"], callback_data="LG")]
    )
    return buttons
