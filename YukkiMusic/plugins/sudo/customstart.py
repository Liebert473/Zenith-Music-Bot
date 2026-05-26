#
# Owner-only commands to customize the bot's /start message and image
# in private chats. Stored in MongoDB, language-independent.
#

import config
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message

from YukkiMusic import app
from YukkiMusic.utils.database import (clear_custom_start,
                                       clear_custom_start_photo,
                                       clear_custom_start_text,
                                       get_custom_start,
                                       set_custom_start_photo,
                                       set_custom_start_text)

_OWNER = filters.user(config.OWNER_ID) & ~filters.forwarded


def _extract_text(message: Message) -> str | None:
    """Pull markdown text from /setstart args or the replied message."""
    if message.reply_to_message:
        replied = message.reply_to_message
        # Preserve markdown formatting from the source message
        if replied.text:
            return replied.text.markdown if hasattr(replied.text, "markdown") else replied.text
        if replied.caption:
            return replied.caption.markdown if hasattr(replied.caption, "markdown") else replied.caption
    if len(message.command) > 1:
        return message.text.split(None, 1)[1]
    return None


@app.on_message(filters.command(["setstart"]) & filters.private & _OWNER)
async def setstart_handler(_, message: Message):
    text = _extract_text(message)
    if not text:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/setstart <text>` — set the start message text\n"
            "• Reply to a message with `/setstart` — copy its text/markdown\n\n"
            "💡 Use `{bot}` in your text and it'll be replaced with the bot's name."
        )
    # Allow {bot} placeholder for the bot name
    text_for_storage = text  # keep the {bot} placeholder verbatim
    await set_custom_start_text(text_for_storage)
    rendered = text_for_storage.replace("{bot}", config.MUSIC_BOT_NAME)
    await message.reply_text(
        f"✅ **Custom /start text saved.**\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"**Preview:**\n\n{rendered}",
        disable_web_page_preview=True,
    )


@app.on_message(filters.command(["setstartimg", "setstartphoto"]) & filters.private & _OWNER)
async def setstartimg_handler(_, message: Message):
    photo_id = None
    if message.reply_to_message and message.reply_to_message.photo:
        photo_id = message.reply_to_message.photo.file_id
    elif len(message.command) > 1:
        candidate = message.text.split(None, 1)[1].strip()
        if candidate.startswith(("http://", "https://")):
            photo_id = candidate
        else:
            return await message.reply_text(
                "❌ Image argument must be an `http://` or `https://` URL.\n"
                "Or just reply to a photo with `/setstartimg`."
            )
    else:
        return await message.reply_text(
            "**Usage:**\n"
            "• Reply to a photo with `/setstartimg` — uses that photo\n"
            "• `/setstartimg <https://image-url.jpg>` — uses a URL"
        )
    await set_custom_start_photo(photo_id)
    await message.reply_text(
        "✅ **Custom /start image saved.** Send `/start` to preview."
    )


@app.on_message(filters.command(["clearstart", "resetstart"]) & filters.private & _OWNER)
async def clearstart_handler(_, message: Message):
    # Allow targeted clears: /clearstart text  /clearstart image  /clearstart all
    arg = message.command[1].lower() if len(message.command) > 1 else "all"
    if arg in ("text", "msg", "message"):
        await clear_custom_start_text()
        return await message.reply_text(
            "🗑 **Custom /start text cleared.** The default language message will be used again."
        )
    if arg in ("img", "image", "photo"):
        await clear_custom_start_photo()
        return await message.reply_text(
            "🗑 **Custom /start image cleared.** Will fall back to `START_IMG_URL` from config."
        )
    if arg in ("all", "everything"):
        await clear_custom_start()
        return await message.reply_text(
            "🗑 **All /start customizations cleared.** Defaults restored."
        )
    await message.reply_text(
        "**Usage:**\n"
        "• `/clearstart text` — clear only the text\n"
        "• `/clearstart image` — clear only the image\n"
        "• `/clearstart all` — clear both (default)"
    )


@app.on_message(filters.command(["viewstart", "previewstart"]) & filters.private & _OWNER)
async def viewstart_handler(_, message: Message):
    custom = await get_custom_start()
    if not custom or (not custom.get("text") and not custom.get("photo")):
        return await message.reply_text(
            "ℹ️ No custom /start configured. The bot is using the language default.\n\n"
            "Set one with `/setstart` and `/setstartimg`."
        )
    text = custom.get("text")
    photo = custom.get("photo")
    rendered = (text or "_(no custom text — language default will be used)_").replace(
        "{bot}", config.MUSIC_BOT_NAME
    )
    header = "🛸 **Current Custom /start:**\n━━━━━━━━━━━━━━━━━━━━\n\n"
    if photo:
        try:
            return await message.reply_photo(photo=photo, caption=header + rendered)
        except Exception:
            return await message.reply_text(
                header + rendered + f"\n\n⚠️ (Photo failed to render: `{photo}`)",
                disable_web_page_preview=True,
            )
    await message.reply_text(header + rendered, disable_web_page_preview=True)
