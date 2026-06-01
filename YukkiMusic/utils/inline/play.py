#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#
# All functions return List[List[dict]] — the tg_send row format.
# Callers using pyrogram must wrap via:   tg_send.to_markup(rows)
# Callers using HTTP Bot API pass rows directly to tg_send helpers.

import random

from YukkiMusic.utils.tg_send import DANGER, PRIMARY, SUCCESS, btn

selections = [
    "▁▄▂▇▄▅▄▅▃",
    "▁▃▇▂▅▇▄▅▃",
    "▃▁▇▂▅▃▄▃▅",
    "▃▄▂▄▇▅▃▅▁",
    "▁▃▄▂▇▃▄▅▃",
    "▃▁▄▂▅▃▇▃▅",
    "▁▇▄▂▅▄▅▃▄",
    "▁▃▅▇▂▅▄▃▇",
    "▃▅▂▅▇▁▄▃▁",
    "▇▅▂▅▃▄▃▁▃",
    "▃▇▂▅▁▅▄▃▁",
    "▅▄▇▂▅▂▄▇▁",
    "▃▅▂▅▃▇▄▅▃",
]


# ── Now-playing panel (YouTube / SoundCloud / any tracked source) ─────────────

def stream_markup_timer(_, videoid, chat_id, played, dur):
    bar = random.choice(selections)
    return [
        [
            btn(f"{played} {bar} {dur}", callback_data="GetTimer"),
        ],
        [
            btn(_["PL_B_2"], callback_data=f"add_playlist {videoid}",
                ),
            btn(_["PL_B_3"], callback_data=f"PanelMarkup {videoid}|{chat_id}",
                ),
        ],
        [
            btn(_["CLOSEMENU_BUTTON"], callback_data="close",
                style=DANGER, ),
        ],
    ]


def stream_markup(_, videoid, chat_id):
    return [
        [
            btn(_["PL_B_2"], callback_data=f"add_playlist {videoid}",
                ),
            btn(_["PL_B_3"], callback_data=f"PanelMarkup {videoid}|{chat_id}",
                ),
        ],
        [
            btn(_["CLOSEMENU_BUTTON"], callback_data="close",
                style=DANGER, ),
        ],
    ]


# ── Now-playing panel (Telegram file — no videoid) ───────────────────────────

def telegram_markup_timer(_, chat_id, played, dur):
    bar = random.choice(selections)
    return [
        [
            btn(f"{played} {bar} {dur}", callback_data="GetTimer"),
        ],
        [
            btn(_["PL_B_3"], callback_data=f"PanelMarkup None|{chat_id}",
                ),
            btn(_["CLOSEMENU_BUTTON"], callback_data="close",
                style=DANGER, ),
        ],
    ]


def telegram_markup(_, chat_id):
    return [
        [
            btn(_["PL_B_3"], callback_data=f"PanelMarkup None|{chat_id}",
                ),
            btn(_["CLOSEMENU_BUTTON"], callback_data="close",
                style=DANGER, ),
        ],
    ]


# ── Search result — Audio / Video choice ─────────────────────────────────────

def track_markup(_, videoid, user_id, channel, fplay):
    return [
        [
            btn(_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style=SUCCESS, ),
            btn(_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style=PRIMARY),
        ],
        [
            btn(_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=DANGER, ),
        ],
    ]


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    return [
        [
            btn(_["P_B_1"],
                callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
                style=SUCCESS, ),
            btn(_["P_B_2"],
                callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
                style=PRIMARY),
        ],
        [
            btn(_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=DANGER, ),
        ],
    ]


# ── Live stream ───────────────────────────────────────────────────────────────

def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    return [
        [
            btn(_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
                style=SUCCESS, ),
            btn(_["CLOSEMENU_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=DANGER, ),
        ],
    ]


# ── Search slider (❮ prev / next ❯ results) ───────────────────────────────────

def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    return [
        [
            btn(_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style=SUCCESS, ),
            btn(_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style=PRIMARY),
        ],
        [
            btn("❮",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
            btn(_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
                style=DANGER, ),
            btn("❯",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
        ],
    ]


# ── Player control panel — page 1 (Pause · Resume · Skip · Stop) ─────────────

def panel_markup_1(_, videoid, chat_id):
    return [
        [
            btn("⏸ Pause",   callback_data=f"ADMIN Pause|{chat_id}"),
            btn("▶️ Resume",  callback_data=f"ADMIN Resume|{chat_id}",
                style=SUCCESS, ),
        ],
        [
            btn("⏯ Skip",    callback_data=f"ADMIN Skip|{chat_id}",
                ),
            btn("⏹ Stop",    callback_data=f"ADMIN Stop|{chat_id}",
                style=DANGER, ),
        ],
        [
            btn("◀️", callback_data=f"Pages Back|0|{videoid}|{chat_id}"),
            btn("🔙 Back",    callback_data=f"MainMarkup {videoid}|{chat_id}"),
            btn("▶️", callback_data=f"Pages Forw|0|{videoid}|{chat_id}"),
        ],
    ]


# ── Player control panel — page 2 (Mute · Unmute · Shuffle · Loop) ───────────

def panel_markup_2(_, videoid, chat_id):
    return [
        [
            btn("🔇 Mute",    callback_data=f"ADMIN Mute|{chat_id}"),
            btn("🔊 Unmute",  callback_data=f"ADMIN Unmute|{chat_id}",
                style=SUCCESS),
        ],
        [
            btn("🔀 Shuffle", callback_data=f"ADMIN Shuffle|{chat_id}"),
            btn("🔁 Loop",    callback_data=f"ADMIN Loop|{chat_id}",
                ),
        ],
        [
            btn("◀️", callback_data=f"Pages Back|1|{videoid}|{chat_id}"),
            btn("🔙 Back",    callback_data=f"MainMarkup {videoid}|{chat_id}"),
            btn("▶️", callback_data=f"Pages Forw|1|{videoid}|{chat_id}"),
        ],
    ]


# ── Player control panel — page 3 (Seek ±10s / ±30s) ────────────────────────

def panel_markup_3(_, videoid, chat_id):
    return [
        [
            btn("⏮ 10s",  callback_data=f"ADMIN 1|{chat_id}"),
            btn("⏭ 10s",  callback_data=f"ADMIN 2|{chat_id}"),
        ],
        [
            btn("⏮ 30s",  callback_data=f"ADMIN 3|{chat_id}"),
            btn("⏭ 30s",  callback_data=f"ADMIN 4|{chat_id}"),
        ],
        [
            btn("◀️", callback_data=f"Pages Back|2|{videoid}|{chat_id}"),
            btn("🔙 Back",    callback_data=f"MainMarkup {videoid}|{chat_id}"),
            btn("▶️", callback_data=f"Pages Forw|2|{videoid}|{chat_id}"),
        ],
    ]
