from pymongo import MongoClient

from bot import bot, LOGGER, config_dict
from bot.helper.telegram_helper.filters import CustomFilters
from pyrogram.filters import command
from pyrogram.handlers import MessageHandler
from bot.helper.telegram_helper.bot_commands import BotCommands

async def sendMessage(client, chat_id, text):
    try:
        await client.send_message(chat_id=chat_id, text=text, disable_web_page_preview=True)
    except Exception as e:
        LOGGER.error(str(e))
        
async def broadcast(client, message):
    print("Broadcast function called")
    reply_to = message.reply_to_message
    print("Reply message:", reply_to)

    # ...
    
    for chat_id in chat_ids:
        print("Processing chat ID:", chat_id)
        try:
        except Exception as err:
            LOGGER.error(err)
    
    # ...

bot.add_handler(MessageHandler(broadcast, filters=command(
    BotCommands.Broadcast) & CustomFilters.sudo))
