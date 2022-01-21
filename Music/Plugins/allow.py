from Music import app, SUDOERS
from pyrogram import filters, Client
from pyrogram.types import Message
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.database.chats import (get_served_chats, is_served_chat, add_served_chat, get_served_chats, remove_served_chat)  

chat_watcher_group = 10


@app.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message):
    chat_id = message.chat.id

    if not chat_id:
        return

    await add_served_chat(chat_id)

@app.on_message(filters.command("allow") & filters.user(SUDOERS))
async def blacklist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Usage:**\n/allow [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if not await is_served_chat(chat_id):
        await add_served_chat(chat_id)
        await message.reply_text("ADDED CHAT TO ALLOWED LIST")
    else:
        await message.reply_text("ALREADY IN ALLOWED LIST")
    
@app.on_message(filters.command("disallow") & filters.user(SUDOERS))
async def whitelist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Usage:**\n/disallow [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if not await is_served_chat(chat_id):
        await message.reply_text("Chat not allowed.")
        return
    try:
        await remove_served_chat(chat_id)
        await message.reply_text("Chat diallowed.")
        return
    except Exception as e:
      await message.reply_text("Error.")


@app.on_message(filters.command("allowedchat") & filters.user(SUDOERS))
async def blacklisted_chats_func(_, message: Message):
    served_chats = []
    text = "**__Allowed Chats__**\n"
    try:
        chats = await get_served_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text("Error.")
        return
    count = 0
    for served_chat in served_chats:
        
        try:
            title = (await app.get_chat(served_chat)).title
        except Exception:
            title = "Private"
        count += 1
        text += f"**{count}. {title}** [`{served_chat}`]\n"
    if not text:
        await message.reply_text("🉐 No Allowed Chats")  
    else:
        await message.reply_text(text)
