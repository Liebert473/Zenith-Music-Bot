#
# Owner-only commands to customize the bot's /start message and image
# in private chats. Stored in MongoDB, language-independent.
#

import re

import config
from pyrogram import filters
from YukkiMusic.utils.tg_send import _prepare_html as _fix_tg_emoji
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, Message

from YukkiMusic import app
from YukkiMusic.utils.database import (clear_custom_start,
                                       clear_custom_start_photo,
                                       clear_custom_start_text,
                                       get_custom_start,
                                       set_custom_start_photo,
                                       set_custom_start_text)

_OWNER = filters.user(config.OWNER_ID) & ~filters.forwarded


def _extract_payload(message: Message) -> tuple[str | None, str | None]:
    """Pull (HTML-formatted text, photo file_id) from /setstart args or reply.

    HTML format is used so entity styling (bold, italic, links, code, emoji)
    survives storage and rendering — the bot sends /start with ParseMode.HTML.

    Returns (text_or_None, photo_id_or_None).
    """
    text: str | None = None
    photo_id: str | None = None

    replied = message.reply_to_message
    if replied:
        # Preserve entities → HTML so storage is parse-mode-stable.
        # _fix_tg_emoji converts pyrogram's <emoji emoji-id="…"> to the
        # Bot API form <tg-emoji emoji-id="…"> before we store the text.
        if replied.text:
            raw = replied.text.html if hasattr(replied.text, "html") else str(replied.text)
            text = _fix_tg_emoji(raw)
        elif replied.caption:
            raw = replied.caption.html if hasattr(replied.caption, "html") else str(replied.caption)
            text = _fix_tg_emoji(raw)
        # Capture photo file_id (largest size) — file_ids are bot-scoped,
        # since the bot received this message the id is reusable by it.
        if replied.photo:
            photo_id = replied.photo.file_id

    # Inline text arg only when no reply.
    # Use .html so MessageEntityCustomEmoji (premium emoji) document-IDs are
    # preserved as <tg-emoji emoji-id="…"> tags in the stored value.
    if text is None and len(message.command) > 1:
        # Strip only the leading /command[@bot] token; keep the rest verbatim.
        raw = re.sub(r'^/\S+\s*', '', message.text.html, count=1).strip()
        text = _fix_tg_emoji(raw)

    return text, photo_id


@app.on_message(filters.command(["setstart"]) & filters.private & _OWNER)
async def setstart_handler(_, message: Message):
    text, photo_id = _extract_payload(message)
    if not text and not photo_id:
        return await message.reply_text(
            "<b>Usage:</b>\n"
            "• <code>/setstart &lt;text&gt;</code> — set the start message text\n"
            "• Reply to a message with <code>/setstart</code> — copy its text + entities\n"
            "• Reply to a photo (with or without caption) — copies <b>both</b> "
            "the photo (preserving its file_id) and any caption text\n\n"
            "💡 Use <code>{bot}</code> in your text and it'll be replaced with "
            "the bot's name.",
            parse_mode=ParseMode.HTML,
        )

    saved = []
    if text is not None:
        await set_custom_start_text(text)
        saved.append("text")
    if photo_id is not None:
        await set_custom_start_photo(photo_id)
        saved.append("photo")

    saved_str = " + ".join(saved)
    rendered_caption = (text or "").replace("{bot}", config.MUSIC_BOT_NAME) if text else ""

    if photo_id:
        # Preview using the exact file_id we just stored
        try:
            return await message.reply_photo(
                photo=photo_id,
                caption=(
                    f"✅ <b>Custom /start saved</b> ({saved_str})\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    + (rendered_caption if rendered_caption else "<i>(no caption)</i>")
                ),
                parse_mode=ParseMode.HTML,
            )
        except Exception as exc:
            await message.reply_text(
                f"⚠️ Saved but preview failed: <code>{exc}</code>",
                parse_mode=ParseMode.HTML,
            )
            return

    # Text-only preview
    await message.reply_text(
        f"✅ <b>Custom /start saved</b> ({saved_str})\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>Preview:</b>\n\n{rendered_caption}",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False,
    )


@app.on_message(filters.command(["setstartimg", "setstartphoto"]) & filters.private & _OWNER)
async def setstartimg_handler(_, message: Message):
    photo_id = None
    if message.reply_to_message and message.reply_to_message.photo:
        # Photo received by THIS bot — file_id is reusable for re-sending
        photo_id = message.reply_to_message.photo.file_id
    elif len(message.command) > 1:
        candidate = message.text.split(None, 1)[1].strip()
        if candidate.startswith(("http://", "https://")):
            photo_id = candidate
        else:
            return await message.reply_text(
                "❌ Image argument must be an <code>http://</code> or "
                "<code>https://</code> URL.\n"
                "Or just reply to a photo with <code>/setstartimg</code>.",
                parse_mode=ParseMode.HTML,
            )
    else:
        return await message.reply_text(
            "<b>Usage:</b>\n"
            "• Reply to a photo with <code>/setstartimg</code> — uses that photo\n"
            "• <code>/setstartimg &lt;https://image-url.jpg&gt;</code> — uses a URL",
            parse_mode=ParseMode.HTML,
        )
    await set_custom_start_photo(photo_id)
    # Live preview of the exact stored file_id
    try:
        await message.reply_photo(
            photo=photo_id,
            caption="✅ <b>Custom /start image saved.</b> Send <code>/start</code> to preview the full panel.",
            parse_mode=ParseMode.HTML,
        )
    except Exception:
        await message.reply_text(
            "✅ <b>Custom /start image saved.</b> Send <code>/start</code> to preview.",
            parse_mode=ParseMode.HTML,
        )


@app.on_message(filters.command(["clearstart", "resetstart"]) & filters.private & _OWNER)
async def clearstart_handler(_, message: Message):
    # Allow targeted clears: /clearstart text  /clearstart image  /clearstart all
    arg = message.command[1].lower() if len(message.command) > 1 else "all"
    if arg in ("text", "msg", "message"):
        await clear_custom_start_text()
        return await message.reply_text(
            "🗑 <b>Custom /start text cleared.</b> The default language message will be used again.",
            parse_mode=ParseMode.HTML,
        )
    if arg in ("img", "image", "photo"):
        await clear_custom_start_photo()
        return await message.reply_text(
            "🗑 <b>Custom /start image cleared.</b> Will fall back to "
            "<code>START_IMG_URL</code> from config.",
            parse_mode=ParseMode.HTML,
        )
    if arg in ("all", "everything"):
        await clear_custom_start()
        return await message.reply_text(
            "🗑 <b>All /start customizations cleared.</b> Defaults restored.",
            parse_mode=ParseMode.HTML,
        )
    await message.reply_text(
        "<b>Usage:</b>\n"
        "• <code>/clearstart text</code> — clear only the text\n"
        "• <code>/clearstart image</code> — clear only the image\n"
        "• <code>/clearstart all</code> — clear both (default)",
        parse_mode=ParseMode.HTML,
    )


@app.on_message(filters.command(["viewstart", "previewstart"]) & filters.private & _OWNER)
async def viewstart_handler(_, message: Message):
    custom = await get_custom_start()
    if not custom or (not custom.get("text") and not custom.get("photo")):
        return await message.reply_text(
            "ℹ️ No custom /start configured. The bot is using the language default.\n\n"
            "Set one with <code>/setstart</code> and <code>/setstartimg</code>.",
            parse_mode=ParseMode.HTML,
        )
    text = custom.get("text")
    photo = custom.get("photo")
    rendered = (text or "<i>(no custom text — language default will be used)</i>").replace(
        "{bot}", config.MUSIC_BOT_NAME
    )
    header = "🛸 <b>Current Custom /start:</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
    if photo:
        try:
            return await message.reply_photo(
                photo=photo,
                caption=header + rendered,
                parse_mode=ParseMode.HTML,
            )
        except Exception as exc:
            return await message.reply_text(
                header + rendered + f"\n\n⚠️ (Photo failed to render: <code>{exc}</code>)",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
    await message.reply_text(
        header + rendered,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False,
    )
