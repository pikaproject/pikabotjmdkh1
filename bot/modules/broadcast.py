from pymongo import MongoClient

from bot import bot, LOGGER, config_dict
from bot.helper.telegram_helper.message_utils import sendMessage
from bot.helper.telegram_helper.filters import CustomFilters
from pyrogram.filters import command
from pyrogram.handlers import MessageHandler
from bot.helper.telegram_helper.bot_commands import BotCommands

async def broadcast(client, message):
    reply_to = message.reply_to_message

    if not config_dict['DATABASE_URL']:
        await client.send_message(chat_id=message.chat.id, text="DATABASE_URL not provided")
    else:
        conn = MongoClient(config_dict['DATABASE_URL'])
        db = conn.mltb
        users_collection = db.users
        users_count = db.users.count_documents({})  # Menghapus 'await' di sini

        chat_ids_cursor = users_collection.find({}, {"_id": 1})
        chat_ids = [str(user["_id"]) async for user in chat_ids_cursor]
        success = 0

        for chat_id in chat_ids:
            try:
                await client.copy_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=reply_to.message_id)
                success += 1
            except Exception as err:
                LOGGER.error(err)

        msg = f"<b>Broadcasting Completed</b>\n"
        msg += f"<b>Total {users_count} users in Database</b>\n"
        msg += f"<b>Success: </b>{success} users\n"
        msg += f"<b>Failed: </b>{users_count - success} users"
        await sendMessage(msg, client, message)

bot.add_handler(MessageHandler(broadcast, filters=command(BotCommands.Broadcast) & CustomFilters.sudo))
