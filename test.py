import asyncio
from telethon import TelegramClient, events
import random
from telethon.errors import MessageIdInvalidError
from PIL import Image
from io import BytesIO


api_id = 8447214
api_hash = '9ec5782ddd935f7e2763e5e49a590c0d'

# Global delay for sending /explore command
EXPLORE_DELAY = 5  # Set the delay in seconds

API_KEY = '2cc06e099a30749dd146b35d66aa443a'

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
            await asyncio.sleep(EXPLORE_DELAY)  # Global delay applied
            await event.client.send_message(5416991774, "/explore")

    @client.on(events.NewMessage(from_users=5416991774))
    async def _(event):
        if any(keyword in event.raw_text for keyword in ["has appeared !", "Your luck helped", "CROSS OVER ITEM"]):
            await asyncio.sleep(EXPLORE_DELAY)  # Global delay applied
            await event.client.send_message(5416991774, "/explore")

    # Integration for "Baka! Don't Spam"
    @client.on(events.NewMessage(from_users=5416991774))
    async def handle_spam_message(event):
        if "Baka! Don't Spam" in event.raw_text:
            await asyncio.sleep(10)  # Specific delay for spam message
            await event.client.send_message(5416991774, "/explore")

    # Integration for "CAPTCHA HERE ! BE CAREFUL"
    @client.on(events.NewMessage(from_users=5416991774))
    async def handle_captcha_message(event):
        if "CAPTCHA HERE ! BE CAREFUL" in event.raw_text:
            mention_username = "@VegetaKunAlt"  # Replace with the target user's username
            chat_id = -1002235680545 # Use the current chat where the message was detected
            await event.client.send_message(chat_id, f"CAPTCHA detected! {mention_username}, please solve it.")
            
    @client.on(events.NewMessage(from_users=5416991774))
    async def handle_captcha_message(event):
        if "CAPTCHA HERE ! BE CAREFUL" in event.raw_text and event.media:
            # Download CAPTCHA image
            captcha_file = await event.download_media()

            # Send the CAPTCHA image to 2Captcha
            with open(captcha_file, 'rb') as image_file:
                response = requests.post(
                    "https://2captcha.com/in.php",
                    files={"file": image_file},
                    data={"key": API_KEY, "method": "post"}
                )
                if response.ok and "OK|" in response.text:
                    captcha_id = response.text.split('|')[1]
                    print(f"Submitted CAPTCHA to 2Captcha: {captcha_id}")
                    
                    # Wait for the CAPTCHA to be solved
                    while True:
                        result = requests.get(
                            f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}"
                        )
                        if result.ok and "OK|" in result.text:
                            captcha_text = result.text.split('|')[1]
                            print(f"CAPTCHA solved: {captcha_text}")
                            await event.reply(f"Solved CAPTCHA: {captcha_text}")
                            break
                        elif "CAPCHA_NOT_READY" in result.text:
                            await asyncio.sleep(5)  # Wait a bit and check again
                        else:
                            print(f"Error solving CAPTCHA: {result.text}")
                            break

    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())