#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import html as _html

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus, ChatType, ParseMode
from pyrogram.errors import (
    ChatAdminRequired,
    FloodWait,
    UserAlreadyParticipant,
    UserBannedInChannel,
    UserNotParticipant,
    UserPrivacyRestricted,
)
from pyrogram.types import (ChatPrivileges, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from youtubesearchpython.__future__ import VideosSearch
from YukkiMusic.utils import tg_send as _ts

import config
from config import BANNED_USERS
from config.config import OWNER_ID
from strings import get_command, get_string
from YukkiMusic import Telegram, YouTube, app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.plugins.play.playlist import del_plist_msg
from YukkiMusic.plugins.sudo.sudoers import sudoers_list
from YukkiMusic.utils.database import (add_served_chat,
                                       add_served_user,
                                       blacklisted_chats,
                                       get_assistant, get_custom_start,
                                       get_lang, get_userss,
                                       is_on_off,
                                       is_served_private_chat)
from YukkiMusic.utils.decorators.language import LanguageStart
from YukkiMusic.utils.inline import (help_pannel, private_panel,
                                     start_pannel)

loop = asyncio.get_running_loop()


@app.on_message(
    filters.command(get_command("START_COMMAND"))
    & filters.private
    & ~BANNED_USERS
)
@LanguageStart
async def start_comm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            rows = help_pannel(_, is_sudo=(message.from_user.id in SUDOERS))
            return await _ts.send_message(
                message.chat.id,
                (_["help_1"]),
                rows,
                reply_to=message.id,
            )
        if name[0:4] == "song":
            return await message.reply_text(_["song_2"])
        if name[0:3] == "sta":
            m = await message.reply_text(
                "🔎 Fetching your personal stats.!"
            )
            stats = await get_userss(message.from_user.id)
            tot = len(stats)
            if not stats:
                await asyncio.sleep(1)
                return await m.edit(_["ustats_1"])

            def get_stats():
                msg = ""
                limit = 0
                results = {}
                for i in stats:
                    top_list = stats[i]["spot"]
                    results[str(i)] = top_list
                    list_arranged = dict(
                        sorted(
                            results.items(),
                            key=lambda item: item[1],
                            reverse=True,
                        )
                    )
                if not results:
                    return m.edit(_["ustats_1"])
                tota = 0
                videoid = None
                for vidid, count in list_arranged.items():
                    tota += count
                    if limit == 10:
                        continue
                    if limit == 0:
                        videoid = vidid
                    limit += 1
                    details = stats.get(vidid)
                    title = (details["title"][:35]).title()
                    if vidid == "telegram":
                        msg += f"🔗 <a href='https://t.me/telegram'>Telegram Files and Audios</a> <b>played {count} times</b>\n\n"
                    else:
                        msg += f"🔗 <a href='https://www.youtube.com/watch?v={vidid}'>{_html.escape(title)}</a> <b>played {count} times</b>\n\n"
                msg = _["ustats_2"].format(tot, tota, limit) + msg
                return videoid, msg

            try:
                videoid, msg = await loop.run_in_executor(
                    None, get_stats
                )
            except Exception as e:
                print(e)
                return
            thumbnail = await YouTube.thumbnail(videoid, True)
            await m.delete()
            await message.reply_photo(photo=thumbnail, caption=msg)
            return
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"{message.from_user.mention} has just started bot to check <code>SUDOLIST</code>\n\n<b>USER ID:</b> {sender_id}\n<b>USER NAME:</b> {sender_name}",
                )
            return
        if name[0:3] == "lyr":
            query = (str(name)).replace("lyrics_", "", 1)
            lyrical = config.lyrical
            lyrics = lyrical.get(query)
            if lyrics:
                return await Telegram.send_split_text(message, lyrics)
            else:
                return await message.reply_text(
                    "Failed to get lyrics."
                )
        if name[0:3] == "del":
            await del_plist_msg(client=client, message=message, _=_)
        if name[0:3] == "inf":
            m = await message.reply_text("🔎 Fetching Info!")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[
                    0
                ]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = (
                f"🔍 <b><i>Video Track Information</i></b>\n\n"
                f"❇️ <b>Title:</b> {_html.escape(title)}\n\n"
                f"⏳ <b>Duration:</b> {_html.escape(duration)} Mins\n"
                f"👀 <b>Views:</b> <code>{_html.escape(views)}</code>\n"
                f"⏰ <b>Published Time:</b> {_html.escape(published)}\n"
                f"🎥 <b>Channel Name:</b> {_html.escape(channel)}\n"
                f"📎 <b>Channel Link:</b> <a href='{channellink}'>Visit From Here</a>\n"
                f"🔗 <b>Video Link:</b> <a href='{link}'>Link</a>\n\n"
                f"⚡️ <i>Searched Powered By {_html.escape(config.MUSIC_BOT_NAME)}</i>"
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎥 Watch ", url=f"{link}"
                        ),
                        InlineKeyboardButton(
                            text="🔄 Close", callback_data="close"
                        ),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"{message.from_user.mention} has just started bot to check <code>VIDEO INFORMATION</code>\n\n<b>USER ID:</b> {sender_id}\n<b>USER NAME:</b> {sender_name}",
                )
    else:
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None
        rows = private_panel(_, app.username, OWNER)
        # Owner-set custom start is stored as HTML (entities preserved via
        # replied.text.html in /setstart) so we always render with HTML mode.
        # Photo: prefer owner-set file_id (copy-safe for this bot), else
        # START_IMG_URL from config.
        custom = await get_custom_start()
        if custom and custom.get("text"):
            caption = custom["text"].replace("{bot}", config.MUSIC_BOT_NAME)
            photo = (custom or {}).get("photo") or config.START_IMG_URL
            if photo:
                sent = await _ts.send_photo(
                    message.chat.id, photo, caption, rows,
                    parse_mode="HTML",
                    reply_to=message.id,
                )
                if not sent:   # bad URL / expired file_id — fall back to text
                    await _ts.send_message(
                        message.chat.id, caption, rows,
                        parse_mode="HTML", reply_to=message.id,
                        disable_preview=False,
                    )
            else:
                await _ts.send_message(
                    message.chat.id, caption, rows,
                    parse_mode="HTML", reply_to=message.id,
                    disable_preview=False,
                )
        else:
            caption = (
                _["start_2"].format(_html.escape(config.MUSIC_BOT_NAME))
            )
            photo = config.START_IMG_URL
            if photo:
                sent = await _ts.send_photo(
                    message.chat.id, photo, caption, rows,
                    reply_to=message.id,
                )
                if not sent:   # photo failed (bad URL etc.) — fall back to text
                    await _ts.send_message(
                        message.chat.id, caption, rows,
                        reply_to=message.id,
                    )
            else:
                await _ts.send_message(
                    message.chat.id, caption, rows,
                    reply_to=message.id,
                )
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"{message.from_user.mention} has just started Bot.\n\n<b>USER ID:</b> {sender_id}\n<b>USER NAME:</b> {sender_name}",
            )


@app.on_message(
    filters.command(get_command("START_COMMAND"))
    & filters.group
    & ~BANNED_USERS
)
@LanguageStart
async def testbot(client, message: Message, _):
    rows = start_pannel(_)
    return await message.reply_text(
        (_["start_1"].format(
            _html.escape(message.chat.title or ""),
            _html.escape(config.MUSIC_BOT_NAME),
        )),
        reply_markup=_ts.to_markup(rows),
        parse_mode=ParseMode.HTML,
    )


welcome_group = 2

# ── Required bot permissions for music streaming ─────────────────────────────
_REQUIRED_BOT_PERMS = {
    "can_manage_video_chats": "Manage Voice/Video Chats",
    "can_delete_messages":    "Delete Messages",
    "can_invite_users":       "Add Members",
}


async def _setup_new_chat(chat_id: int, chat_title: str) -> None:
    """
    Background task run once when the bot joins a new supergroup.

    Steps
    ─────
    1. Check whether the bot has the necessary admin permissions and send
       a one-time action-required message if anything is missing.
    2. Resolve the assigned assistant account, verify it is not banned,
       and join it to the chat (via username or invite link).
    3. Promote the assistant with Manage Voice/Video Chats so it can
       stream audio/video.
    4. Log the full outcome (success or every failure) to LOG_GROUP_ID.
    """
    await asyncio.sleep(2)          # let the welcome message land first

    log     = config.LOG_GROUP_ID
    title   = _html.escape(chat_title or str(chat_id))

    # ── helper: safe log ──────────────────────────────────────────────────
    async def _log(text: str) -> None:
        if not log:
            return
        try:
            await app.send_message(log, text, parse_mode=ParseMode.HTML)
        except Exception:
            pass

    async def _chat_msg(text: str) -> None:
        try:
            await app.send_message(chat_id, text, parse_mode=ParseMode.HTML)
        except Exception:
            pass

    # ── 1. Bot permission audit ───────────────────────────────────────────
    missing_perms: list[str] = []
    try:
        me     = await app.get_chat_member(chat_id, app.id)
        privs  = me.privileges         # None when not admin
        if privs is None:
            missing_perms = list(_REQUIRED_BOT_PERMS.values())
        else:
            for attr, label in _REQUIRED_BOT_PERMS.items():
                if not getattr(privs, attr, False):
                    missing_perms.append(label)
    except Exception:
        missing_perms = list(_REQUIRED_BOT_PERMS.values())

    if missing_perms:
        lines = "\n".join(f"  • {p}" for p in missing_perms)
        await _chat_msg(
            f"⚠️ <b>Action Required</b>\n\n"
            f"Please promote me as admin with the following permissions:\n"
            f"{lines}\n\n"
            f"<i>Without these, voice/video streaming may not work properly.</i>"
        )

    # ── 2. Resolve assistant ──────────────────────────────────────────────
    try:
        userbot  = await get_assistant(chat_id)
    except Exception as exc:
        await _log(
            f"❌ <b>Assistant Resolve Error</b>\n"
            f"<b>Chat:</b> {title} (<code>{chat_id}</code>)\n"
            f"<b>Error:</b> <code>{_html.escape(str(exc))}</code>"
        )
        return

    asst_id   = getattr(userbot, "id",       None)
    asst_name = getattr(userbot, "name",     "assistant")
    asst_user = getattr(userbot, "username", None)
    asst_ref  = f"@{asst_user}" if asst_user else asst_name

    # ── 3. Check assistant membership ────────────────────────────────────
    already_in = False
    try:
        member = await app.get_chat_member(chat_id, asst_id)
        if member.status == ChatMemberStatus.BANNED:
            await _chat_msg(
                f"⚠️ <b>Assistant Banned</b>\n\n"
                f"The assistant {asst_ref} is <b>banned</b> in this group.\n"
                f"Please unban them to enable voice/video streaming."
            )
            await _log(
                f"🚫 <b>Assistant Banned</b>\n"
                f"<b>Chat:</b> {title} (<code>{chat_id}</code>)\n"
                f"<b>Assistant:</b> {asst_ref} (<code>{asst_id}</code>)"
            )
            return
        if member.status not in (ChatMemberStatus.LEFT,):
            already_in = True
    except UserNotParticipant:
        already_in = False
    except Exception:
        already_in = False

    # ── 4. Invite assistant if not present ────────────────────────────────
    if not already_in:
        try:
            chat = await app.get_chat(chat_id)
            if chat.username:
                try:
                    await userbot.join_chat(chat.username)
                except UserAlreadyParticipant:
                    pass
            else:
                # private group — need invite link
                invitelink = getattr(chat, "invite_link", None)
                if not invitelink:
                    try:
                        invitelink = await app.export_chat_invite_link(chat_id)
                    except ChatAdminRequired:
                        await _chat_msg(
                            f"⚠️ <b>Cannot Auto-Invite Assistant</b>\n\n"
                            f"I need the <b>Add Members</b> permission to invite {asst_ref}.\n"
                            f"Please add them manually and grant <b>Manage Voice Chats</b>."
                        )
                        return
                    except Exception as exc:
                        await _log(
                            f"❌ <b>Invite Link Error</b>\n"
                            f"<b>Chat:</b> {title} (<code>{chat_id}</code>)\n"
                            f"<b>Error:</b> <code>{_html.escape(str(exc))}</code>"
                        )
                        return
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                try:
                    await userbot.join_chat(invitelink)
                except UserAlreadyParticipant:
                    pass

        except FloodWait as exc:
            await asyncio.sleep(exc.value)

        except UserPrivacyRestricted:
            await _chat_msg(
                f"⚠️ <b>Privacy Restricted</b>\n\n"
                f"Can't auto-invite {asst_ref} due to their privacy settings.\n"
                f"Please add them manually and grant <b>Manage Voice Chats</b>."
            )
            await _log(
                f"⚠️ <b>Privacy Restricted</b>\n"
                f"<b>Chat:</b> {title} (<code>{chat_id}</code>)\n"
                f"<b>Assistant:</b> {asst_ref} — privacy restricted, manual add required."
            )
            return

        except UserBannedInChannel:
            await _chat_msg(
                f"⚠️ <b>Assistant Banned</b>\n\n"
                f"{asst_ref} is banned in this group.\n"
                f"Please unban them to enable streaming."
            )
            await _log(
                f"🚫 <b>Assistant Banned on Join</b>\n"
                f"<b>Chat:</b> {title} (<code>{chat_id}</code>)\n"
                f"<b>Assistant:</b> {asst_ref} (<code>{asst_id}</code>)"
            )
            return

        except Exception as exc:
            await _log(
                f"❌ <b>Assistant Join Error</b>\n"
                f"<b>Chat:</b> {title} (<code>{chat_id}</code>)\n"
                f"<b>Assistant:</b> {asst_ref}\n"
                f"<b>Error:</b> <code>{_html.escape(str(exc))}</code>"
            )
            return

    # ── 5. Promote assistant with voice-chat permission ───────────────────
    promote_ok = False
    try:
        await app.promote_chat_member(
            chat_id,
            asst_id,
            privileges=ChatPrivileges(can_manage_video_chats=True),
        )
        promote_ok = True
    except ChatAdminRequired:
        await _chat_msg(
            f"⚠️ Please promote {asst_ref} as admin with "
            f"<b>Manage Voice Chats</b> permission to enable streaming."
        )
    except Exception:
        pass    # silent — manually promoted chats still work

    # ── 6. Log success ────────────────────────────────────────────────────
    promote_status = "joined & promoted ✅" if promote_ok else "joined (promote manually ⚠️)"
    await _log(
        f"✅ <b>New Chat Setup</b>\n"
        f"<b>Chat:</b> {title} (<code>{chat_id}</code>)\n"
        f"<b>Assistant:</b> {asst_ref} (<code>{asst_id}</code>) — {promote_status}\n"
        f"<b>Bot perms missing:</b> {len(missing_perms)} "
        f"({', '.join(missing_perms) if missing_perms else 'none'})"
    )


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(client, message: Message):
    chat_id = message.chat.id
    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(message.chat.id):
            await message.reply_text(
                "<b>Private Music Bot</b>\n\nOnly for authorized chats from the owner. Ask my owner to allow your chat first."
            )
            return await app.leave_chat(message.chat.id)
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if member.id == app.id:
                chat_type = message.chat.type
                if chat_type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_6"])
                    return await app.leave_chat(message.chat.id)
                if chat_id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_7"].format(
                            f"https://t.me/{app.username}?start=sudolist"
                        )
                    )
                    return await app.leave_chat(chat_id)
                userbot = await get_assistant(message.chat.id)
                out = start_pannel(_)
                await message.reply_text(
                    (_["start_3"].format(
                        _html.escape(config.MUSIC_BOT_NAME),
                        _html.escape(userbot.username or ""),
                        userbot.id,
                    )),
                    reply_markup=_ts.to_markup(out),
                    parse_mode=ParseMode.HTML,
                )
                # One-time setup: permissions check + assistant invite/promote + logging
                asyncio.create_task(
                    _setup_new_chat(chat_id, message.chat.title or "")
                )
            if member.id in config.OWNER_ID:
                return await message.reply_text(
                    _["start_4"].format(
                        config.MUSIC_BOT_NAME, member.mention
                    )
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    _["start_5"].format(
                        config.MUSIC_BOT_NAME, member.mention
                    )
                )
            return
        except:
            return
