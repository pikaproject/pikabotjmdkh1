from pymongo import MongoClient
from pyrogram import filters
from pyrogram.types import Message

from pyrogram.handlers import MessageHandler
from pyrogram.filters import command
from bot import bot, config_dict, LOGGER
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage


async def broadcast(client, message):

    if not config_dict['DATABASE_URL']:
        await client.send_message(chat_id=message.chat.id, text=f"DATABASE_URL not provided")
    else:
        conn = MongoClient(config_dict['DATABASE_URL'])
        db = conn['mltb']
        users_collection = db['users.5692262279']
        users_count = users_collection.count_documents({})

        chat_ids = [str(user["_id"]) for user in users_collection.find({}, {"_id": 1})]
        auth = [str(user["is_auth"]) for user in users_collection.find({}, {"is_auth": 1})]
        success = 0

        for chat_id in chat_ids:
            try:
                if auth = True
                   return await client.copy_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.id)
                    success += 1
                else:
                    await message.reply(text= "Error : Bot tidak berinteraksi Dengan User id atau chat Id Yang Gagal" )
            except Exception as err:
                LOGGER.error(err)

        msg = f"Broadcasting Completed\n"
        msg += f"Total {users_count} users in Database\n"
        msg += f"Sucess: {success} users\n"
        msg += f"Failed: {users_count - success} users"
        await message.reply(msg)

async def broadcast_psn(client, message):
    mess = message.text.split()
    #replied = message.reply_to_message.text
    #replied_text = replied.text.split(' ', 1)[1]
    if len(mess) > 1:
       message = " ".join([k for k in mess if k != "/broadcast"])
       await broadcast(client, message)
    #elif len(message) >replied := reply_to_message:
       #await broadcast(client, message)
    else:
       await message.reply(message, "Gunakan /broadcast Untuk Melakukan tugas ini")

bot.add_handler(MessageHandler(broadcast, filters=command(BotCommands.Broadcast) & CustomFilters.sudo))