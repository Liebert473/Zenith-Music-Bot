#
# Owner-only commands to assign the bot's Support Group and Support
# Channel at runtime. Persists to MongoDB, overrides env config.
#

import re

import config
from pyrogram import filters
from pyrogram.types import Message

from YukkiMusic import app
from YukkiMusic.utils.database import (clear_owner_links,
                                       clear_support_channel,
                                       clear_support_group,
                                       get_owner_links,
                                       set_support_channel,
                                       set_support_group)
from YukkiMusic.utils.inline.start import update_owner_links_cache


_OWNER = filters.user(config.OWNER_ID) & ~filters.forwarded


def _normalize_link(raw: str) -> str | None:
    """Accept t.me URLs, @usernames, bare usernames, or invite links.
    Returns the canonical https://t.me/... form, or None if invalid."""
    if not raw:
        return None
    raw = raw.strip()
    # Full URL — accept https only
    if raw.startswith("https://t.me/") or raw.startswith("http://t.me/"):
        return raw.replace("http://", "https://", 1)
    # invite links via t.me/+abcd
    if raw.startswith("t.me/"):
        return "https://" + raw
    # @username or username
    if raw.startswith("@"):
        raw = raw[1:]
    # Public Telegram usernames are 5-32 chars, [a-zA-Z0-9_]
    if re.match(r"^[A-Za-z][A-Za-z0-9_]{3,31}$", raw):
        return f"https://t.me/{raw}"
    return None


def _format_status(links: dict) -> str:
    gr = links.get("support_group") or "_(using config default)_"
    ch = links.get("support_channel") or "_(using config default)_"
    cfg_gr = config.SUPPORT_GROUP or "_(unset)_"
    cfg_ch = config.SUPPORT_CHANNEL or "_(unset)_"
    return (
        "🛸 **Current Support Links**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"**📡 Support Channel:** {ch}\n"
        f"**🛡️ Support Group:** {gr}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "**Config defaults (`.env`):**\n"
        f"`SUPPORT_CHANNEL`: {cfg_ch}\n"
        f"`SUPPORT_GROUP`: {cfg_gr}"
    )


@app.on_message(filters.command(["setsupportgroup", "setgroup"]) & filters.private & _OWNER)
async def setsupportgroup_handler(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/setsupportgroup @username`\n"
            "• `/setsupportgroup https://t.me/your_group`\n"
            "• `/setsupportgroup https://t.me/+invitehash` (private group invite)"
        )
    raw = message.text.split(None, 1)[1]
    url = _normalize_link(raw)
    if not url:
        return await message.reply_text(
            "❌ Invalid link. Use `@username` or a `https://t.me/...` URL."
        )
    await set_support_group(url)
    update_owner_links_cache(support_group=url)
    await message.reply_text(
        f"✅ **Support Group set:** {url}\n\n"
        "All `/start` buttons now point here."
    )


@app.on_message(filters.command(["setsupportchannel", "setchannel"]) & filters.private & _OWNER)
async def setsupportchannel_handler(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n"
            "• `/setsupportchannel @username`\n"
            "• `/setsupportchannel https://t.me/your_channel`\n"
            "• `/setsupportchannel https://t.me/+invitehash`"
        )
    raw = message.text.split(None, 1)[1]
    url = _normalize_link(raw)
    if not url:
        return await message.reply_text(
            "❌ Invalid link. Use `@username` or a `https://t.me/...` URL."
        )
    await set_support_channel(url)
    update_owner_links_cache(support_channel=url)
    await message.reply_text(
        f"✅ **Support Channel set:** {url}\n\n"
        "All `/start` buttons now point here."
    )


@app.on_message(filters.command(["clearsupport", "resetsupport"]) & filters.private & _OWNER)
async def clearsupport_handler(_, message: Message):
    arg = message.command[1].lower() if len(message.command) > 1 else "all"
    if arg in ("group", "g"):
        await clear_support_group()
        update_owner_links_cache(support_group="")
        return await message.reply_text(
            "🗑 Support Group override cleared. Falling back to `SUPPORT_GROUP` env config."
        )
    if arg in ("channel", "ch", "c"):
        await clear_support_channel()
        update_owner_links_cache(support_channel="")
        return await message.reply_text(
            "🗑 Support Channel override cleared. Falling back to `SUPPORT_CHANNEL` env config."
        )
    if arg in ("all", "everything"):
        await clear_owner_links()
        update_owner_links_cache(support_group="", support_channel="")
        return await message.reply_text(
            "🗑 All support link overrides cleared. Falling back to `.env` config."
        )
    await message.reply_text(
        "**Usage:**\n"
        "• `/clearsupport group` — clear only the group override\n"
        "• `/clearsupport channel` — clear only the channel override\n"
        "• `/clearsupport all` — clear both (default)"
    )


@app.on_message(filters.command(["viewsupport", "supportlinks"]) & filters.private & _OWNER)
async def viewsupport_handler(_, message: Message):
    links = await get_owner_links()
    await message.reply_text(
        _format_status(links), disable_web_page_preview=True
    )
