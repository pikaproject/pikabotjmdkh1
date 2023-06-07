from asyncio import sleep
from pymongo import MongoClient
from pyrogram import filters
from pyrogram.errors import FloodWait

from pyrogram.handlers import MessageHandler
from pyrogram.filters import command
from bot import bot, config_dict, LOGGER, user_data
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage


async def broadcast(bot, message):
    mess = message.text
    #if (reply_to := message.reply_to_message) and len(mess) == 0:
    elif len(mess) > 1 :
        mess = mess.split(maxsplit=1)[1]
        success = 0
        totals = len(user_data)
        for chat_id in user_data:
            reply_to=message.reply_to_message
            try:
                await bot.send_message(chat_id=chat_id, text= mess) #from_chat_id=message.chat.id, message_id=message.id)
            except Exception as e:
               LOGGER.error(e)
               continue
        success += 1
        msg = f"Broadcasting Completed\n"
        msg += f"Total {totals} users in Database\n"
        msg += f"Sucess: {success} users\n"
        msg += f"Failed: {totals - success} users"
        await message.reply(msg, message)
    else:
        await sendMessage("Silahkan Masukkan Pesann yang akan di Broadcast", message)
bot.add_handler(MessageHandler(broadcast, filters=command(BotCommands.Broadcast) & CustomFilters.sudo))
