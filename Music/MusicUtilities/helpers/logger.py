# Skyzo Music Bot
# By Kenkan 

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Music.config import LOG_GROUP_ID
from Music import app


async def LOG_CHAT(message, what):
    if message.chat.username:
        chatusername = (f"@{message.chat.username}")
    else:
        chatusername = ("Private Group")
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = "["+user_name+"](tg://user?id="+str(user_id)+")" 
    logger_text = f"""
__**New {what}**__

**Chat:** {message.chat.title} [`{message.chat.id}`]
**User:** {mention}
**Username:** @{message.from_user.username}
**User ID:** `{message.from_user.id}`
**Chat Link:** {chatusername}
**Query:** {message.text}"""
    await app.send_message(LOG_GROUP_ID, 
               text = f"{logger_text}", 
               keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="ᴠɪᴇᴡs​​", url=f"t.me/c/{message.chat.id}")]]),
               disable_web_page_preview=True,
          )
    
