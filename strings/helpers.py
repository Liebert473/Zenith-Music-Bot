#
# Help-menu text for the /help inline panel.
# Localized for en / zh / my (Burmese). Other languages fall back to en.
#
# Public API:
#   helpers.get_help(num: int, lang: str = "en") -> str
#   helpers.HELP_1 ... HELP_5  (legacy English shortcuts, still exported)
#


# ── HELP_1: Admin Commands ──────────────────────────────────────────────
_HELP_1_EN = """✅**<u>Admin Commands:</u>**

**c** stands for channel play.

/pause or /cpause - Pause the playing music.
/resume or /cresume- Resume the paused music.
/mute or /cmute- Mute the playing music.
/unmute or /cunmute- Unmute the muted music.
/skip or /cskip- Skip the current playing music.
/stop or /cstop- Stop the playing music.
/shuffle or /cshuffle- Randomly shuffles the queued playlist.
/seek or /cseek - Forward Seek the music to your duration
/seekback or /cseekback - Backward Seek the music to your duration
/restart - Restart bot for your chat .


✅<u>**Specific Skip:**</u>
/skip or /cskip [Number(example: 3)]
    - Skips music to a the specified queued number. Example: /skip 3 will skip music to third queued music and will ignore 1 and 2 music in queue.

✅<u>**Loop Play:**</u>
/loop or /cloop [enable/disable] or [Numbers between 1-10]
    - When activated, bot loops the current playing music to 1-10 times on voice chat. Default to 10 times.

✅<u>**Auth Users:**</u>
Auth Users can use admin commands without admin rights in your chat.

/auth [Username] - Add a user to AUTH LIST of the group.
/unauth [Username] - Remove a user from AUTH LIST of the group.
/authusers - Check AUTH LIST of the group."""


_HELP_1_ZH = """✅**<u>管理员命令:</u>**

**c** 表示频道播放（channel play）。

/pause 或 /cpause - 暂停当前播放的音乐。
/resume 或 /cresume - 恢复已暂停的音乐。
/mute 或 /cmute - 静音当前播放的音乐。
/unmute 或 /cunmute - 取消静音。
/skip 或 /cskip - 跳到下一首。
/stop 或 /cstop - 停止当前播放。
/shuffle 或 /cshuffle - 随机打乱队列。
/seek 或 /cseek - 向前跳转指定秒数。
/seekback 或 /cseekback - 向后跳转指定秒数。
/restart - 在此聊天中重启机器人。


✅<u>**指定跳过:**</u>
/skip 或 /cskip [数字（例如：3）]
    - 跳到队列中指定位置的歌曲。例如 /skip 3 会直接跳到队列第 3 首，前两首被忽略。

✅<u>**循环播放:**</u>
/loop 或 /cloop [enable/disable] 或 [1-10 之间的数字]
    - 启用后，机器人会将当前播放的音乐循环 1-10 次。默认 10 次。

✅<u>**授权用户 (AUTH):**</u>
授权用户无需管理员权限即可使用管理员命令。

/auth [用户名] - 将用户添加到此群的授权名单。
/unauth [用户名] - 从授权名单移除用户。
/authusers - 查看此群的授权名单。"""


_HELP_1_MY = """✅**<u>[🛡️ ADMIN COMMANDS] 🛡️</u>**

⚡ **c** = channel play

/pause / /cpause - ⏸ Music ကို ခဏရပ်ပါ
/resume / /cresume - ▶️ Music ကို ပြန်ဖွင့်ပါ
/mute / /cmute - 🔇 Music ကို mute ပြုလုပ်ပါ
/unmute / /cunmute - 🔊 Music ကို unmute ပြုလုပ်ပါ
/skip / /cskip - ⏭ နောက် track သို့ ကျော်ပါ
/stop / /cstop - ⏹ Music ကို ရပ်ပါ
/shuffle / /cshuffle - 🎲 Queue ကို shuffle ပြုလုပ်ပါ
/seek / /cseek - ⏩ N စက္ကန့် ရှေ့သို့ ရွှေ့ပါ
/seekback / /cseekback - ⏪ N စက္ကန့် နောက်သို့ ပြန်ရွှေ့ပါ
/restart - 🌀 သင်၏ chat အတွက် bot ကို restart လုပ်ပါ


✅<u>**[🔢 SPECIFIC SKIP] 🔢**</u>
/skip / /cskip [Number e.g. 3]
    - Queue ထဲရှိ သီးခြား position သို့ ကျော်ပါ။ ဥပမာ `/skip 3` သည် queue ထဲ track #3 သို့ တိုက်ရိုက် ကျော်သည် [#1, #2 ကို ကျော်လွန်] ။

✅<u>**[🔁 LOOP_PROTOCOL] 🔁**</u>
/loop / /cloop [enable/disable] / [1-10 အကြား ဂဏန်း]
    - လက်ရှိ track ကို 1-10 ကြိမ်အထိ loop ပြုလုပ်ပါမည် [default: 10]။

✅<u>**[🎩 AUTH USERS] 🎩**</u>
Auth Users များသည် admin rights မပါဘဲ admin commands များ သုံးနိုင်ပါသည်။

/auth [Username] - User တစ်ဦးကို group ၏ AUTH LIST ထဲ ထည့်ပါ။
/unauth [Username] - User တစ်ဦးကို AUTH LIST မှ ဖယ်ရှားပါ။
/authusers - Group ၏ AUTH LIST ကို ပြသပါ။"""


# ── HELP_2: Play Commands ───────────────────────────────────────────────
_HELP_2_EN = """✅<u>**Play Commands:**</u>

Available Commands = play , vplay , cplay

ForcePlay Commands = playforce , vplayforce , cplayforce

**c** stands for channel play.
**v** stands for video play.
**force** stands for force play.

/play or /vplay or /cplay  - Bot will start playing your given query on voice chat or Stream live links on voice chats.

/playforce or /vplayforce or /cplayforce -  **Force Play** stops the current playing track on voice chat and starts playing the searched track instantly without disturbing/clearing queue.

/channelplay [Chat username or id] or [Disable] - Connect channel to a group and stream music on channel's voice chat from your group.


✅**<u>Bot's Server Playlists:</u>**
/playlist  - Check Your Saved Playlist On Servers.
/deleteplaylist - Delete any saved music in your playlist
/play  - Start playing Your Saved Playlist from Servers."""


_HELP_2_ZH = """✅<u>**播放命令:**</u>

可用命令 = play , vplay , cplay

强制播放命令 = playforce , vplayforce , cplayforce

**c** = 频道播放（channel play）
**v** = 视频播放（video play）
**force** = 强制播放

/play 或 /vplay 或 /cplay - 在语音聊天中播放你提供的搜索词或链接（包括 live 流）。

/playforce 或 /vplayforce 或 /cplayforce - **强制播放**：停止当前曲目，立即播放搜索结果，不清空队列。

/channelplay [频道用户名或 ID] 或 [Disable] - 将群组连接到频道，从群组发起命令在频道语音聊天中播放音乐。


✅**<u>服务器端播放列表:</u>**
/playlist - 查看保存在服务器上的个人播放列表。
/deleteplaylist - 删除播放列表中的某首歌。
/play - 直接从服务器播放列表开始播放。"""


_HELP_2_MY = """✅<u>**[🎶 PLAY COMMANDS] 🎶**</u>

📡 Available = play , vplay , cplay
⚡ ForcePlay = playforce , vplayforce , cplayforce

▰ **c** = channel play
▰ **v** = video play
▰ **force** = force play

/play / /vplay / /cplay - သင်ပေးသော query / link ကို voice chat တွင် play သို့မဟုတ် live stream ပြုလုပ်ပါမည်။

/playforce / /vplayforce / /cplayforce - **Force Play** ⚡ : လက်ရှိ track ကို ရပ်ပြီး ရှာထားသော track ကို ချက်ချင်း play ပါသည် [queue မပျောက်ပါ]။

/channelplay [Channel username/id] / [Disable] - Group ကို channel တစ်ခုနှင့် ချိတ်ဆက်ပြီး channel ၏ voice chat တွင် music stream ပြုလုပ်ပါ။


✅**<u>[💾 SERVER PLAYLISTS] 💾</u>**
/playlist - Server တွင် သင် save ထားသော playlist ကို ကြည့်ပါ။
/deleteplaylist - Playlist ထဲမှ track တစ်ပုဒ်ကို ဖျက်ပါ။
/play - Server ၏ saved playlist ကို play စတင်ပါ။"""


# ── HELP_3: Bot Commands ────────────────────────────────────────────────
_HELP_3_EN = """✅<u>**Bot Commands:**</u>

/stats - Get Top 10 Tracks Global Stats, Top 10 Users of bot, Top 10 Chats on bot, Top 10 Played in a chat etc etc.

/sudolist - Check Sudo Users of Yukki Music Bot

/lyrics [Music Name] - Searches Lyrics for the particular Music on web.

/song [Track Name] or [YT Link] - Download any track from youtube in mp3 or mp4 formats.

/player -  Get a interactive Playing Panel.

**c** stands for channel play.

/queue or /cqueue- Check Queue List of Music."""


_HELP_3_ZH = """✅<u>**机器人命令:**</u>

/stats - 查看 Top 10 全局曲目、用户、群聊以及本群 Top 10 等统计。

/sudolist - 查看 Yukki Music Bot 的 Sudo 用户列表。

/lyrics [歌曲名] - 在网上搜索指定歌曲的歌词。

/song [歌曲名] 或 [YouTube 链接] - 从 YouTube 下载音频（mp3）或视频（mp4）。

/player - 打开交互式的播放面板。

**c** 表示频道播放。

/queue 或 /cqueue - 查看当前播放队列。"""


_HELP_3_MY = """✅<u>**[🤖 BOT COMMANDS] 🤖**</u>

/stats - 📊 Top 10 Tracks (Global), Top 10 Users, Top 10 Chats, Top 10 Played per chat စတဲ့ telemetry အပြည့်အစုံ။

/sudolist - ⭐ Yukki Music Bot ၏ Sudo Users စာရင်း။

/lyrics [Music Name] - 📖 သီးခြား music အတွက် lyrics web မှ ရှာပါ။

/song [Track Name] / [YT Link] - 💾 YouTube မှ track ကို mp3 / mp4 format ဖြင့် download ပြုလုပ်ပါ။

/player - 🎛️ Interactive playing panel ဖွင့်ပါ။

▰ **c** = channel play

/queue / /cqueue - 📑 Music ၏ Queue List ကို ပြသပါ။"""


# ── HELP_4: Extra Commands + Settings ───────────────────────────────────
_HELP_4_EN = """✅<u>**Extra  Commands:**</u>
/start - Start the Music Bot.
/help  - Get Commands Helper Menu with detailed explanations of commands.
/ping- Ping the Bot and check Ram, Cpu etc stats of Bot.

✅<u>**Group Settings:**</u>
/settings - Get a complete group's settings with inline buttons

🔗 **Options in Settings:**

1️⃣ You can set **Audio Quality** you want to stream on voice chat.

2️⃣ You can set **Video Quality** you want to stream on voice chat.

3️⃣ **Auth Users**:- You can change admin commands mode from here to everyone or admins only. If everyone, anyone present in you group will be able to use admin commands(like /skip, /stop etc)

4️⃣ **Clean Mode:** When enabled deletes the bot's messages after 5 mins from your group to make sure your chat remains clean and good.

5️⃣ **Command Clean** : When activated, Bot will delete its executed commands (/play, /pause, /shuffle, /stop etc) immediately.

6️⃣ **Play Settings:**

/playmode - Get a complete play settings panel with buttons where you can set your group's play settings.

<u>Options in playmode:</u>

1️⃣ **Search Mode** [Direct or Inline] - Changes your search mode while you give /play mode.

2️⃣ **Admin Commands** [Everyone or Admins] - If everyone, anyone present in you group will be able to use admin commands(like /skip, /stop etc)

3️⃣ **Play Type** [Everyone or Admins] - If admins, only admins present in group can play music on voice chat."""


_HELP_4_ZH = """✅<u>**额外命令:**</u>
/start - 启动机器人。
/help - 打开命令帮助菜单（含详细说明）。
/ping - Ping 机器人并查看 RAM、CPU 等状态。

✅<u>**群组设置:**</u>
/settings - 通过内联按钮打开完整的群组设置面板。

🔗 **设置选项:**

1️⃣ **音频质量** - 设置语音聊天中流式播放的音频质量。

2️⃣ **视频质量** - 设置视频质量。

3️⃣ **授权用户**:- 设置管理员命令权限模式：全员可用 或 仅管理员。若选「全员」，群内任何人都可以用 /skip /stop 等命令。

4️⃣ **Clean Mode**：启用后机器人会在 5 分钟后删除自己发的消息，保持群组整洁。

5️⃣ **Command Clean**：启用后机器人会立刻删除已执行的命令（/play /pause /shuffle /stop 等）。

6️⃣ **播放设置:**

/playmode - 打开播放设置面板，按钮可调。

<u>playmode 中的选项:</u>

1️⃣ **搜索模式** [Direct / Inline] - 改变 /play 时的搜索方式。

2️⃣ **管理员命令** [Everyone / Admins] - 若选「Everyone」，群内任何人都可使用管理员命令。

3️⃣ **播放类型** [Everyone / Admins] - 若选「Admins」，只有管理员可在语音聊天中播放音乐。"""


_HELP_4_MY = """✅<u>**[⚡ EXTRA COMMANDS] ⚡**</u>
/start - 🛸 Music Bot ကို စတင်ပါ။
/help - 📜 Commands များ၏ အသေးစိတ်ဖော်ပြချက်ပါ helper menu ဖွင့်ပါ။
/ping - ⚡ Ping + RAM, CPU စသော stats စစ်ပါ။

✅<u>**[⚙️ GROUP SETTINGS] ⚙️**</u>
/settings - Inline buttons ပါသော group settings panel ဖွင့်ပါ။

🔗 **Settings အတွင်း Options:**

1️⃣ **🎚️ Audio Quality** - Voice chat တွင် stream ပြုလုပ်လိုသော audio quality သတ်မှတ်ပါ။

2️⃣ **🎥 Video Quality** - Video quality သတ်မှတ်ပါ။

3️⃣ **🎩 Auth Users** - Admin commands mode ပြောင်းပါ [everyone / admins only]။ `Everyone` ဆိုပါက group ထဲ ရှိသူတိုင်း /skip, /stop စသော commands သုံးနိုင်ပါမည်။

4️⃣ **🔄 Clean Mode** - ဖွင့်ထားသောအခါ Bot ၏ messages များကို 5 မိနစ်အကြာတွင် ဖျက်ပစ်ပြီး chat ကို သန့်ရှင်းပါသည်။

5️⃣ **🗑 Command Clean** - ဖွင့်ထားသောအခါ executed commands များ (/play, /pause, /shuffle, /stop) ကို ချက်ချင်း ဖျက်ပစ်ပါသည်။

6️⃣ **▶️ Play Settings:**

/playmode - Group ၏ play settings panel ဖွင့်ပါ။

<u>playmode အတွင်း Options:</u>

1️⃣ **🔎 Search Mode** [Direct / Inline] - /play သုံးချိန် search mode ပြောင်းပါ။

2️⃣ **🛡️ Admin Commands** [Everyone / Admins] - `Everyone` ဆိုပါက group ထဲ ရှိသူတိုင်း admin commands သုံးနိုင်သည်။

3️⃣ **🫂 Play Type** [Everyone / Admins] - `Admins` ဆိုပါက admins များသာ voice chat တွင် music play နိုင်သည်။"""


# ── HELP_5: Sudo / Owner Commands ──────────────────────────────────────
_HELP_5_EN = """🔰**<u>ADD & REMOVE SUDO USERS :</u>**
/addsudo [Username or Reply to a user]
/delsudo [Username or Reply to a user]

🛸**<u>OWNER /START CUSTOMIZATION:</u>**
The /start welcome shown in private chats is owner-editable and bypasses the language system entirely (works in any user's language).

/setstart [text] or reply to a message - Set the welcome text. Use `{bot}` as a placeholder for the bot name. Markdown is preserved when replying to a formatted message.
/setstartimg - Reply to a photo to use it as the welcome image. Or /setstartimg [https://url.jpg] for a URL.
/clearstart [text|image|all] - Clear the custom text, image, or both. Defaults to `all`.
/viewstart - Preview the currently-configured custom /start.

🔗**<u>SUPPORT LINKS (runtime override):</u>**
Override the Support Group and Support Channel buttons that appear on the /start inline keyboard — no need to restart the bot.

/setsupportgroup or /setgroup [@username | https://t.me/...] - Set the Support Group link (public @username, t.me URL, or invite link).
/setsupportchannel or /setchannel [@username | https://t.me/...] - Set the Support Channel link.
/clearsupport [group|channel|all] - Clear the override and fall back to the `.env` config value. Defaults to `all`.
/viewsupport - Show the currently active support links (override + .env defaults side-by-side).

🛃**<u>HEROKU:</u>**
/usage - Dyno Usage.

🌐**<u>CONFIG VARS:</u>**
/get_var - Get a config var from Heroku or .env.
/del_var - Delete any var on Heroku or .env.
/set_var [Var Name] [Value] - Set a Var or Update a Var on heroku or .env. Seperate Var and its Value with a space.

🤖**<u>BOT COMMANDS:</u>**
/reboot - Reboot your Bot.
/update - Update Bot.
/speedtest - Check server speeds
/maintenance [enable / disable]
/logger [enable / disable] - Bot logs the searched queries in logger group.
/get_log [Number of Lines] - Get log of your bot from heroku or vps. Works for both.
/autoend [enable|disable] - Enable Auto stream end after 3 mins if no one is listening.

📈**<u>STATS COMMANDS:</u>**
/activevoice - Check active voice chats on bot.
/activevideo - Check active video calls on bot.
/stats - Check Bots Stats

⚠️**<u>BLACKLIST CHAT FUNCTION:</u>**
/blacklistchat [CHAT_ID] - Blacklist any chat from using Music Bot
/whitelistchat [CHAT_ID] - Whitelist any blacklisted chat from using Music Bot
/blacklistedchat - Check all blacklisted chats.

👤**<u>BLOCKED FUNCTION:</u>**
/block [Username or Reply to a user] - Prevents a user from using bot commands.
/unblock [Username or Reply to a user] - Remove a user from Bot's Blocked List.
/blockedusers - Check blocked Users Lists

👤**<u>GBAN FUNCTION:</u>**
/gban [Username or Reply to a user] - Gban a user from bot's served chat and stop him from using your bot.
/ungban [Username or Reply to a user] - Remove a user from Bot's gbanned List and allow him for using your bot
/gbannedusers - Check Gbanned Users Lists

🎥**<u>VIDEOCALLS FUNCTION:</u>**
/set_video_limit [Number of Chats] - Set a maximum Number of Chats allowed for Video Calls at a time. Default to 3 chats.
/videomode [download|m3u8] - If download mode is enabled, Bot will download videos instead of playing them in M3u8 form. ByDefault to M3u8. You can use download mode when any query doesnt plays in m3u8 mode.

⚡️**<u>PRIVATE BOT FUNCTION:</u>**
/authorize [CHAT_ID] - Allow a chat for using your bot.
/unauthorize [CHAT_ID] - Disallow a chat from using your bot.
/authorized - Check all allowed chats of your bot.

🌐**<u>BROADCAST FUNCTION:</u>**
Broadcast text **or media** (photo, GIF, video, document, audio, sticker) to every served chat.

**Three input modes:**
1. `/broadcast Hello everyone` — plain text.
2. **Reply** to any message (with or without media) with `/broadcast`.
3. **Upload media** (photo / GIF / video / etc.) and put `/broadcast <caption>` in the *caption* — the media is broadcast with the cleaned caption.

<u>Flags (can appear anywhere in the text or caption):</u>
**-pin** : Pin the message silently in each chat.
**-pinloud** : Pin with loud notification.
**-user** : Also DM every user who has started the bot.
**-assistant** : Also broadcast through assistant accounts.
**-nobot** : Skip the bot's own served-chat sweep.
**-forward** : Use `forward_messages` (shows "Forwarded from"). **Default is `copy_message`** — clean look with no forward header, recommended for advertising / promotional sends.

**Examples:**
• `/broadcast -user -assistant -pin Hello Testing` — text everywhere, pinned silently.
• Upload a promo image with caption `/broadcast -user Check out our new bot!` — image + caption is delivered cleanly to every chat and user.
• Reply to a video message with `/broadcast -pinloud` — video is copied (no forward tag) and pinned loudly.

"""


_HELP_5_ZH = """🔰**<u>添加 / 移除 Sudo 用户:</u>**
/addsudo [用户名 或 回复某用户]
/delsudo [用户名 或 回复某用户]

🛸**<u>主人专属 — /start 自定义:</u>**
私聊中的 /start 欢迎语可由主人编辑，且**不受语言系统影响**（无论用户用哪种语言都看到同一条）。

/setstart [文本] 或 回复某条消息 - 设置欢迎文本。`{bot}` 会被替换为机器人名字。回复带格式的消息时会保留 Markdown。
/setstartimg - 回复一张图片以将其设为欢迎图。或 /setstartimg [https://url.jpg] 使用 URL。
/clearstart [text|image|all] - 清除自定义文本、图片或全部。默认 `all`。
/viewstart - 预览当前自定义 /start 配置。

🔗**<u>支持链接（运行时覆盖）:</u>**
覆盖 /start 内联键盘上的「支持群组」和「支持频道」按钮 — 无需重启机器人。

/setsupportgroup 或 /setgroup [@用户名 | https://t.me/...] - 设置支持群组链接（公开 @username、t.me URL 或邀请链接均可）。
/setsupportchannel 或 /setchannel [@用户名 | https://t.me/...] - 设置支持频道链接。
/clearsupport [group|channel|all] - 清除覆盖，回退到 `.env` 配置值。默认 `all`。
/viewsupport - 显示当前生效的支持链接（覆盖值 + .env 默认值对比）。

🛃**<u>HEROKU:</u>**
/usage - Dyno 使用情况。

🌐**<u>配置变量:</u>**
/get_var - 获取 Heroku / .env 中的配置变量。
/del_var - 删除 Heroku / .env 中的任意变量。
/set_var [变量名] [值] - 在 Heroku / .env 中设置或更新变量。变量名和值用空格分隔。

🤖**<u>机器人命令:</u>**
/reboot - 重启机器人。
/update - 更新机器人。
/speedtest - 测试服务器速度。
/maintenance [enable / disable]
/logger [enable / disable] - 机器人将搜索查询记录到日志群。
/get_log [行数] - 从 Heroku 或 VPS 获取日志（两者都可用）。
/autoend [enable|disable] - 启用后，如果 3 分钟无人收听，自动结束语音流。

📈**<u>统计命令:</u>**
/activevoice - 查看机器人当前活跃的语音聊天。
/activevideo - 查看活跃的视频通话。
/stats - 查看机器人整体状态。

⚠️**<u>群组黑名单功能:</u>**
/blacklistchat [CHAT_ID] - 将聊天加入黑名单。
/whitelistchat [CHAT_ID] - 从黑名单移除。
/blacklistedchat - 查看所有被加入黑名单的聊天。

👤**<u>用户屏蔽功能:</u>**
/block [用户名 或 回复某用户] - 禁止用户使用机器人。
/unblock [用户名 或 回复某用户] - 从屏蔽名单移除用户。
/blockedusers - 查看被屏蔽的用户列表。

👤**<u>GBAN 功能:</u>**
/gban [用户名 或 回复某用户] - 在机器人服务的所有聊天中封禁该用户。
/ungban [用户名 或 回复某用户] - 解除 gban。
/gbannedusers - 查看被 gban 的用户列表。

🎥**<u>视频通话功能:</u>**
/set_video_limit [聊天数] - 设置同时允许视频通话的最大聊天数（默认 3）。
/videomode [download|m3u8] - 若启用 download 模式，机器人会先下载视频再播放，而非 m3u8 流式播放。默认 m3u8。

⚡️**<u>私有机器人功能:</u>**
/authorize [CHAT_ID] - 允许某聊天使用机器人。
/unauthorize [CHAT_ID] - 禁止某聊天使用机器人。
/authorized - 查看已允许的聊天列表。

🌐**<u>广播功能:</u>**
向机器人服务过的所有聊天广播 **文字或媒体**（图片、GIF、视频、文档、音频、贴纸）。

**三种输入方式:**
1. `/broadcast 你好大家` — 纯文字广播。
2. **回复**任意消息（带或不带媒体）并加上 `/broadcast`。
3. **直接上传媒体**（图片 / GIF / 视频 等）并在「caption」里写 `/broadcast <你的文字>` — 媒体会连同清理后的文字一起广播。

<u>选项（可以出现在文字或 caption 的任何位置）:</u>
**-pin** : 静默置顶消息
**-pinloud** : 带强提示的置顶
**-user** : 同时给所有启动过机器人的用户发私信
**-assistant** : 用助手账号广播
**-nobot** : 跳过机器人自身的服务群广播
**-forward** : 使用 `forward_messages`（显示「转发自」）。**默认是 `copy_message`** — 干净的外观，无转发标签，适合广告/推广场景。

**示例:**
• `/broadcast -user -assistant -pin Hello Testing` — 文字广播到所有地方，静默置顶。
• 上传一张推广图，caption 写 `/broadcast -user 来看看我们的新机器人!` — 图片 + caption 干净地送达每个群和每个用户。
• 回复一条视频消息并发 `/broadcast -pinloud` — 视频被复制（无转发标签），并带提示置顶。

"""


_HELP_5_MY = """🔰**<u>[⭐ SUDO USERS MANAGEMENT] ⭐</u>**
/addsudo [Username / Reply to a user] - Sudo user ထဲ ထည့်ပါ။
/delsudo [Username / Reply to a user] - Sudo user မှ ဖယ်ရှားပါ။

🛸**<u>[OWNER /START CUSTOMIZATION] 🛸</u>**
Private chat တွင် ပြသသော /start welcome ကို Owner သတ်မှတ်နိုင်ပါသည်။ Language system ၏ ဩဇာ မထိရောက်ပါ — user မည်သည့်ဘာသာစကား ရွေးထားသည် ဖြစ်စေ တူညီသော message ပြသပါမည်။

/setstart [text] / Reply to a message - Welcome text ကို သတ်မှတ်ပါ။ `{bot}` placeholder ကို bot ၏ name အဖြစ် အလိုအလျောက် ပြောင်းပါမည်။ Replied message မှ Markdown ကို ထိန်းသိမ်းပါမည်။
/setstartimg - Photo တစ်ပုံကို reply လုပ်ပြီး welcome image အဖြစ် သတ်မှတ်ပါ။ သို့မဟုတ် /setstartimg [https://url.jpg] ဖြင့် URL ပေးပါ။
/clearstart [text|image|all] - Custom text/image/all ကို ဖျက်ပါ။ Default = `all`။
/viewstart - လက်ရှိ custom /start config ကို preview ပြသပါ။

🔗**<u>[SUPPORT LINKS :: RUNTIME OVERRIDE] 🔗</u>**
/start keyboard ပေါ်ရှိ Support Group နှင့် Support Channel buttons များကို bot restart မလုပ်ဘဲ runtime တွင် တိုက်ရိုက် ပြောင်းလဲနိုင်ပါသည်။

/setsupportgroup / /setgroup [@username | https://t.me/...] - Support Group link သတ်မှတ်ပါ (public @username, t.me URL, invite link ဖြစ်နိုင်ပါသည်)။
/setsupportchannel / /setchannel [@username | https://t.me/...] - Support Channel link သတ်မှတ်ပါ။
/clearsupport [group|channel|all] - Override ဖျက်ပြီး `.env` config value သို့ fallback ပြန်ပါ [default: all]။
/viewsupport - လက်ရှိ active support links ကို ပြသပါ (override + .env defaults နှိုင်းယှဉ်)။

🛃**<u>[HEROKU] 🛃</u>**
/usage - Dyno Usage ။

🌐**<u>[CONFIG VARS] 🌐</u>**
/get_var - Heroku / .env မှ config var ရယူပါ။
/del_var - Heroku / .env မှ var တစ်ခု ဖျက်ပါ။
/set_var [Var Name] [Value] - Heroku / .env တွင် var ထည့်/update ပြုလုပ်ပါ။ Var name နှင့် value ကို space ဖြင့် ခွဲပါ။

🤖**<u>[BOT COMMANDS] 🤖</u>**
/reboot - Bot ကို reboot ပြုလုပ်ပါ။
/update - Bot ကို update ပြုလုပ်ပါ။
/speedtest - Server speeds ကို စစ်ပါ။
/maintenance [enable / disable] - Maintenance mode ။
/logger [enable / disable] - Bot သည် ရှာဖွေချက်များကို logger group တွင် မှတ်ပါမည်။
/get_log [Number of Lines] - Heroku / VPS မှ bot log ရယူပါ။
/autoend [enable|disable] - နားထောင်သူ မရှိပါက 3 မိနစ်အကြာတွင် auto stream end ။

📈**<u>[STATS COMMANDS] 📈</u>**
/activevoice - Active voice chats ကို စစ်ပါ။
/activevideo - Active video calls ကို စစ်ပါ။
/stats - Bot ၏ stats စစ်ပါ။

⚠️**<u>[BLACKLIST CHAT] ⚠️</u>**
/blacklistchat [CHAT_ID] - Chat တစ်ခုကို blacklist ထဲ ထည့်ပါ။
/whitelistchat [CHAT_ID] - Blacklisted chat တစ်ခုကို whitelist ပြန်ထည့်ပါ။
/blacklistedchat - Blacklisted chats အားလုံး စစ်ပါ။

👤**<u>[BLOCKED FUNCTION] 👤</u>**
/block [Username / Reply] - User တစ်ဦးကို bot commands သုံးခွင့်မပြုပါ။
/unblock [Username / Reply] - Bot ၏ Blocked List မှ ဖယ်ရှားပါ။
/blockedusers - Blocked Users စာရင်း စစ်ပါ။

👤**<u>[GBAN FUNCTION] 👤</u>**
/gban [Username / Reply] - User တစ်ဦးကို bot ၏ served chats အားလုံးတွင် ban ပြုလုပ်ပါ။
/ungban [Username / Reply] - Gbanned List မှ ဖယ်ရှားပါ။
/gbannedusers - Gbanned Users စာရင်း စစ်ပါ။

🎥**<u>[VIDEOCALLS] 🎥</u>**
/set_video_limit [Number of Chats] - တစ်ပြိုင်နက် Video Calls အတွက် Maximum chats အရေအတွက် သတ်မှတ်ပါ [default: 3]။
/videomode [download|m3u8] - Download mode ဖွင့်ပါက bot သည် video များကို m3u8 ဖြင့် play မလုပ်ဘဲ download ပြုလုပ်ပါမည် [default: m3u8]။

⚡️**<u>[PRIVATE BOT FUNCTION] ⚡️</u>**
/authorize [CHAT_ID] - Chat တစ်ခုကို bot သုံးခွင့်ပြုပါ။
/unauthorize [CHAT_ID] - Bot သုံးခွင့်မပြုပါ။
/authorized - Allowed chats အားလုံး စစ်ပါ။

🌐**<u>[BROADCAST FUNCTION] 🌐</u>**
**Text** သို့မဟုတ် **media** (photo, GIF, video, document, audio, sticker) ကို bot ၏ served chats အားလုံးသို့ broadcast ပါ။

**[INPUT_MODES :: 3]**
1. `/broadcast မင်္ဂလာပါ` — text broadcast ။
2. Message တစ်ခုကို **reply** လုပ်ပြီး `/broadcast` — media ပါသည် ဖြစ်စေ မပါသည် ဖြစ်စေ ။
3. Media (photo / GIF / video / etc.) ကို တင်ပြီး caption တွင် `/broadcast <သင်၏ caption>` ထည့်ပါ — media + cleaned caption ကို broadcast ပါမည်။

<u>[FLAGS :: text/caption အတွင်း မည်သည့်နေရာတွင်ဖြစ်စေ ထည့်နိုင်]</u>
**-pin** : Silent pin ထိုးပါ။
**-pinloud** : Loud notification ဖြင့် pin ထိုးပါ။
**-user** : Bot စတင်ဖူးသော users အားလုံးသို့ DM ပါ။
**-assistant** : Assistant accounts မှလည်း broadcast ပါ။
**-nobot** : Bot ၏ served chats sweep ကို skip ပါ။
**-forward** : `forward_messages` သုံးပါ ("Forwarded from" header ပြသမည်)။ **Default = `copy_message`** [forward header မပါ — advertisement / promotion အတွက် သင့်တော်]။

**Examples:**
• `/broadcast -user -assistant -pin Hello Testing` — text ကို everywhere ပို့ပြီး silent pin ။
• Promo image တင်ပြီး caption: `/broadcast -user ကျွန်ုပ်တို့၏ bot အသစ်ကို ကြည့်ပါ!` — image + caption ကို clean ပုံစံဖြင့် ပို့ပါမည်။
• Video တစ်ခုကို reply လုပ်ပြီး `/broadcast -pinloud` — video ကို copy ပြုလုပ်ပြီး (forward tag မပါ) loud pin ထိုးပါမည်။

"""


# ── public lookup ───────────────────────────────────────────────────────
_HELP = {
    1: {"en": _HELP_1_EN, "zh": _HELP_1_ZH, "my": _HELP_1_MY},
    2: {"en": _HELP_2_EN, "zh": _HELP_2_ZH, "my": _HELP_2_MY},
    3: {"en": _HELP_3_EN, "zh": _HELP_3_ZH, "my": _HELP_3_MY},
    4: {"en": _HELP_4_EN, "zh": _HELP_4_ZH, "my": _HELP_4_MY},
    5: {"en": _HELP_5_EN, "zh": _HELP_5_ZH, "my": _HELP_5_MY},
}


def get_help(num: int, lang: str = "en") -> str:
    """Return the localized HELP_<num> string. Falls back to en."""
    bucket = _HELP.get(num)
    if bucket is None:
        return ""
    # 'cn' is the repo's filename for Chinese; Telegram uses 'zh'.
    if lang == "cn":
        lang = "zh"
    return bucket.get(lang) or bucket["en"]


# Legacy English exports — kept so any other code still does helpers.HELP_X
HELP_1 = _HELP_1_EN
HELP_2 = _HELP_2_EN
HELP_3 = _HELP_3_EN
HELP_4 = _HELP_4_EN
HELP_5 = _HELP_5_EN
