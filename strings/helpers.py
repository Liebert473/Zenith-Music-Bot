#
# Help-menu text for the /help inline panel.
# Localized for en / zh / my (Burmese). Other languages fall back to en.
#
# Public API:
#   helpers.get_help(num: int, lang: str = "en") -> str
#   helpers.HELP_1 ... HELP_5  (legacy English shortcuts, still exported)
#


# ── HELP_1: Admin Commands ──────────────────────────────────────────────
_HELP_1_EN = """✅<b><u>Admin Commands:</u></b>

<b>c</b> stands for channel play.

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


✅<u><b>Specific Skip:</b></u>
/skip or /cskip [Number(example: 3)]
    - Skips music to a the specified queued number. Example: /skip 3 will skip music to third queued music and will ignore 1 and 2 music in queue.

✅<u><b>Loop Play:</b></u>
/loop or /cloop [enable/disable] or [Numbers between 1-10]
    - When activated, bot loops the current playing music to 1-10 times on voice chat. Default to 10 times.

✅<u><b>Auth Users:</b></u>
Auth Users can use admin commands without admin rights in your chat.

/auth [Username] - Add a user to AUTH LIST of the group.
/unauth [Username] - Remove a user from AUTH LIST of the group.
/authusers - Check AUTH LIST of the group."""


_HELP_1_ZH = """✅<b><u>管理员命令:</u></b>

<b>c</b> 表示频道播放（channel play）。

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


✅<u><b>指定跳过:</b></u>
/skip 或 /cskip [数字（例如：3）]
    - 跳到队列中指定位置的歌曲。例如 /skip 3 会直接跳到队列第 3 首，前两首被忽略。

✅<u><b>循环播放:</b></u>
/loop 或 /cloop [enable/disable] 或 [1-10 之间的数字]
    - 启用后，机器人会将当前播放的音乐循环 1-10 次。默认 10 次。

✅<u><b>授权用户 (AUTH):</b></u>
授权用户无需管理员权限即可使用管理员命令。

/auth [用户名] - 将用户添加到此群的授权名单。
/unauth [用户名] - 从授权名单移除用户。
/authusers - 查看此群的授权名单。"""


_HELP_1_MY = """✅<b><u>🛡️ Admin Commands</u></b>

⚡ <b>c</b> = channel play

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


✅<u><b>🔢 Specific Skip</b></u>
/skip / /cskip [Number e.g. 3]
    - Queue ထဲရှိ သီးခြား position သို့ ကျော်ပါ။ ဥပမာ <code>/skip 3</code> သည် queue ထဲ track #3 သို့ တိုက်ရိုက် ကျော်သည် [#1, #2 ကို ကျော်လွန်] ။

✅<u><b>🔁 Loop Play</b></u>
/loop / /cloop [enable/disable] / [1-10 အကြား ဂဏန်း]
    - လက်ရှိ track ကို 1-10 ကြိမ်အထိ loop ပြုလုပ်ပါမည် [default: 10]။

✅<u><b>🎩 Auth Users</b></u>
Auth Users များသည် admin rights မပါဘဲ admin commands များ သုံးနိုင်ပါသည်။

/auth [Username] - User တစ်ဦးကို group ၏ AUTH LIST ထဲ ထည့်ပါ။
/unauth [Username] - User တစ်ဦးကို AUTH LIST မှ ဖယ်ရှားပါ။
/authusers - Group ၏ AUTH LIST ကို ပြသပါ။"""


# ── HELP_2: Play Commands ───────────────────────────────────────────────
_HELP_2_EN = """✅<u><b>Play Commands:</b></u>

Available Commands = play , vplay , cplay

ForcePlay Commands = playforce , vplayforce , cplayforce

<b>c</b> stands for channel play.
<b>v</b> stands for video play.
<b>force</b> stands for force play.

/play or /vplay or /cplay  - Bot will start playing your given query on voice chat or Stream live links on voice chats.

/playforce or /vplayforce or /cplayforce -  <b>Force Play</b> stops the current playing track on voice chat and starts playing the searched track instantly without disturbing/clearing queue.

/channelplay [Chat username or id] or [Disable] - Connect channel to a group and stream music on channel's voice chat from your group.


✅<b><u>Bot's Server Playlists:</u></b>
/playlist  - Check Your Saved Playlist On Servers.
/deleteplaylist - Delete any saved music in your playlist
/play  - Start playing Your Saved Playlist from Servers."""


_HELP_2_ZH = """✅<u><b>播放命令:</b></u>

可用命令 = play , vplay , cplay

强制播放命令 = playforce , vplayforce , cplayforce

<b>c</b> = 频道播放（channel play）
<b>v</b> = 视频播放（video play）
<b>force</b> = 强制播放

/play 或 /vplay 或 /cplay - 在语音聊天中播放你提供的搜索词或链接（包括 live 流）。

/playforce 或 /vplayforce 或 /cplayforce - <b>强制播放</b>：停止当前曲目，立即播放搜索结果，不清空队列。

/channelplay [频道用户名或 ID] 或 [Disable] - 将群组连接到频道，从群组发起命令在频道语音聊天中播放音乐。


✅<b><u>服务器端播放列表:</u></b>
/playlist - 查看保存在服务器上的个人播放列表。
/deleteplaylist - 删除播放列表中的某首歌。
/play - 直接从服务器播放列表开始播放。"""


_HELP_2_MY = """✅<u><b>🎶 Play Commands</b></u>

📡 Available = play , vplay , cplay
⚡ ForcePlay = playforce , vplayforce , cplayforce

▰ <b>c</b> = channel play
▰ <b>v</b> = video play
▰ <b>force</b> = force play

/play / /vplay / /cplay - သင်ပေးသော query / link ကို voice chat တွင် play သို့မဟုတ် live stream ပြုလုပ်ပါမည်။

/playforce / /vplayforce / /cplayforce - <b>Force Play</b> ⚡ : လက်ရှိ track ကို ရပ်ပြီး ရှာထားသော track ကို ချက်ချင်း play ပါသည် [queue မပျောက်ပါ]။

/channelplay [Channel username/id] / [Disable] - Group ကို channel တစ်ခုနှင့် ချိတ်ဆက်ပြီး channel ၏ voice chat တွင် music stream ပြုလုပ်ပါ။


✅<b><u>💾 Server Playlists</u></b>
/playlist - Server တွင် သင် save ထားသော playlist ကို ကြည့်ပါ။
/deleteplaylist - Playlist ထဲမှ track တစ်ပုဒ်ကို ဖျက်ပါ။
/play - Server ၏ saved playlist ကို play စတင်ပါ။"""


# ── HELP_3: Bot Commands ────────────────────────────────────────────────
_HELP_3_EN = """✅<u><b>Bot Commands:</b></u>

/stats - Get Top 10 Tracks Global Stats, Top 10 Users of bot, Top 10 Chats on bot, Top 10 Played in a chat etc etc.

/sudolist - Check Sudo Users of Yukki Music Bot

/lyrics [Music Name] - Searches Lyrics for the particular Music on web.

/song [Track Name] or [YT Link] - Download any track from youtube in mp3 or mp4 formats.

/player -  Get a interactive Playing Panel.

<b>c</b> stands for channel play.

/queue or /cqueue- Check Queue List of Music."""


_HELP_3_ZH = """✅<u><b>机器人命令:</b></u>

/stats - 查看 Top 10 全局曲目、用户、群聊以及本群 Top 10 等统计。

/sudolist - 查看 Yukki Music Bot 的 Sudo 用户列表。

/lyrics [歌曲名] - 在网上搜索指定歌曲的歌词。

/song [歌曲名] 或 [YouTube 链接] - 从 YouTube 下载音频（mp3）或视频（mp4）。

/player - 打开交互式的播放面板。

<b>c</b> 表示频道播放。

/queue 或 /cqueue - 查看当前播放队列。"""


_HELP_3_MY = """✅<u><b>🤖 Bot Commands</b></u>

/stats - 📊 Top 10 Tracks (Global), Top 10 Users, Top 10 Chats, Top 10 Played per chat စတဲ့ telemetry အပြည့်အစုံ။

/sudolist - ⭐ Yukki Music Bot ၏ Sudo Users စာရင်း။

/lyrics [Music Name] - 📖 သီးခြား music အတွက် lyrics web မှ ရှာပါ။

/song [Track Name] / [YT Link] - 💾 YouTube မှ track ကို mp3 / mp4 format ဖြင့် download ပြုလုပ်ပါ။

/player - 🎛️ Interactive playing panel ဖွင့်ပါ။

▰ <b>c</b> = channel play

/queue / /cqueue - 📑 Music ၏ Queue List ကို ပြသပါ။"""


# ── HELP_4: Extra Commands + Settings ───────────────────────────────────
_HELP_4_EN = """✅<u><b>Extra Commands:</b></u>
/start - Start the Music Bot.
/help  - Get Commands Helper Menu with detailed explanations of commands.
/ping- Ping the Bot and check Ram, Cpu etc stats of Bot.

✅<u><b>Group Settings:</b></u>
/settings - Get a complete group's settings with inline buttons

🔗 <b>Options in Settings:</b>

1️⃣ You can set <b>Audio Quality</b> you want to stream on voice chat.

2️⃣ You can set <b>Video Quality</b> you want to stream on voice chat.

3️⃣ <b>Auth Users</b>:- You can change admin commands mode from here to everyone or admins only. If everyone, anyone present in you group will be able to use admin commands(like /skip, /stop etc)

4️⃣ <b>Clean Mode:</b> When enabled deletes the bot's messages after 5 mins from your group to make sure your chat remains clean and good.

5️⃣ <b>Command Clean</b> : When activated, Bot will delete its executed commands (/play, /pause, /shuffle, /stop etc) immediately.

6️⃣ <b>Play Settings:</b>

/playmode - Get a complete play settings panel with buttons where you can set your group's play settings.

<u>Options in playmode:</u>

1️⃣ <b>Search Mode</b> [Direct or Inline] - Changes your search mode while you give /play mode.

2️⃣ <b>Admin Commands</b> [Everyone or Admins] - If everyone, anyone present in you group will be able to use admin commands(like /skip, /stop etc)

3️⃣ <b>Play Type</b> [Everyone or Admins] - If admins, only admins present in group can play music on voice chat."""


_HELP_4_ZH = """✅<u><b>额外命令:</b></u>
/start - 启动机器人。
/help - 打开命令帮助菜单（含详细说明）。
/ping - Ping 机器人并查看 RAM、CPU 等状态。

✅<u><b>群组设置:</b></u>
/settings - 通过内联按钮打开完整的群组设置面板。

🔗 <b>设置选项:</b>

1️⃣ <b>音频质量</b> - 设置语音聊天中流式播放的音频质量。

2️⃣ <b>视频质量</b> - 设置视频质量。

3️⃣ <b>授权用户</b>:- 设置管理员命令权限模式：全员可用 或 仅管理员。若选「全员」，群内任何人都可以用 /skip /stop 等命令。

4️⃣ <b>Clean Mode</b>：启用后机器人会在 5 分钟后删除自己发的消息，保持群组整洁。

5️⃣ <b>Command Clean</b>：启用后机器人会立刻删除已执行的命令（/play /pause /shuffle /stop 等）。

6️⃣ <b>播放设置:</b>

/playmode - 打开播放设置面板，按钮可调。

<u>playmode 中的选项:</u>

1️⃣ <b>搜索模式</b> [Direct / Inline] - 改变 /play 时的搜索方式。

2️⃣ <b>管理员命令</b> [Everyone / Admins] - 若选「Everyone」，群内任何人都可使用管理员命令。

3️⃣ <b>播放类型</b> [Everyone / Admins] - 若选「Admins」，只有管理员可在语音聊天中播放音乐。"""


_HELP_4_MY = """✅<u><b>⚡ Extra Commands</b></u>
/start - 🛸 Music Bot ကို စတင်ပါ။
/help - 📜 Commands များ၏ အသေးစိတ်ဖော်ပြချက်ပါ helper menu ဖွင့်ပါ။
/ping - ⚡ Ping + RAM, CPU စသော stats စစ်ပါ။

✅<u><b>⚙️ Group Settings</b></u>
/settings - Inline buttons ပါသော group settings panel ဖွင့်ပါ။

🔗 <b>Settings အတွင်း Options:</b>

1️⃣ <b>🎚️ Audio Quality</b> - Voice chat တွင် stream ပြုလုပ်လိုသော audio quality သတ်မှတ်ပါ။

2️⃣ <b>🎥 Video Quality</b> - Video quality သတ်မှတ်ပါ။

3️⃣ <b>🎩 Auth Users</b> - Admin commands mode ပြောင်းပါ [everyone / admins only]။ <code>Everyone</code> ဆိုပါက group ထဲ ရှိသူတိုင်း /skip, /stop စသော commands သုံးနိုင်ပါမည်။

4️⃣ <b>🔄 Clean Mode</b> - ဖွင့်ထားသောအခါ Bot ၏ messages များကို 5 မိနစ်အကြာတွင် ဖျက်ပစ်ပြီး chat ကို သန့်ရှင်းပါသည်။

5️⃣ <b>🗑 Command Clean</b> - ဖွင့်ထားသောအခါ executed commands များ (/play, /pause, /shuffle, /stop) ကို ချက်ချင်း ဖျက်ပစ်ပါသည်။

6️⃣ <b>▶️ Play Settings:</b>

/playmode - Group ၏ play settings panel ဖွင့်ပါ။

<u>playmode အတွင်း Options:</u>

1️⃣ <b>🔎 Search Mode</b> [Direct / Inline] - /play သုံးချိန် search mode ပြောင်းပါ။

2️⃣ <b>🛡️ Admin Commands</b> [Everyone / Admins] - <code>Everyone</code> ဆိုပါက group ထဲ ရှိသူတိုင်း admin commands သုံးနိုင်သည်။

3️⃣ <b>🫂 Play Type</b> [Everyone / Admins] - <code>Admins</code> ဆိုပါက admins များသာ voice chat တွင် music play နိုင်သည်။"""


# ── HELP_5: Sudo / Owner Commands — PAGE 1 (user/start/support/bot mgmt) ──
_HELP_5p1_EN = """📄 <b>Sudo Commands — Page 1 / 2</b>
🔐 = Owner only  |  ✅ = Sudo accessible

🔰<b><u>SUDO USERS [🔐 Owner]:</u></b>
/addsudo [Username or Reply] — Add to sudo list.
/delsudo [Username or Reply] — Remove from sudo list.
/sudolist — View all sudo users. (public)

🛸<b><u>START CUSTOMIZATION [🔐 Owner]:</u></b>
/setstart [text] or reply — Set welcome text. <code>{bot}</code> = bot name.
/setstartimg — Reply to photo or provide [url] to set welcome image.
/clearstart [text|image|all] — Clear custom start. Default: <code>all</code>.
/viewstart — Preview current /start.

🔗<b><u>SUPPORT LINKS [🔐 Owner]:</u></b>
/setsupportgroup or /setgroup [@user | t.me/...] — Set support group link.
/setsupportchannel or /setchannel [@user | t.me/...] — Set support channel link.
/clearsupport [group|channel|all] — Clear override. Default: <code>all</code>.
/viewsupport — Show active links (override vs .env).

🛃<b><u>CONFIG [🔐 Owner]:</u></b>
/vars — View all current config vars.
/usage — Dyno usage.
/get_var — Read a config var.
/del_var — Delete a config var.
/set_var [Name] [Value] — Set/update a config var.

🤖<b><u>BOT MANAGEMENT:</u></b>
🔐 /reboot — Reboot the bot.
🔐 /update — Pull updates and restart.
🔐 /get_log [lines] — Fetch bot log.
🔐 /maintenance [enable|disable] — Toggle maintenance mode.
✅ /speedtest — Server speed check.
✅ /logger [enable|disable] — Log queries to logger group.
✅ /autoend [enable|disable] — Auto-end stream after 3 min idle."""


# ── HELP_5: Sudo / Owner Commands — PAGE 2 (moderation / broadcast) ────
_HELP_5p2_EN = """📄 <b>Sudo Commands — Page 2 / 2</b>

📈<b><u>STATS:</u></b>
/activevoice — Active voice chats.
/activevideo — Active video calls.
/stats — Overall bot stats.

⚠️<b><u>BLACKLIST CHAT:</u></b>
/blacklistchat [CHAT_ID] — Block a chat from using the bot.
/whitelistchat [CHAT_ID] — Unblock a chat.
/blacklistedchat — List all blocked chats.

👤<b><u>BLOCK / GBAN:</u></b>
/block [User or Reply] — Block a user from bot commands.
/unblock [User or Reply] — Unblock a user.
/blockedusers — View blocked users.
/gban [User or Reply] — Global-ban a user across all served chats.
/ungban [User or Reply] — Remove global ban.
/gbannedusers — View gbanned users.

🎥<b><u>VIDEO CALLS:</u></b>
/set_video_limit [N] — Max simultaneous video-call chats (default 3).
/videomode [download|m3u8] — Switch video delivery mode.

⚡️<b><u>PRIVATE BOT:</u></b>
/authorize [CHAT_ID] — Allow a chat to use the bot.
/unauthorize [CHAT_ID] — Remove a chat's access.
/authorized — List allowed chats.

🌐<b><u>BROADCAST:</u></b>
Sends text <b>or media</b> (photo, GIF, video, doc, audio, sticker) to all served chats.

<b>Input modes:</b>
1. <code>/broadcast Hello</code> — plain text.
2. Reply to any message + <code>/broadcast</code> — copies it (no "Forwarded from").
3. Upload media + caption <code>/broadcast text</code> — sends media cleanly.

<b>Flags:</b>
<code>-pin</code> — Silent-pin in each chat.
<code>-pinloud</code> — Pin with notification; overrides <code>-pin</code>.
<code>-user</code> — Also DM every served user.
<code>-nobot</code> — Skip served chats (pair with <code>-user</code> / <code>-assistant</code>).
<code>-assistant</code> — Also send via assistant userbot accounts.
<code>-forward</code> — Show "Forwarded from". Default: <code>copy_message</code> (no header).

<b>Example:</b> reply to a promo image + <code>/broadcast -user -pin</code>"""


# ── PAGE 1: Chinese ─────────────────────────────────────────────────────
_HELP_5p1_ZH = """📄 <b>Sudo 命令 — 第 1 / 2 页</b>
🔐 = 仅主人  |  ✅ = Sudo 可用

🔰<b><u>Sudo 用户 [🔐 主人]:</u></b>
/addsudo [用户名 或 回复] — 加入 sudo 名单。
/delsudo [用户名 或 回复] — 移出 sudo 名单。
/sudolist — 查看 sudo 用户列表。（公开）

🛸<b><u>/start 自定义 [🔐 主人]:</u></b>
/setstart [文本] 或 回复消息 — 设置欢迎文本，<code>{bot}</code> = 机器人名字。
/setstartimg — 回复图片或提供 [url] 设为欢迎图。
/clearstart [text|image|all] — 清除自定义。默认 <code>all</code>。
/viewstart — 预览当前 /start。

🔗<b><u>支持链接 [🔐 主人]:</u></b>
/setsupportgroup 或 /setgroup [@用户名 | t.me/...] — 设置支持群组。
/setsupportchannel 或 /setchannel [@用户名 | t.me/...] — 设置支持频道。
/clearsupport [group|channel|all] — 清除覆盖。默认 <code>all</code>。
/viewsupport — 显示当前生效链接。

🛃<b><u>配置 [🔐 主人]:</u></b>
/vars — 查看所有配置变量。
/usage — Dyno 使用量。
/get_var — 读取配置变量。
/del_var — 删除配置变量。
/set_var [名称] [值] — 设置 / 更新配置变量。

🤖<b><u>机器人管理:</u></b>
🔐 /reboot — 重启机器人。
🔐 /update — 拉取更新并重启。
🔐 /get_log [行数] — 获取日志。
🔐 /maintenance [enable|disable] — 维护模式开关。
✅ /speedtest — 服务器测速。
✅ /logger [enable|disable] — 查询日志记录。
✅ /autoend [enable|disable] — 无人收听 3 分钟自动结束。"""


# ── PAGE 2: Chinese ─────────────────────────────────────────────────────
_HELP_5p2_ZH = """📄 <b>Sudo 命令 — 第 2 / 2 页</b>

📈<b><u>统计:</u></b>
/activevoice — 当前活跃语音聊天。
/activevideo — 当前活跃视频通话。
/stats — 机器人整体统计。

⚠️<b><u>群组黑名单:</u></b>
/blacklistchat [CHAT_ID] — 将聊天加入黑名单。
/whitelistchat [CHAT_ID] — 从黑名单移除。
/blacklistedchat — 查看黑名单列表。

👤<b><u>屏蔽 / 全局封禁:</u></b>
/block [用户 或 回复] — 屏蔽某用户。
/unblock [用户 或 回复] — 取消屏蔽。
/blockedusers — 查看屏蔽列表。
/gban [用户 或 回复] — 全局封禁（所有服务群）。
/ungban [用户 或 回复] — 解除全局封禁。
/gbannedusers — 查看封禁列表。

🎥<b><u>视频通话:</u></b>
/set_video_limit [N] — 最大同时视频通话群数（默认 3）。
/videomode [download|m3u8] — 切换视频传输模式。

⚡️<b><u>私有机器人:</u></b>
/authorize [CHAT_ID] — 允许某聊天使用机器人。
/unauthorize [CHAT_ID] — 禁止某聊天使用机器人。
/authorized — 查看已授权列表。

🌐<b><u>广播:</u></b>
发送 <b>文字或媒体</b>（图片 / GIF / 视频 / 文档 / 音频 / 贴纸）到所有服务群。

<b>输入方式:</b>
1. <code>/broadcast 你好</code> — 纯文字。
2. 回复任意消息 + <code>/broadcast</code> — 复制（无转发标签）。
3. 上传媒体 + caption 写 <code>/broadcast 文字</code> — 干净发送。

<b>标志:</b>
<code>-pin</code> — 在各群静默置顶。
<code>-pinloud</code> — 有通知置顶；覆盖 <code>-pin</code>。
<code>-user</code> — 同时私信所有已启动用户。
<code>-nobot</code> — 跳过服务群（配合 <code>-user</code> / <code>-assistant</code>）。
<code>-assistant</code> — 同时通过助手账号发送。
<code>-forward</code> — 显示「转发自」。默认：<code>copy_message</code>（无标签）。

<b>示例:</b> 回复推广图 + <code>/broadcast -user -pin</code>"""


# ── PAGE 1: Burmese ──────────────────────────────────────────────────────
_HELP_5p1_MY = """📄 <b>Sudo Commands · Page 1 / 2</b>
🔐 = Owner သာ  |  ✅ = Sudo သုံးနိုင်

🔰<b><u>Sudo Users [🔐 Owner]</u></b>
/addsudo [Username / Reply] — Sudo list ထဲ ထည့်ပါ။
/delsudo [Username / Reply] — Sudo list မှ ဖယ်ပါ။
/sudolist — Sudo users စာရင်း ကြည့်ပါ (public)။

🛸<b><u>/start Customization [🔐 Owner]</u></b>
/setstart [text] / reply — Welcome text သတ်မှတ်ပါ (<code>{bot}</code> = bot name)။
/setstartimg — Photo reply / URL ဖြင့် welcome image သတ်မှတ်ပါ။
/clearstart [text|image|all] — Custom /start ဖျက်ပါ [default: all]။
/viewstart — Custom /start preview ကြည့်ပါ။

🔗<b><u>Support Links [🔐 Owner]</u></b>
/setsupportgroup / /setgroup [@user | t.me/...] — Support group link သတ်မှတ်ပါ။
/setsupportchannel / /setchannel [@user | t.me/...] — Support channel link သတ်မှတ်ပါ။
/clearsupport [group|channel|all] — Override ဖျက်ပြီး .env fallback [default: all]။
/viewsupport — Active links ကြည့်ပါ (override vs .env)။

🛃<b><u>Config [🔐 Owner]</u></b>
/vars — Config vars အားလုံး ကြည့်ပါ။
/usage — Dyno usage ။
/get_var — Config var ရယူပါ။
/del_var — Config var ဖျက်ပါ။
/set_var [Name] [Value] — Config var ထည့်/update ပါ။

🤖<b><u>Bot Management</u></b>
🔐 /reboot — Bot restart ပြုလုပ်ပါ။
🔐 /update — Update ဆွဲပြီး restart ပါ။
🔐 /get_log [lines] — Bot log ရယူပါ။
🔐 /maintenance [enable|disable] — Maintenance mode ။
✅ /speedtest — Server speed စစ်ပါ။
✅ /logger [enable|disable] — Query logging ။
✅ /autoend [enable|disable] — 3 မိနစ် idle ဆိုပါက auto stream end ။"""


# ── PAGE 2: Burmese ──────────────────────────────────────────────────────
_HELP_5p2_MY = """📄 <b>Sudo Commands · Page 2 / 2</b>

📈<b><u>Stats</u></b>
/activevoice — Active voice chats ။
/activevideo — Active video calls ။
/stats — Bot stats စစ်ပါ။

⚠️<b><u>Blacklist Chat</u></b>
/blacklistchat [CHAT_ID] — Chat ကို blacklist ထည့်ပါ။
/whitelistchat [CHAT_ID] — Blacklist မှ ဖယ်ပါ။
/blacklistedchat — Blacklisted chats ကြည့်ပါ။

👤<b><u>Block / GBan</u></b>
/block [User / Reply] — User ကို bot commands သုံးခွင့်မပြုပါ။
/unblock [User / Reply] — Unblock ပြုလုပ်ပါ။
/blockedusers — Blocked users ကြည့်ပါ။
/gban [User / Reply] — Served chats အားလုံးတွင် ban ပြုလုပ်ပါ။
/ungban [User / Reply] — Gban ဖြုတ်ပါ။
/gbannedusers — Gbanned users ကြည့်ပါ။

🎥<b><u>Video Calls</u></b>
/set_video_limit [N] — Max video call chats [default: 3]။
/videomode [download|m3u8] — Video delivery mode ပြောင်းပါ။

⚡️<b><u>Private Bot</u></b>
/authorize [CHAT_ID] — Chat ကို bot သုံးခွင့်ပြုပါ။
/unauthorize [CHAT_ID] — ခွင့်မပြုပါ။
/authorized — Allowed chats ကြည့်ပါ။

🌐<b><u>Broadcast</u></b>
Text / media (photo, GIF, video, doc, audio, sticker) ကို served chats အားလုံးသို့ ပို့ပါ။

<b>Input Modes</b>
1. <code>/broadcast မင်္ဂလာပါ</code> — Text ။
2. Message ကို reply + <code>/broadcast</code> — copy ပြုလုပ်ပါ (forward tag မပါ)။
3. Media upload + caption တွင် <code>/broadcast text</code> — media + text ပို့ပါ။

<b>Flags:</b>
<code>-pin</code> — Served chats တစ်ခုစီတွင် silent-pin ပြုလုပ်ပါ။
<code>-pinloud</code> — Notification ပါ pin; <code>-pin</code> ကို override ပြုလုပ်သည်။
<code>-user</code> — Served users အားလုံးကို DM ပါ ပို့ပါ။
<code>-nobot</code> — Served chats ကို ကျော်ပါ (<code>-user</code> / <code>-assistant</code> နှင့် တွဲသုံးပါ)။
<code>-assistant</code> — Assistant userbot accounts ဖြင့်လည်း ပို့ပါ။
<code>-forward</code> — "Forwarded from" ပြသသည်။ Default: <code>copy_message</code> (tag မပါ)။

<b>Example:</b> Promo image ကို reply + <code>/broadcast -user -pin</code>"""


# ── public lookup ───────────────────────────────────────────────────────
_HELP = {
    1: {"en": _HELP_1_EN, "zh": _HELP_1_ZH, "my": _HELP_1_MY},
    2: {"en": _HELP_2_EN, "zh": _HELP_2_ZH, "my": _HELP_2_MY},
    3: {"en": _HELP_3_EN, "zh": _HELP_3_ZH, "my": _HELP_3_MY},
    4: {"en": _HELP_4_EN, "zh": _HELP_4_ZH, "my": _HELP_4_MY},
    # HELP_5 is paginated — key 5 = page 1, key "5b" = page 2.
    5:    {"en": _HELP_5p1_EN, "zh": _HELP_5p1_ZH, "my": _HELP_5p1_MY},
    "5b": {"en": _HELP_5p2_EN, "zh": _HELP_5p2_ZH, "my": _HELP_5p2_MY},
}


def get_help(num, lang: str = "en") -> str:
    """Return the localized HELP_<num> string.

    num can be 1-4 (int) or 5 / "5b" (HELP_5 is paginated):
      get_help(5,   lang)  → page 1 of sudo/owner commands
      get_help("5b", lang) → page 2 of sudo/owner commands
    Falls back to English when the requested language is not available.
    """
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
HELP_5 = _HELP_5p1_EN  # legacy alias points to page 1
