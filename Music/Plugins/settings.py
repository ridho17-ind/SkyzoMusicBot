import asyncio
import psutil
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
from Music.MusicUtilities.database.assistant import (_get_assistant, get_as_names, get_assistant,
                        save_assistant)
from Music.MusicUtilities.database.auth import (_get_authusers, add_nonadmin_chat, delete_authuser,
                   get_authuser, get_authuser_count, get_authuser_names,
                   is_nonadmin_chat, remove_nonadmin_chat, save_authuser)
from Music.MusicUtilities.database.blacklistchat import blacklist_chat, blacklisted_chats, whitelist_chat

from Music.MusicUtilities.tgcallsrun.music import pytgcalls
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

text = f"**PENGATURAN {BOT_NAME}**"

@app.on_message(filters.command("dashboard") & filters.group)
async def settings(_, message: Message):
    c_id = message.chat.id
    _check = await get_assistant(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_assistant(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    await message.reply_text(f"{text}\n\n**Group:** {message.chat.title}\n**Group ID:** {message.chat.id}\n**Volume Level:** {volume}%", 
                  reply_markup=InlineKeyboardMarkup([
            [
            InlineKeyboardButton(text="🔈 ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ", callback_data="AQ"),
            InlineKeyboardButton(text="🎚 ᴀᴜᴅɪᴏ ᴠᴏʟᴜᴍᴇ", callback_data="AV"),
            ],
            [
            InlineKeyboardButton(
                text="👥 ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs", callback_data="AU"
            ),
            InlineKeyboardButton(
                text="💻 ᴅᴀsʜʙᴏᴀʀᴅ", callback_data="Dashboard"
            ),
            ],
            [
            InlineKeyboardButton(text="✖️ ᴄʟᴏsᴇ", callback_data="close"),
            ],
           ]
        )
      )

@app.on_callback_query(filters.regex("settingm"))
async def settingm(_, CallbackQuery):
    await CallbackQuery.answer("Bot Settings ...")
    buttons = [
        [
            InlineKeyboardButton(text="🔈 ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ", callback_data="AQ"),
            InlineKeyboardButton(text="🎚 ᴀᴜᴅɪᴏ ᴠᴏʟᴜᴍᴇ", callback_data="AV"),
        ],
        [
            InlineKeyboardButton(
                text="👥 ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs", callback_data="AU"
            ),
            InlineKeyboardButton(
                text="💻 ᴅᴀsʜʙᴏᴀʀᴅ", callback_data="Dashboard"
            ),
        ],
        [
            InlineKeyboardButton(text="✖️ ᴄʟᴏsᴇ", callback_data="close"),
        ],
    ]
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    _check = await get_assistant(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_assistant(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    await CallbackQuery.edit_message_text(
        text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("EVE"))
async def EVE(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    buttons = [
        [
            InlineKeyboardButton(text="👥 ᴇᴠʀʏᴏɴᴇ", callback_data="EVE"),
            InlineKeyboardButton(text="🙍 ᴀᴅᴍɪɴs", callback_data="AMS"),
        ],
        [
            InlineKeyboardButton(
                text="📋 ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ ʟɪsᴛ", callback_data="USERLIST"
            )
        ],
        [InlineKeyboardButton(text="🔙 ʙᴀᴄᴋ", callback_data="settingm")],
    ]
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer("Changes Saved")
        await add_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nAdmins Commands Mode to **Everyone**\n\nNow anyone present in this group can skip, pause, resume, stop music.\n\nChanges Done By @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await CallbackQuery.answer(
            "Commands Mode is Already Set To EVERYONE", show_alert=True
        )

@app.on_callback_query(filters.regex("AMS"))
async def AMS(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    buttons = [
        [
            InlineKeyboardButton(text="👥 ᴇᴠʀʏᴏɴᴇ", callback_data="EVE"),
            InlineKeyboardButton(text="🙍 ᴀᴅᴍɪɴs", callback_data="AMS"),
        ],
        [
            InlineKeyboardButton(
                text="📋 ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ ʟɪsᴛ", callback_data="USERLIST"
            )
        ],
        [InlineKeyboardButton(text="🔙 ʙᴀᴄᴋ", callback_data="settingm")],
    ]
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer(
            "Commands Mode is Already Set To ADMINS ONLY", show_alert=True
        )
    else:
        await CallbackQuery.answer("Changes Saved")
        await remove_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nSet Commands Mode to **Admins**\n\nNow only Admins present in this group can skip, pause, resume, stop musics.\n\nChanges Done By @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(
    filters.regex(
        pattern=r"^(AQ|AV|AU|Dashboard|HV|LV|MV|HV|VAM|Custommarkup|PTEN|MTEN|PTF|MTF|PFZ|MFZ|USERLIST|UPT|CPT|RAT|DIT)$"
    )
)
async def start_markup_check(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    if command == "AQ":
        await CallbackQuery.answer("Already in Best Quality", show_alert=True)
    if command == "AV":
        await CallbackQuery.answer("Bot Settings ...")
        buttons = [
        [
            InlineKeyboardButton(
                text="🔄 ʀᴇsᴇᴛ ᴀᴜᴅɪᴏ ᴠᴏʟᴜᴍᴇ 🔄", callback_data="HV"
            )
        ],
        [
            InlineKeyboardButton(text="🔈 ʟᴏᴡ ᴠᴏʟ", callback_data="LV"),
            InlineKeyboardButton(text="🔉 ᴍᴇᴅɪᴜᴍ ᴠᴏʟ", callback_data="MV"),
        ],
        [
            InlineKeyboardButton(text="🔊 ʜɪɢʜ ᴠᴏʟ", callback_data="HV"),
            InlineKeyboardButton(text="🔈 ᴀᴍᴘʟɪғɪᴇᴅ ᴠᴏʟ", callback_data="VAM"),
        ],
        [
            InlineKeyboardButton(
                text="🔽 ᴄᴜsᴛᴏᴍ ᴠᴏʟᴜᴍᴇ 🔽", callback_data="Custommarkup"
            )
        ],
        [InlineKeyboardButton(text="🔙 ʙᴀᴄᴋ", callback_data="settingm")],
        ]
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "AU":
        await CallbackQuery.answer("Bot Settings ...")
        buttons = [
        [
            InlineKeyboardButton(text="👥 ᴇᴠʀʏᴏɴᴇ", callback_data="EVE"),
            InlineKeyboardButton(text="🙍 ᴀᴅᴍɪɴs", callback_data="AMS"),
        ],
        [
            InlineKeyboardButton(
                text="📋 ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ ʟɪsᴛ", callback_data="USERLIST"
            )
        ],
        [InlineKeyboardButton(text="🔙 ʙᴀᴄᴋ", callback_data="settingm")],
        ]
        is_non_admin = await is_nonadmin_chat(chat_id)
        if not is_non_admin:
            current = "Admins Only"
        else:
            current = "Everyone"
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n\nCurrently Who Can Use {BOT_NAME}:- **{current}**\n\n**⁉️ What is This?**\n\n**👥 Everyone :-**Anyone can use {BOT_NAME}'s commands(skip, pause, resume etc) present in this group.\n\n**🙍 Admin Only :-**  Only the admins and authorized users can use all commands of {BOT_NAME}.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Dashboard":
        await CallbackQuery.answer("Dashboard...")
        buttons = [
        [
            InlineKeyboardButton(text="✔️ ᴜᴘᴛɪᴍᴇ", callback_data="UPT"),
            InlineKeyboardButton(text="💾 ʀᴀᴍ", callback_data="RAT"),
        ],
        [
            InlineKeyboardButton(text="💻 ᴄᴘᴜ", callback_data="CPT"),
            InlineKeyboardButton(text="💽 ᴅɪsᴋ", callback_data="DIT"),
        ],
        [InlineKeyboardButton(text="🔙 ʙᴀᴄᴋ", callback_data="settingm")],
        ]
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n\nCheck {BOT_NAME}'s System Stats In the DashBoard Here! More Functions adding very soon! Keep on Checking Support Channel.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Custommarkup":
        await CallbackQuery.answer("Bot Settings ...")
        buttons = [
        [
            InlineKeyboardButton(text="+10", callback_data="PTEN"),
            InlineKeyboardButton(text="-10", callback_data="MTEN"),
        ],
        [
            InlineKeyboardButton(text="+25", callback_data="PTF"),
            InlineKeyboardButton(text="-25", callback_data="MTF"),
        ],
        [
            InlineKeyboardButton(text="+50", callback_data="PFZ"),
            InlineKeyboardButton(text="-50", callback_data="MFZ"),
        ],
        [InlineKeyboardButton(text="🔼 ᴄᴜsᴛᴏᴍ ᴠᴏʟᴜᴍᴇ 🔼", callback_data="AV")],
        ]
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "LV":
        assis = {
            "volume": 25,
        }
        volume = 25
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        buttons = [
        [
            InlineKeyboardButton(
                text="🔄 ʀᴇsᴇᴛ ᴀᴜᴅɪᴏ ᴠᴏʟᴜᴍᴇ 🔄", callback_data="HV"
            )
        ],
        [
            InlineKeyboardButton(text="🔈 ʟᴏᴡ ᴠᴏʟ", callback_data="LV"),
            InlineKeyboardButton(text="🔉 ᴍᴇᴅɪᴜᴍ ᴠᴏʟ", callback_data="MV"),
        ],
        [
            InlineKeyboardButton(text="🔊 ʜɪɢʜ ᴠᴏʟ", callback_data="HV"),
            InlineKeyboardButton(text="🔈 ᴀᴍᴘʟɪғɪᴇᴅ ᴠᴏʟ", callback_data="VAM"),
        ],
        [
            InlineKeyboardButton(
                text="🔽 ᴄᴜsᴛᴏᴍ ᴠᴏʟᴜᴍᴇ 🔽", callback_data="Custommarkup"
            )
        ],
        [InlineKeyboardButton(text="🔙 ʙᴀᴄᴋ", callback_data="settingm")],
        ]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MV":
        assis = {
            "volume": 50,
        }
        volume = 50
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        buttons = [
        [
            InlineKeyboardButton(
                text="🔄 ʀᴇsᴇᴛ ᴀᴜᴅɪᴏ ᴠᴏʟᴜᴍᴇ 🔄", callback_data="HV"
            )
        ],
        [
            InlineKeyboardButton(text="🔈 ʟᴏᴡ ᴠᴏʟ", callback_data="LV"),
            InlineKeyboardButton(text="🔉 ᴍᴇᴅɪᴜᴍ ᴠᴏʟ", callback_data="MV"),
        ],
        [
            InlineKeyboardButton(text="🔊 ʜɪɢʜ ᴠᴏʟ", callback_data="HV"),
            InlineKeyboardButton(text="🔈 ᴀᴍᴘʟɪғɪᴇᴅ ᴠᴏʟ", callback_data="VAM"),
        ],
        [
            InlineKeyboardButton(
                text="🔽 ᴄᴜsᴛᴏᴍ ᴠᴏʟᴜᴍᴇ 🔽", callback_data="Custommarkup"
            )
        ],
        [InlineKeyboardButton(text="🔙 ʙᴀᴄᴋ", callback_data="settingm")],
        ]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "HV":
        assis = {
            "volume": 100,
        }
        volume = 100
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        buttons = [
        [
            InlineKeyboardButton(
                text="🔄 ʀᴇsᴇᴛ ᴀᴜᴅɪᴏ ᴠᴏʟᴜᴍᴇ 🔄", callback_data="HV"
            )
        ],
        [
            InlineKeyboardButton(text="🔈 ʟᴏᴡ ᴠᴏʟ", callback_data="LV"),
            InlineKeyboardButton(text="🔉 ᴍᴇᴅɪᴜᴍ ᴠᴏʟ", callback_data="MV"),
        ],
        [
            InlineKeyboardButton(text="🔊 ʜɪɢʜ ᴠᴏʟ", callback_data="HV"),
            InlineKeyboardButton(text="🔈 ᴀᴍᴘʟɪғɪᴇᴅ ᴠᴏʟ", callback_data="VAM"),
        ],
        [
            InlineKeyboardButton(
                text="🔽 ᴄᴜsᴛᴏᴍ ᴠᴏʟᴜᴍᴇ 🔽", callback_data="Custommarkup"
            )
        ],
        [InlineKeyboardButton(text="🔙 ʙᴀᴄᴋ", callback_data="settingm")],
        ]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "VAM":
        assis = {
            "volume": 200,
        }
        volume = 200
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        buttons = [
        [
            InlineKeyboardButton(
                text="🔄 ʀᴇsᴇᴛ ᴀᴜᴅɪᴏ ᴠᴏʟᴜᴍᴇ 🔄", callback_data="HV"
            )
        ],
        [
            InlineKeyboardButton(text="🔈 ʟᴏᴡ ᴠᴏʟ", callback_data="LV"),
            InlineKeyboardButton(text="🔉 ᴍᴇᴅɪᴜᴍ ᴠᴏʟ", callback_data="MV"),
        ],
        [
            InlineKeyboardButton(text="🔊 ʜɪɢʜ ᴠᴏʟ", callback_data="HV"),
            InlineKeyboardButton(text="🔈 ᴀᴍᴘʟɪғɪᴇᴅ ᴠᴏʟ", callback_data="VAM"),
        ],
        [
            InlineKeyboardButton(
                text="🔽 ᴄᴜsᴛᴏᴍ ᴠᴏʟᴜᴍᴇ 🔽", callback_data="Custommarkup"
            )
        ],
        [InlineKeyboardButton(text="🔙 ʙᴀᴄᴋ", callback_data="settingm")],
        ]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTEN":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        buttons = [
        [
            InlineKeyboardButton(text="+10", callback_data="PTEN"),
            InlineKeyboardButton(text="-10", callback_data="MTEN"),
        ],
        [
            InlineKeyboardButton(text="+25", callback_data="PTF"),
            InlineKeyboardButton(text="-25", callback_data="MTF"),
        ],
        [
            InlineKeyboardButton(text="+50", callback_data="PFZ"),
            InlineKeyboardButton(text="-50", callback_data="MFZ"),
        ],
        [InlineKeyboardButton(text="🔼 ᴄᴜsᴛᴏᴍ ᴠᴏʟᴜᴍᴇ 🔼", callback_data="AV")],
        ]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTEN":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        buttons = [
        [
            InlineKeyboardButton(text="+10", callback_data="PTEN"),
            InlineKeyboardButton(text="-10", callback_data="MTEN"),
        ],
        [
            InlineKeyboardButton(text="+25", callback_data="PTF"),
            InlineKeyboardButton(text="-25", callback_data="MTF"),
        ],
        [
            InlineKeyboardButton(text="+50", callback_data="PFZ"),
            InlineKeyboardButton(text="-50", callback_data="MFZ"),
        ],
        [InlineKeyboardButton(text="🔼 ᴄᴜsᴛᴏᴍ ᴠᴏʟᴜᴍᴇ 🔼", callback_data="AV")],
        ]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTF":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        buttons = [
        [
            InlineKeyboardButton(text="+10", callback_data="PTEN"),
            InlineKeyboardButton(text="-10", callback_data="MTEN"),
        ],
        [
            InlineKeyboardButton(text="+25", callback_data="PTF"),
            InlineKeyboardButton(text="-25", callback_data="MTF"),
        ],
        [
            InlineKeyboardButton(text="+50", callback_data="PFZ"),
            InlineKeyboardButton(text="-50", callback_data="MFZ"),
        ],
        [InlineKeyboardButton(text="🔼 ᴄᴜsᴛᴏᴍ ᴠᴏʟᴜᴍᴇ 🔼", callback_data="AV")],
       ]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTF":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        buttons = [
        [
            InlineKeyboardButton(text="+10", callback_data="PTEN"),
            InlineKeyboardButton(text="-10", callback_data="MTEN"),
        ],
        [
            InlineKeyboardButton(text="+25", callback_data="PTF"),
            InlineKeyboardButton(text="-25", callback_data="MTF"),
        ],
        [
            InlineKeyboardButton(text="+50", callback_data="PFZ"),
            InlineKeyboardButton(text="-50", callback_data="MFZ"),
        ],
        [InlineKeyboardButton(text="🔼 ᴄᴜsᴛᴏᴍ ᴠᴏʟᴜᴍᴇ 🔼", callback_data="AV")],
       ]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PFZ":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        buttons = [
        [
            InlineKeyboardButton(text="+10", callback_data="PTEN"),
            InlineKeyboardButton(text="-10", callback_data="MTEN"),
        ],
        [
            InlineKeyboardButton(text="+25", callback_data="PTF"),
            InlineKeyboardButton(text="-25", callback_data="MTF"),
        ],
        [
            InlineKeyboardButton(text="+50", callback_data="PFZ"),
            InlineKeyboardButton(text="-50", callback_data="MFZ"),
        ],
        [InlineKeyboardButton(text="🔼 ᴄᴜsᴛᴏᴍ ᴠᴏʟᴜᴍᴇ 🔼", callback_data="AV")],
        ]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MFZ":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_assistant(c_id, "assistant", assis)
        buttons = [
        [
            InlineKeyboardButton(text="+10", callback_data="PTEN"),
            InlineKeyboardButton(text="-10", callback_data="MTEN"),
        ],
        [
            InlineKeyboardButton(text="+25", callback_data="PTF"),
            InlineKeyboardButton(text="-25", callback_data="MTF"),
        ],
        [
            InlineKeyboardButton(text="+50", callback_data="PFZ"),
            InlineKeyboardButton(text="-50", callback_data="MFZ"),
        ],
        [InlineKeyboardButton(text="🔼 ᴄᴜsᴛᴏᴍ ᴠᴏʟᴜᴍᴇ 🔼", callback_data="AV")],
        ]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "USERLIST":
        await CallbackQuery.answer("Auth Users!")
        buttons = [
        [
            InlineKeyboardButton(text="👥 ᴇᴠʀʏᴏɴᴇ", callback_data="EVE"),
            InlineKeyboardButton(text="🙍 ᴀᴅᴍɪɴs", callback_data="AMS"),
        ],
        [
            InlineKeyboardButton(
                text="📋 ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ ʟɪsᴛ", callback_data="USERLIST"
            )
        ],
        [InlineKeyboardButton(text="🔙 ʙᴀᴄᴋ", callback_data="settingm")],
       ]
        _playlist = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _playlist:
            return await CallbackQuery.edit_message_text(
                text=f"{text}\n\nNo Authorized Users Found\n\nYou can allow any non-admin to use my admin commands by /auth and delete by using /unauth",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            j = 0
            await CallbackQuery.edit_message_text(
                "Fetching Authorised Users... Please Wait"
            )
            msg = f"**Authorised Users List[AUL]:**\n\n"
            for note in _playlist:
                _note = await get_authuser(
                    CallbackQuery.message.chat.id, note
                )
                user_id = _note["auth_user_id"]
                user_name = _note["auth_name"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name
                    j += 1
                except Exception:
                    continue
                msg += f"{j}➤ {user}[`{user_id}`]\n"
                msg += f"    ┗ Added By:- {admin_name}[`{admin_id}`]\n\n"
            await CallbackQuery.edit_message_text(
                msg, reply_markup=InlineKeyboardMarkup(buttons)
            )
    if command == "UPT":
        bot_uptimee = int(time.time() - bot_start_time)
        Uptimeee = f"{get_readable_time((bot_uptimee))}"
        await CallbackQuery.answer(
            f"Bot's Uptime: {Uptimeee}", show_alert=True
        )
    if command == "CPT":
        cpue = psutil.cpu_percent(interval=0.5)
        await CallbackQuery.answer(
            f"Bot's Cpu Usage: {cpue}%", show_alert=True
        )
    if command == "RAT":
        meme = psutil.virtual_memory().percent
        await CallbackQuery.answer(
            f"Bot's Memory Usage: {meme}%", show_alert=True
        )
    if command == "DIT":
        diske = psutil.disk_usage("/").percent
        await CallbackQuery.answer(
            f"Disk Usage: {diske}%", show_alert=True
        )
