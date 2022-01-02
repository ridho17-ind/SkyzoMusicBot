from Music import app, SUDOERS, BOT_ID
from pyrogram import filters, Client
from sys import version as pyver
from pyrogram import __version__ as pyrover
from pytgcalls import (__version__ as pytover)
from pyrogram.types import Message
import platform, socket, re, uuid, json, psutil, logging
from Music.MusicUtilities.database.gbanned import get_gbans_count
from Music.MusicUtilities.database.chats import get_served_chats
from Music.MusicUtilities.database.sudo import (get_sudoers, get_sudoers, remove_sudo)
from Music.MusicUtilities.database.playlist import get_playlist_count
from Music.MusicUtilities.helpers.time import get_readable_time
from Music import app, SUDOERS, Music_START_TIME
import os 
import time
from pymongo import MongoClient
from Music.config import MONGO_DB_URI as smex

@app.on_message(filters.command("statsmusic") & ~filters.edited)
async def gstats(_, message):
    m = await message.reply_text("**Getting Stats**\n\nPlease wait for some time..")
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    blocked = await get_gbans_count()
    sudoers = await get_sudoers()
    j = 0
    for count, user_id in enumerate(sudoers, 0):
        try:                     
            user = await app.get_users(user_id)
            j += 1
        except Exception:
            continue                     
    modules_count ="17"
    sc = platform.system()
    arch = platform.machine()
    ram = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    bot_uptime = int(time.time() - Music_START_TIME)
    uptime = f"{get_readable_time((bot_uptime))}"
    hdd = psutil.disk_usage('/')
    total = (hdd.total / (1024.0 ** 3))
    total = str(total)
    used = (hdd.used / (1024.0 ** 3))
    used = str(used)
    free = (hdd.free / (1024.0 ** 3))
    free = str(free)
    msg = f"""
**Global Stats Of Music Bot**:\n\n
[•]<u>__**System Stats**__</u>
**Music Uptime:** {uptime}
**System Process:** Online
**Platform:** {sc}
**Storage:** Used {used[:4]} GiB out of {total[:4]} GiB, free {free[:4]} GiB
**Architecture:** {arch}
**Ram:** {ram}
**Python Version:** {pyver.split()[0]}
**Pyrogram Version:** {pyrover}
**PyTgCalls Version:** {pytover.__version__}

[•]<u>__**Bot Music Stats**__</u>
**Modules Loaded:** {modules_count}
**GBanned Users:** {blocked}
**Sudo Users:** {j}
**Allowed Chats:** {len(served_chats)}

"""
    served_chats.pop(0)
    await m.edit(msg, disable_web_page_preview=True)
