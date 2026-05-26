#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from YukkiMusic import app


def help_pannel(_, START: Union[bool, int] = None, is_sudo: bool = False):
    first = [
        InlineKeyboardButton(
            text=_["CLOSEMENU_BUTTON"], callback_data=f"close"
        )
    ]
    second = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data=f"settingsback_helper",
        ),
        InlineKeyboardButton(
            text=_["CLOSEMENU_BUTTON"], callback_data=f"close"
        ),
    ]
    mark = second if START else first
    rows = [
        [
            InlineKeyboardButton(
                text=_["H_B_1"],
                callback_data="help_callback hb1",
            ),
            InlineKeyboardButton(
                text=_["H_B_2"],
                callback_data="help_callback hb2",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["H_B_3"],
                callback_data="help_callback hb3",
            ),
            InlineKeyboardButton(
                text=_["H_B_4"],
                callback_data="help_callback hb4",
            ),
        ],
    ]
    # Only owner + sudo users see the SudoUser commands button
    if is_sudo:
        rows.append([
            InlineKeyboardButton(
                text=_["H_B_6"],
                callback_data="help_callback hb5",
            ),
        ])
    rows.append(mark)
    return InlineKeyboardMarkup(rows)


def help_back_markup(_, next_page: str = None, prev_page: str = None):
    """Back/Close row, with optional Prev ◀ / Next ▶ nav buttons above it."""
    rows = []
    # Navigation row — only rendered for paginated sections (e.g. HELP_5)
    nav = []
    if prev_page:
        nav.append(InlineKeyboardButton(
            text="◀ Prev", callback_data=prev_page,
        ))
    if next_page:
        nav.append(InlineKeyboardButton(
            text="Next ▶", callback_data=next_page,
        ))
    if nav:
        rows.append(nav)
    # Always-present back / close row
    rows.append([
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data="settings_back_helper",
        ),
        InlineKeyboardButton(
            text=_["CLOSE_BUTTON"], callback_data="close",
        ),
    ])
    return InlineKeyboardMarkup(rows)


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons
