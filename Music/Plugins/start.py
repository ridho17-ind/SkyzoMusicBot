import yt_dlp
from Music import (
    ASSID,
    BOT_ID,
    BOT_NAME,
    BOT_USERNAME,
    OWNER,
    SUDOERS,
    app,
)
from Music.MusicUtilities.database.chats import is_served_chat
from Music.MusicUtilities.database.queue import remove_active_chat
from Music.MusicUtilities.database.sudo import get_sudoers
from Music.MusicUtilities.helpers.inline import personal_markup
from Music.MusicUtilities.helpers.thumbnails import down_thumb
from Music.MusicUtilities.helpers.ytdl import ytdl_opts
from Music.config import GROUP, CHANNEL, BOT_IMG
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


def start_pannel():
    buttons = [
        [
            InlineKeyboardButton(text="Support​", url=f"https://t.me/{GROUP}"),
            InlineKeyboardButton(text="Updates", url=f"https://t.me/{CHANNEL}"),
        ],
        [
            InlineKeyboardButton("Command", url="https://telegra.ph/Skyzo-11-10"),
        ],
    ]
    return (
        "🎛 **{BOT_NAME} Is a bot that can play a song or video from the voice chats**",
        buttons,
    )


pstart_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "Add Me To Your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
        ],
        [
            InlineKeyboardButton("Support", url=f"https://t.me/{GROUP}"),
            InlineKeyboardButton("Updates", url=f"https://t.me/{CHANNEL}"),
        ],
        [
            InlineKeyboardButton("Cd Music", url="https://telegra.ph/Skyzo-11-10"),
            InlineKeyboardButton("Cd Dev", url="https://telegra.ph/壊Skyzo-01-21"),
            InlineKeyboardButton("Cd Stream", url="https://telegra.ph/sᴋʏᴢᴏ-ᴇx-12-21"),
        ],
    ]
)
welcome_captcha_group = 2


@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    for member in message.new_chat_members:
        try:
            if member.id in OWNER:
                return await message.reply_text(
                    f"🦸🏻‍♂️ **Owners Bot [{member.mention}] Has Joined Your Chats.**"
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    f"**🉐 Admin Bot [{member.mention}] Just Joined Your Chats.**"
                )
            if member.id == ASSID:
                await remove_active_chat(chat_id)
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(
                    f"""
👋 **Hi, Thanks For Adding Me To The Group**

🛵 **Don't Forget To Make Me Admin So Music Can Run Normally**
""",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                    disable_web_page_preview=True
                )
                return
        except BaseException:
            return


@Client.on_message(
    filters.group
    & filters.command(
        ["start", "help", f"start@{BOT_USERNAME}", f"help@{BOT_USERNAME}"]
    )
)
async def start(_, message: Message):
    chat_id = message.chat.id
    out = start_pannel()
    await message.reply_text(
        f"""
**[🚀]({BOT_IMG}) Thanks For Adding Me To {message.chat.title}.**
**㊙️ {BOT_NAME} Is Music Player And Video Player Bot**
""",
        reply_markup=InlineKeyboardMarkup(out[1]),
        disable_web_page_preview=True
    )
    return


@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def play(_, message: Message):
    if len(message.command) == 1:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await app.send_message(
            message.chat.id,
            text=f"""
**[🗣]({BOT_IMG}) Hello {rpk}! Ready Use Me?

🉐 [{BOT_NAME}](tg://user?id=2129034376) Is A Bot That Can Be Used To Listen To Songs In Voice Chat And Can Play Videos In Voice Chat!

🧰 To Find Out All The Available Command Bots, You Can Press The Two Buttons Below, Namely Cd Music, Cd Dev And Cd Stream**

""",
            parse_mode="markdown",
            reply_markup=pstart_markup,
            reply_to_message_id=message.message_id,
        )
    elif len(message.command) == 2:
        query = message.text.split(None, 1)[1]
        f1 = query[0]
        f2 = query[1]
        f3 = query[2]
        finxx = f"{f1}{f2}{f3}"
        if str(finxx) == "inf":
            query = (str(query)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                x = ytdl.extract_info(query, download=False)
            thumbnail = x["thumbnail"]
            searched_text = f"""
🔍 **Video Track Information**

❇️ **Title:** {x["title"]}

⏳ **Duration:** {round(x["duration"] / 60)} Mins
👀 **Views:** `{x["view_count"]}`
👍 **Like:** `{x["like_count"]}`
👎 **Dislike:** `{x["dislike_count"]}`
⭐️ **Rating:** {x["average_rating"]}
📹 **Channel:** {x["uploader"]}
📎 **Channel Link:** [Kunjungi Dari Sini]({x["channel_url"]})
🔗 **Link:** [Link]({x["webpage_url"]})
"""
            link = x["webpage_url"]
            buttons = personal_markup(link)
            userid = message.from_user.id
            thumb = await down_thumb(thumbnail, userid)
            await app.send_photo(
                message.chat.id,
                photo=thumb,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        if str(finxx) == "sud":
            sudoers = await get_sudoers()
            text = "**💻 SUDO USERS FLICKS BOT**\n\n"
            for count, user_id in enumerate(sudoers, 1):
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name if not user.mention else user.mention
                except Exception:
                    continue
                text += f"- {user}\n"
            if not text:
                await message.reply_text("Tidak Ada Pengguna Sudo")
            else:
                await message.reply_text(text)
