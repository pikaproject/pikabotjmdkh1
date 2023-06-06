from asyncio import sleep
from pymongo import MongoClient
from pyrogram import filters
from pyrogram.errors import FloodWait

from pyrogram.handlers import MessageHandler
from pyrogram.filters import command
from bot import bot, config_dict, LOGGER
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage

async def broadcast(bot, message):
    mess = message.text.split(maxsplit=1)
    if not config_dict['DATABASE_URL']:
        await sendMessage(f"DATABASE_URL not provided", message)
    else:
        a = await sendMessage(f"Broadcasting Your Message", bot, message)
        conn = MongoClient(config_dict['DATABASE_URL'])
        db = conn['mltb']
        users_collection = db['users.5692262279']
        users_count = users_collection.count_documents({})

        chat_ids = [str(user["_id"]) for user in users_collection.find({}, {"_id": 1})]
        auth = [str(user["is_auth"]) for user in users_collection.find({}, {"is_auth": 1})]
        success = 0
        for chat_id in chat_ids:
            try:
               await message.copy(chat_id=chat_id) #from_chat_id=message.chat.id, message_id=message.id)
            except Exception as e:
               LOGGER.error(e)
        success += 1
        msg = f"Broadcasting Completed\n"
        msg += f"Total {users_count} users in Database\n"
        msg += f"Sucess: {success} users\n"
        msg += f"Failed: {users_count - success} users"
        await sendMessage(msg, bot, message)
        #else:
        #   await editMessage(f"No message provided for broadcast", bot, a)

#if len(mess) > 1:
#           a = await sendMessage(f"Broadcasting Your Message", bot, message)
#          return
bot.add_handler(MessageHandler(broadcast, filters=command(BotCommands.Broadcast) & CustomFilters.sudo))
