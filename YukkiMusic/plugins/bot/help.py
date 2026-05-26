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
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, Message

from config import BANNED_USERS
from strings import get_command, get_string, helpers
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils import help_pannel
from YukkiMusic.utils.database import get_lang, is_commanddelete_on
from YukkiMusic.utils.decorators.language import (LanguageStart,
                                                  languageCB)
from YukkiMusic.utils.inline.help import (help_back_markup,
                                          private_help_panel)

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
        keyboard = help_pannel(_, True, is_sudo=(user_id in SUDOERS))
        if update.message.photo:
            await update.message.delete()
            await update.message.reply_text(
                _["help_1"],
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
        else:
            await update.edit_message_text(
                _["help_1"],
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
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
        keyboard = help_pannel(_, is_sudo=(user_id in SUDOERS))
        await update.reply_text(
            _["help_1"],
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )


@app.on_message(
    filters.command(HELP_COMMAND)
    & filters.group
    & ~BANNED_USERS
)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(
        _["help_2"], reply_markup=InlineKeyboardMarkup(keyboard)
    )


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    # Fetch the user's lang code so HELP_X bodies render in their language
    lang = await get_lang(CallbackQuery.message.chat.id)

    # ── Paginated HELP_5 (sudo/owner commands) ───────────────────────────
    if cb in ("hb5", "hb5p2"):
        if CallbackQuery.from_user.id not in SUDOERS:
            return await CallbackQuery.answer(
                "Only for Sudo Users", show_alert=True
            )
        if cb == "hb5":
            # Page 1: show with a "Next ▶" button
            kbd = help_back_markup(
                _, next_page="help_callback hb5p2"
            )
            await CallbackQuery.edit_message_text(
                helpers.get_help(5, lang), reply_markup=kbd
            )
        else:
            # Page 2: show with a "◀ Prev" button
            kbd = help_back_markup(
                _, prev_page="help_callback hb5"
            )
            await CallbackQuery.edit_message_text(
                helpers.get_help("5b", lang), reply_markup=kbd
            )
        return await CallbackQuery.answer()

    # ── Regular help sections (no pagination) ───────────────────────────
    keyboard = help_back_markup(_)
    try:
        await CallbackQuery.answer()
    except:
        pass
    if cb == "hb1":
        await CallbackQuery.edit_message_text(
            helpers.get_help(1, lang), reply_markup=keyboard
        )
    elif cb == "hb2":
        await CallbackQuery.edit_message_text(
            helpers.get_help(2, lang), reply_markup=keyboard
        )
    elif cb == "hb3":
        await CallbackQuery.edit_message_text(
            helpers.get_help(3, lang), reply_markup=keyboard
        )
    elif cb == "hb4":
        await CallbackQuery.edit_message_text(
            helpers.get_help(4, lang), reply_markup=keyboard
        )
