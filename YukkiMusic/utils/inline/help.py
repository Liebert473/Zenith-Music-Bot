#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from YukkiMusic import app
from YukkiMusic.utils.tg_send import DANGER, PRIMARY, SUCCESS, btn

# All builders return List[List[dict]] (colored row format).
# • Pass directly to tg_send.send_message / edit_message  →  colors + icons.
# • Wrap with tg_send.to_markup(rows) for pyrogram InlineKeyboardMarkup.


def help_pannel(_, START=None, is_sudo: bool = False):
    """Main help category grid."""
    rows = [
        [
            btn(_["H_B_1"], callback_data="help_callback hb1",
                style=PRIMARY, icon_emoji="⚡"),
            btn(_["H_B_2"], callback_data="help_callback hb2",
                style=SUCCESS, icon_emoji="🎵"),
        ],
        [
            btn(_["H_B_3"], callback_data="help_callback hb3",
                style=PRIMARY, icon_emoji="🤖"),
            btn(_["H_B_4"], callback_data="help_callback hb4",
                style=SUCCESS, icon_emoji="🛸"),
        ],
    ]
    if is_sudo:
        rows.append([
            btn(_["H_B_6"], callback_data="help_callback hb5",
                style=DANGER, icon_emoji="👑"),
        ])
    if START:
        rows.append([
            btn(_["BACK_BUTTON"],    callback_data="settingsback_helper",
                style=PRIMARY),
            btn(_["CLOSEMENU_BUTTON"], callback_data="close",
                style=DANGER),
        ])
    else:
        rows.append([
            btn(_["CLOSEMENU_BUTTON"], callback_data="close",
                style=DANGER),
        ])
    return rows


def help_back_markup(_, next_page: str = None, prev_page: str = None):
    """Back + Close row for individual help sections; optional Prev / Next nav."""
    rows = []
    nav = []
    if prev_page:
        nav.append(btn("◀ Prev", callback_data=prev_page, style=PRIMARY))
    if next_page:
        nav.append(btn("Next ▶", callback_data=next_page, style=PRIMARY))
    if nav:
        rows.append(nav)
    rows.append([
        btn(_["BACK_BUTTON"],  callback_data="settings_back_helper",
            style=PRIMARY),
        btn(_["CLOSE_BUTTON"], callback_data="close",
            style=DANGER),
    ])
    return rows


def private_help_panel(_):
    """Group /help → redirect PM button."""
    return [
        [btn(_["S_B_1"],
             url=f"https://t.me/{app.username}?start=help",
             style=SUCCESS)],
    ]
