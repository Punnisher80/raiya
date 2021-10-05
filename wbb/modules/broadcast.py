import os
import asyncio
from presets import Presets
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from wbb.utils.support import users_info
from wbb import SUDOERS, app
from wbb.utils.dbfunctions import add_user, query_msg

# ------------------------------- View Subscribers --------------------------------- #
@app.on_message(filters.private & filters.command('subscribers'))
async def subscribers_count(bot, m: Message):
    id = m.from_user.id
    if id not in SUDOERS:
        return
    msg = await m.reply_text(Presets.WAIT_MSG)
    messages = await users_info(bot)
    active = messages[0]
    blocked = messages[1]
    await m.delete()
    await msg.edit(Presets.USERS_LIST.format(active, blocked))

@app.on_message(filters.private & filters.command('send'))
async def send_text(bot, m: Message):
    id = m.from_user.id
    if id not in Config.AUTH_USERS:
        return
    if (" " not in m.text) and ("send" in m.text) and (m.reply_to_message is not None):
        query = await query_msg()
        for row in query:
            chat_id = int(row[0])
            try:
                await bot.copy_message(
                    chat_id=chat_id,
                    from_chat_id=m.chat.id,
                    message_id=m.reply_to_message.message_id,
                    caption=m.caption,
                    reply_markup=m.reply_markup
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except Exception:
                pass
    else:
        msg = await m.reply_text(Presets.REPLY_ERROR, m.message_id)
        await asyncio.sleep(8)
        await msg.delete()
