import subprocess
import asyncio
import re
import random
from telethon import TelegramClient, events
from telethon.errors import MessageIdInvalidError
from collections import deque

api_id = '29848170'
api_hash = 'e2b1cafae7b2492c625e19db5ec7f513'
session = '"1BVtsOH8Bu4FVmqgUEOPlLr_eCNE1LLZG6HYP-byyEwqkhlgqEBSnKD-E5R4mxJolZHfOx-X0Lpgjr3ApU_a0E-q2kaz7wUErqCWCVJxU4ZsMYasvF63OJEn553RXpFIi0SMnmJS1XHCQthYKksRnNba_Of3eOzUEyM95ftNoqTurHv_Ft-M0_tgmmM7x9ZYKf6EfFGEwjbsIlmf7rjcDv6gsOHt9vlQiRWiGc48tXAT02QHAuYMOy-e6nSOPB40p4l3BO6GufwiSnOkCtVdkIbQq9zukLHPLHq18iNlpUI6-Khx87E3McikCNEBVeEn_36KSurj6k9Pm67qCHfo0fAaOL1VXjzA="'

clicked_4th_button = False

last_two_messages = deque(maxlen=2)

client = TelegramClient('your_session_file.session', api_id, api_hash)

legendary_poks = ["Zapdos", "Mewtwo", "Lugia", "Ho-Oh", "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys", "Dialga", "Palkia", "Regigigas", "Giratina", "Shaymin", "Arceus", "Victini", "Cobalion", "Terrakion", "Virizion", "Reshiram", "Zekrom", "Landorus", "Kyurem", "Keldeo", "Genesect", "Xerneas", "Yveltal", "Zygarde", "Diancie", "Hoopa", "Cosmog", "Cosmoem", "Buzzwole", "Pheromosa", "Kartana", "Necrozma", "Magearna", "Marshadow", "Blacephalon", "Zeraora", "Zacian", "Zamazenta", "Eternatus", "Kubfu", "Spectrier", "Glastrier", "Regieleki", "Aerodactyl", "Lopunny", "Charizard", "Gallade", "Manectric", "Sceptile", "Salamence", "Pidgeot", "Venusaur", "Blastoise", "Beedrill", "Alakazam", "Gyarados", "Lopunny", "Audino", "Abomasnow", "Steelix", "Ampharos","Lucario"]

regular_ball = ["Darumaka", "Darmanitan", "Wishiwashi", "Drakloak", "Duraludon", "Rotom", "Tentacruel", "Snorlax", "Overqwil", "Munchlax", "Kleavor", "Fennekin", "Delphox", "Dunsparce", "Braixen", "Axew", "Fraxure", "Haxorus", "Floette", "Flabebe", "Rufflet", "Porygon", "Porygon2", "Mankey", "Primeape", "Dratini", "Shellder", "Gible", "Gabite", "Dragonair", "Golett", "Goomy", "Greninja", "Vikavolt", "Vullaby", "Litwick", "Lampent", "Wimpod", "Buneary", "Ursaring", "Teddiursa", "Hawlucha", "Abra", "Kadabra", "Turtonator", "Jolteon", "Dwebble", "Crustle", "Starly", "Stantler", "Rhyhorn", "Staryu", "Starmie", "Tauros", "Lapras", "Vaporeon", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Espeon", "Slakoth", "Vigoroth", "Lotad", "Lombre", "Ludicolo", "Treecko", "Grovyle", "Electrike", "Manectric", "Growlithe", "Monferno", "Piplup", "Prinplup", "Chimchar", "Sirfetch'd", "Staravia", "Bagon", "Shelgon", "Salamence", "Tepig", "Pignite", "Spiritomb", "Togekiss", "Skorupi", "Drilbur", "Timburr", "Gurdurr", "Scraggy", "Scrafty", "Yamask", "Cofagrigus", "Ducklett", "Swanna", "Zorua", "Zoroark", "Cinccino", "Frillish", "Jellicent", "Karrablast", "Escavalier", "Ferroseed", "Mienfoo", "Mienshao", "Cryogonal", "Shelmet", "Accelgor", "Helioptile", "Heliolisk", "Tyrunt", "Tyrantrum", "Sylveon", "Litleo", "Pyroar", "Chespin", "Quilladin", "Chesnaught", "Durant", "Deino", "Phantump", "Trevenant", "Pumpkaboo", "Gourgeist", "Popplio", "Brionne", "Litten", "Torracat", "Rowlet", "Dartrix", "Grookey", "Thwackey", "Rillaboom", "Scorbunny", "Raboot", "Orbeetle", "Rookidee", "Corvisquire", "Sobble", "Drizzile", "Inteleon", "Dracozolt", "Dracovish", "Morpeko", "Sneasler", "Toxapex", "Mareanie", "Volcarona", "Tentacool", "Larvesta", "Charmeleon", "Charmander", "Togetic", "Togepi", "Druddigon", "Dhelmise","Runerigus", "Lucario", "Unfezant", "Tranquill", "Pidove", "Barraskewda", "Arrokuda", "Zubat", "Golbat", "Gastly", "Haunter", "Clauncher", "Clawitzer", "Froslass", "Cutiefly", "Ribombee"]

repeat_ball = legendary_poks
cooldown = random.randint(1, 2)
low_lvl = False

@client.on(events.NewMessage(from_users=572621020))
async def dailyLimit(event):
    if "Daily hunt limit reached" in event.raw_text:
        await client.disconnect()
        
pokemon_caught = False  # Flag to track if a Pokémon is caught
@client.on(events.NewMessage(from_users=572621020))
async def hunt_or_pass(event):
    if "✨ Shiny Pokémon found!" in event.raw_text:
        await event.client.send_message(-1002235680545, "@Mr_animosity @Xander_sama 4mar shiny aaya Whatsapp kar")
        await client.disconnect()
    elif "A wild" in event.raw_text:
        global cooldown
        global pokemon_caught
        pok_name = event.raw_text.split("wild ")[1].split(" (")[0]
        print(pok_name)
        if pok_name in regular_ball or pok_name in repeat_ball:
            await asyncio.sleep(cooldown)
            try:
                await event.click(0, 0)
            except MessageIdInvalidError:
                print(f"Failed to click the button for {pok_name}")
        else:
            await asyncio.sleep(cooldown)
            await client.send_message(572621020, '/hunt')

@client.on(events.NewMessage(from_users=572621020))
async def battlefirst(event):
    global low_lvl
    global cooldown
    if "Battle begins!" in event.raw_text:
        wild_pokemon_name_match = re.search(r"Wild (\w+) \[.*\]\nLv\. \d+  •  HP \d+/\d+", event.raw_text)
        if wild_pokemon_name_match:
            pok_name = wild_pokemon_name_match.group(1)
            wild_pokemon_hp_match = re.search(r"Wild .* \[.*\]\nLv\. \d+  •  HP (\d+)/(\d+)", event.raw_text)
            if wild_pokemon_hp_match:
                wild_max_hp = int(wild_pokemon_hp_match.group(2))
                if wild_max_hp <= 50:
                    low_lvl = True
                    print("low lvl set to true")
                    await asyncio.sleep(cooldown)
                    try:
                        await event.click(text="Poke Balls")
                        print("clicked on btn poke balls")
                    except MessageIdInvalidError:
                        print("Failed to click Poke Balls")
                else:
                    await asyncio.sleep(2)
                    try:
                        await event.click(0, 0)
                    except MessageIdInvalidError:
                        print("Failed to click the button for high-level Pokemon")

def calculate_health_percentage(max_hp, current_hp):
    if max_hp <= 0:
        raise ValueError("Total health must be greater than zero.")
    if current_hp < 0 or current_hp > max_hp:
        raise ValueError("Current health must be between 0 and the total health.")
    health_percentage = round((current_hp / max_hp) * 100)
    return health_percentage

@client.on(events.MessageEdited(from_users=572621020))
async def battle(event):
    global low_lvl
    if "Wild" in event.raw_text:
        wild_pokemon_name_match = re.search(r"Wild (\w+) \[.*\]\nLv\. \d+  •  HP \d+/\d+", event.raw_text)
        if wild_pokemon_name_match:
            pok_name = wild_pokemon_name_match.group(1)
            wild_pokemon_hp_match = re.search(r"Wild .* \[.*\]\nLv\. \d+  •  HP (\d+)/(\d+)", event.raw_text)
            if wild_pokemon_hp_match:
                wild_max_hp = int(wild_pokemon_hp_match.group(2))
                wild_current_hp = int(wild_pokemon_hp_match.group(1))
                wild_health_percentage = calculate_health_percentage(wild_max_hp, wild_current_hp)
                if low_lvl:
                    await asyncio.sleep(cooldown)
                    try:
                        await event.click(text="Poke Balls")
                        if pok_name in regular_ball:
                            await asyncio.sleep(1)
                            await event.click(text="Regular")
                        elif pok_name in repeat_ball:
                            await asyncio.sleep(1)
                            await event.click(text="Repeat")
                    except MessageIdInvalidError:
                        print(f"Failed to click Poke Balls for {pok_name}")
                elif wild_health_percentage > 50:
                    await asyncio.sleep(1)
                    try:
                        await event.click(0, 0)
                    except MessageIdInvalidError:
                        print(f"Failed to click the button for {pok_name} with high health")
                elif wild_health_percentage <= 50:
                    await asyncio.sleep(1)
                    try:
                        await event.click(text="Poke Balls")
                        if pok_name in regular_ball:
                            await asyncio.sleep(1)
                            await event.click(text="Regular")
                        elif pok_name in repeat_ball:
                            await asyncio.sleep(1)
                            await event.click(text="Repeat")
                    except MessageIdInvalidError:
                        print(f"Failed to click Poke Balls for {pok_name} with low health")
                print(f"{pok_name} health percentage: {wild_health_percentage}%")
            else:
                print(f"Wild Pokemon {pok_name} HP not found in the battle description.")
        else:
            print("Wild Pokemon name not found in the battle description.")

@client.on(events.MessageEdited(from_users=572621020))
async def skip(event):
    if any(substring in event.raw_text for substring in ["fled", "💵", "You caught"]):
        global cooldown
        global low_lvl
        global pokemon_caught 
        low_lvl = False
        await asyncio.sleep(cooldown)
        await client.send_message(572621020, '/hunt')

@client.on(events.NewMessage(from_users=572621020))
async def skipTrainer(event):
    if "An expert trainer" in event.raw_text:
        global cooldown
        await asyncio.sleep(cooldown)
        await client.send_message(572621020, '/hunt')

@client.on(events.MessageEdited(from_users=572621020))
async def pokeSwitch(event):
    if "Choose your next pokemon." in event.raw_text:
        buttons_to_click = ["Sceptile","Snorlax","Sliggoo","Scizor","Solgaleo"]
        for button in buttons_to_click:
            try:
                await event.click(text=button)
            except MessageIdInvalidError:
                print(f"Failed to click button {button}")
# Global variable to track bot status
bot_running = False

# Replace with your Telegram user ID(s)
AUTHORIZED_USERS = [1710597756]  # Add your Telegram ID(s) here
# Global variable to store the last message ID
last_message_id = None

@client.on(events.NewMessage)
async def command_handler(event):
    global bot_running, cooldown, last_message_id

    # Restrict commands to authorized users
    if event.sender_id not in AUTHORIZED_USERS:
        return

    # Extract command
    command = event.text.strip().lower()

    # Handle commands
    if command == ".stop":
        if bot_running:
            bot_running = False
            await event.reply("Bot has been stopped. Use .start to run it again.")
        else:
            await event.reply("Bot is already stopped.")
    elif command == ".start":
        if not bot_running:
            bot_running = True
            await edit_message(event, "Bot has been started. Resuming operations.")
        else:
            await edit_message(event, "Bot is already running.")
    elif command.startswith(".set_cooldown"):
        try:
            cooldown = int(command.split(" ")[1])
            await edit_message(event, f"Cooldown updated to {cooldown} seconds.")
        except (IndexError, ValueError):
            await edit_message(event, "Invalid usage. Example: .set_cooldown 2")
    elif command == ".status":
        status = "running" if bot_running else "stopped"
        await edit_message(event, f"The bot is currently {status}. Cooldown: {cooldown} seconds.")


async def edit_message(event, new_text):
    global last_message_id

    # If no message has been sent yet, send a new one
    if last_message_id is None:
        message = await event.reply(new_text)
        last_message_id = message.id
    else:
        # Try to edit the existing message
        try:
            await client.edit_message(event.chat_id, last_message_id, new_text)
        except Exception as e:
            print(f"Failed to edit message: {e}")
            # If editing fails, send a new message
            message = await event.reply(new_text)
            last_message_id = message.id



    # Skip processing if the bot is stopped
    if not bot_running:
        return

                          
client.start()
client.run_until_disconnected()