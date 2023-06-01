from pymongo import MongoClient
from pyrogram import filters
from pyrogram.types import Message

from pyrogram.handlers import MessageHandler
from pyrogram.filters import command
from bot import bot, config_dict, LOGGER
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage


async def broadcast_handler(bot : Client, message: Message):
    replied = message.reply_to_message

    if not config_dict['DATABASE_URL']:
        await sendMessage(bot, message.chat.id, text="DATABASE_URL not provided")
    else:
        conn = MongoClient(config_dict['DATABASE_URL'])
        db = conn['mltb']
        users_collection = db['users.5692262279']
        users_count = users_collection.count_documents({})

        chat_ids = [str(user["_id"]) for user in users_collection.find({}, {"_id": 1})]
        success = 0

        for chat_id in chat_ids:
            try:
                await bot.copy_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.id)
                success += 1
            except Exception as err:
                LOGGER.error(err)

        msg = f"Broadcasting Completed\n"
        msg += f"Total {users_count} users in Database\n"
        msg += f"Success: {success} users\n"
        msg += f"Failed: {users_count - success} users"
        await sendMessage(bot, message.chat.id, msg)


async def broadcast_command_handler(_, message: Message):
    await broadcast_handler(bot, message)

bot.add_handler(MessageHandler(broadcast_command_handler, filters=command(BotCommands.Broadcast) & CustomFilters.sudo))
