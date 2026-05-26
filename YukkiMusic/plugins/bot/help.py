#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

import config
from config import BANNED_USERS
from strings import get_command, get_string, helpers
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils import help_pannel, tg_send as _ts
from YukkiMusic.utils.custom_emoji import enhance_text
from YukkiMusic.utils.database import get_lang, is_commanddelete_on
from YukkiMusic.utils.decorators.language import (LanguageStart, languageCB)
from YukkiMusic.utils.inline.help import (help_back_markup, private_help_panel)

### Command
HELP_COMMAND = get_command("HELP_COMMAND")


@app.on_message(
    filters.command(HELP_COMMAND)
    & filters.private
    & ~BANNED_USERS
)
@app.on_callback_query(
    filters.regex("settings_back_helper") & ~BANNED_USERS
)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        user_id = update.from_user.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        rows = help_pannel(_, True, is_sudo=(user_id in SUDOERS))
        text = enhance_text(_["help_1"])
        # Delete old message, send fresh one with colors
        try:
            await update.message.delete()
        except:
            pass
        await _ts.send_message(chat_id, text, rows, disable_preview=True)
    else:
        chat_id = update.chat.id
        user_id = update.from_user.id
        if await is_commanddelete_on(update.chat.id):
            try:
                await update.delete()
            except:
                pass
        language = await get_lang(chat_id)
        _ = get_string(language)
        rows = help_pannel(_, is_sudo=(user_id in SUDOERS))
        await _ts.send_message(
            chat_id, enhance_text(_["help_1"]), rows,
            reply_to=update.id, disable_preview=True,
        )


@app.on_message(
    filters.command(HELP_COMMAND)
    & filters.group
    & ~BANNED_USERS
)
@LanguageStart
async def help_com_group(client, message: Message, _):
    rows = private_help_panel(_)
    await message.reply_text(
        _["help_2"],
        reply_markup=_ts.to_markup(rows),
    )


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    lang = await get_lang(CallbackQuery.message.chat.id)
    chat_id = CallbackQuery.message.chat.id
    msg_id  = CallbackQuery.message.id

    # ── Paginated HELP_5 (sudo/owner commands) ───────────────────────────
    if cb in ("hb5", "hb5p2"):
        if CallbackQuery.from_user.id not in SUDOERS:
            return await CallbackQuery.answer(
                "Only for Sudo Users", show_alert=True
            )
        if cb == "hb5":
            kbd = help_back_markup(_, next_page="help_callback hb5p2")
            await _ts.edit_message(
                chat_id, msg_id, helpers.get_help(5, lang), kbd
            )
        else:
            kbd = help_back_markup(_, prev_page="help_callback hb5")
            await _ts.edit_message(
                chat_id, msg_id, helpers.get_help("5b", lang), kbd
            )
        return await CallbackQuery.answer()

    # ── Regular help sections ────────────────────────────────────────────
    kbd = help_back_markup(_)
    try:
        await CallbackQuery.answer()
    except:
        pass

    section_map = {
        "hb1": 1,
        "hb2": 2,
        "hb3": 3,
        "hb4": 4,
    }
    if cb in section_map:
        await _ts.edit_message(
            chat_id, msg_id,
            helpers.get_help(section_map[cb], lang),
            kbd,
        )
