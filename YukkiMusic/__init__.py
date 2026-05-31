#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

# ── Pyrogram peer-ID compatibility patch ─────────────────────────────────────
# pyrogram 2.0.106 hard-rejects channel IDs longer than 13 chars in
# get_peer_type() (i.e. -100 + 9 digits).  Telegram now issues 10-digit
# channel IDs (-100 + 10 digits = 14 chars).  Patch the function to use
# prefix-based detection instead of a length cap so all valid IDs work.
import pyrogram.utils as _pyu  # noqa: E402

def _get_peer_type_patched(peer_id: int) -> str:
    s = str(peer_id)
    if not s.startswith("-"):
        return "user"
    if s.startswith("-100"):
        return "channel"
    return "chat"

_pyu.get_peer_type = _get_peer_type_patched
# ─────────────────────────────────────────────────────────────────────────────

from YukkiMusic.core.bot import YukkiBot
from YukkiMusic.core.dir import dirr
from YukkiMusic.core.git import git
from YukkiMusic.core.userbot import Userbot
from YukkiMusic.misc import dbb, heroku, sudo

from .logging import LOGGER

# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Load Sudo Users from DB
sudo()

# Bot Client
app = YukkiBot()

# Assistant Client
userbot = Userbot()

from .platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()
