from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message

from bot import bot, config_dict, LOGGER
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage

@Client.on_message(filters.command(['broadcast']) & CustomFilters.owner_filter)
async def broadcast(client: Client, message: Message):
    reply_to = message.reply_to_message

    if not config_dict['DATABASE_URL']:
        await client.send_message(chat_id=message.chat.id, text=f"DATABASE_URL not provided")
    else:
        conn = MongoClient(config_dict['DATABASE_URL'])
        db = conn['mltb']
        users_collection = db['users.5692262279']
        users_count = users_collection.count_documents({})

        chat_ids = [str(user["_id"]) for user in users_collection.find({}, {"_id": 1})]
        success = 0

        for chat_id in chat_ids:
            try:
                await client.copy_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=reply_to.message_id)
                success += 1
            except Exception as err:
                LOGGER.error(err)

        msg = f"<b>Broadcasting Completed</b>\n"
        msg += f"<b>Total {users_count} users in Database</b>\n"
        msg += f"<b>Sucess: </b>{success} users\n"
        msg += f"<b>Failed: </b>{users_count - success} users"
        await sendMessage(msg, client, message)



