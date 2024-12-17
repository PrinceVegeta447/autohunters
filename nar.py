import asyncio
from telethon import TelegramClient, events
import random
from telethon.errors import MessageIdInvalidError

api_id = 8447214
api_hash = '9ec5782ddd935f7e2763e5e49a590c0d'

async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    print('''
                 _                ____ _______ 
                | |              / __ \\__   __|
  _ __ ___   ___| | ___  _ __   | |  | | | |   
 | '_ ` _ \\ / _ \\ |/ _ \\| '_ \\  | |  | | | |   
 | | | | | |  __/ | (_) | | | | | |__| | | |   
 |_| |_| |_|\\___|_|\\___/|_| |_|  \\___\\_\\ |_|   
                                               
                                               
                                               ''')

    @client.on(events.NewMessage(from_users=5416991774))
    async def _(event):
        if "challenged you !" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(0, 0)
            return

    @client.on(events.NewMessage(from_users=5416991774))
    async def _(event):
        if "HP" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(0, 0)
            return

    @client.on(events.MessageEdited(from_users=5416991774))
    async def _(event):
        if "HP" in event.raw_text:
            try:
                await asyncio.sleep(random.random() + 1)
                await event.click(0)
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

    @client.on(events.MessageEdited(from_users=5416991774))
    async def _(event):
        if "got defeated !" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(0, 0)
            return

    @client.on(events.NewMessage(from_users=5416991774))
    async def handle_message(event):
        if "Death's Gambit" in event.raw_text:
            async for message in client.iter_messages(event.chat_id, limit=1):
                if message.reply_markup and message.reply_markup.rows:
                    found_data = None
                    for row in message.reply_markup.rows:
                        for button in row.buttons:
                            if button.data and len(button.data) == 33:
                                found_data = button.data
                                break
                        if found_data:
                            break

                    if found_data:
                        await asyncio.sleep(random.random() + 1)
                        await event.click(data=found_data)

    @client.on(events.MessageEdited(from_users=5416991774))
    async def _(event):
        if any(keyword in event.raw_text for keyword in ["You have defeated"]):
            await asyncio.sleep(random.random() + 1)
            await event.client.send_message(5416991774, "/explore")

    @client.on(events.NewMessage(from_users=5416991774))
    async def _(event):
        if any(keyword in event.raw_text for keyword in ["has appeared !", "Your luck helped", "CROSS OVER ITEM"]):
            await asyncio.sleep(random.random() + 1)
            await event.client.send_message(5416991774, "/explore")

    # Integration for "Baka! Don't Spam"
    @client.on(events.NewMessage(from_users=5416991774))
    async def handle_spam_message(event):
        if "Baka! Don't Spam" in event.raw_text:
            await asyncio.sleep(10)  # Wait for 10 seconds
            await event.client.send_message(5416991774, "/explore")

    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())