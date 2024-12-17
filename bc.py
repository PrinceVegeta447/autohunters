import subprocess
import asyncio
import re
import random
from telethon import TelegramClient, events
from telethon.errors import MessageIdInvalidError
from collections import deque
import logging
logging.basicConfig(level=logging.INFO)

api_id = '1747534' # Keep this as it is 
api_hash = '5a2684512006853f2e48aca9652d83ea' # same heree
session = '"1BVtsOH8Bu4FVmqgUEOPlLr_eCNE1LLZG6HYP-byyEwqkhlgqEBSnKD-E5R4mxJolZHfOx-X0Lpgjr3ApU_a0E-q2kaz7wUErqCWCVJxU4ZsMYasvF63OJEn553RXpFIi0SMnmJS1XHCQthYKksRnNba_Of3eOzUEyM95ftNoqTurHv_Ft-M0_tgmmM7x9ZYKf6EfFGEwjbsIlmf7rjcDv6gsOHt9vlQiRWiGc48tXAT02QHAuYMOy-e6nSOPB40p4l3BO6GufwiSnOkCtVdkIbQq9zukLHPLHq18iNlpUI6-Khx87E3McikCNEBVeEn_36KSurj6k9Pm67qCHfo0fAaOL1VXjzA="'

client = TelegramClient('your_session_file.session', api_id, api_hash)

pd = 0
bt = 0
def main():
    @client.on(events.NewMessage(func=lambda e: e.is_private, pattern=r'/give 45'))
    async def give_handler(event):
        user_id =-1002381740109
        await event.reply('/challenge')  
    @client.on(events.MessageEdited(from_users=572621020))
    async def _(event):
        if "Choose your next pokemon." in event.raw_text:
            if event.buttons:
                await asyncio.sleep(0)
                await event.click(1, 1)
                await event.click(2, 0)
                await event.click(2, 1)
                await event.click(3, 0)
                await event.click(3, 1)
                await event.click(4, 0)
                await event.click(4, 1)
            return
    @client.on(events.NewMessage(outgoing=True, pattern='.db_battle'))
    async def _(event):
        await event.edit('''\nData For Auto Battle\nTotal Battles : '''+ str(bt)+'''\nTotal Pd : '''+str(pd))
    


    @client.on(events.NewMessage(from_users=572621020))
    async def _(event):
        if "has challenged" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(0, 0)
                global bt
                bt+=1
            return

    @client.on(events.NewMessage(from_users=572621020))
    async def _(event):
        if "Battle begins!" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(0, 0)
                #await message.click(row, column) ye hoga yaad rkahna hai
            return

    @client.on(events.MessageEdited(from_users=572621020))
    async def _(event):
        if "Battle begins!" in event.raw_text:
            try:
                await asyncio.sleep(random.random() + 1)
                await event.click(0)
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

  
            
         

    
    
                
        
    @client.on(events.MessageEdited(from_users=572621020))
    async def _(event):
        if "Current turn:" in event.raw_text:
            if event.buttons:
                await asyncio.sleep(random.random() + 1)
                await event.click(0, 0)
            return
    @client.on(events.MessageEdited(from_users=572621020))
    async def _(event):
        if "Current turn:" in event.raw_text:
            try:
                await asyncio.sleep(random.random() + 1)
                await event.click(0)
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

    client.start()
    client.run_until_disconnected()

main()