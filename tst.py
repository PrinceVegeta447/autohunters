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


LOG_CHANNEL_ID = -1002366595362

POKEMON_CATEGORIES = {
    "legendary": ["Zapdos", "Mewtwo", "Lugia", "Ho-Oh", "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys", "Dialga", "Palkia", "Regigigas", "Giratina", "Shaymin", "Arceus", "Victini", "Cobalion", "Terrakion", "Virizion", "Reshiram", "Zekrom", "Landorus", "Kyurem", "Keldeo", "Genesect", "Xerneas", "Yveltal", "Zygarde", "Diancie", "Hoopa", "Cosmog", "Cosmoem", "Buzzwole", "Pheromosa", "Kartana", "Necrozma", "Magearna", "Marshadow", "Blacephalon", "Zeraora", "Zacian", "Zamazenta", "Eternatus", "Kubfu", "Spectrier", "Glastrier", "Regieleki", "Aerodactyl", "Lopunny", "Charizard", "Gallade", "Manectric", "Sceptile", "Salamence", "Pidgeot", "Venusaur", "Blastoise", "Beedrill", "Alakazam", "Gyarados", "Lopunny", "Audino", "Abomasnow", "Steelix", "Ampharos","Lucario" ],
    "regular": ["Darumaka", "Darmanitan", "Wishiwashi", "Drakloak", "Duraludon", "Rotom", "Tentacruel", "Snorlax", "Overqwil", "Munchlax", "Kleavor", "Fennekin", "Delphox", "Dunsparce", "Braixen", "Axew", "Fraxure", "Haxorus", "Floette", "Flabebe", "Rufflet", "Porygon", "Porygon2", "Mankey", "Primeape", "Dratini", "Shellder", "Gible", "Gabite", "Dragonair", "Golett", "Goomy", "Greninja", "Vikavolt", "Vullaby", "Litwick", "Lampent", "Wimpod", "Buneary", "Ursaring", "Teddiursa", "Hawlucha", "Abra", "Kadabra", "Turtonator", "Jolteon", "Dwebble", "Crustle", "Starly", "Stantler", "Rhyhorn", "Staryu", "Starmie", "Tauros", "Lapras", "Vaporeon", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Espeon", "Slakoth", "Vigoroth", "Lotad", "Lombre", "Ludicolo", "Treecko", "Grovyle", "Electrike", "Manectric", "Growlithe", "Monferno", "Piplup", "Prinplup", "Chimchar", "Sirfetch'd", "Staravia", "Bagon", "Shelgon", "Salamence", "Tepig", "Pignite", "Spiritomb", "Togekiss", "Skorupi", "Drilbur", "Timburr", "Gurdurr", "Scraggy", "Scrafty", "Yamask", "Cofagrigus", "Ducklett", "Swanna", "Zorua", "Zoroark", "Cinccino", "Frillish", "Jellicent", "Karrablast", "Escavalier", "Ferroseed", "Mienfoo", "Mienshao", "Cryogonal", "Shelmet", "Accelgor", "Helioptile", "Heliolisk", "Tyrunt", "Tyrantrum", "Sylveon", "Litleo", "Pyroar", "Chespin", "Quilladin", "Chesnaught", "Durant", "Deino", "Phantump", "Trevenant", "Pumpkaboo", "Gourgeist", "Popplio", "Brionne", "Litten", "Torracat", "Rowlet", "Dartrix", "Grookey", "Thwackey", "Rillaboom", "Scorbunny", "Raboot", "Orbeetle", "Rookidee", "Corvisquire", "Sobble", "Drizzile", "Inteleon", "Dracozolt", "Dracovish", "Morpeko", "Sneasler", "Toxapex", "Mareanie", "Volcarona", "Tentacool", "Larvesta", "Charmeleon", "Charmander", "Togetic", "Togepi", "Druddigon", "Dhelmise","Runerigus", "Lucario", "Unfezant", "Tranquill", "Pidove", "Barraskewda", "Arrokuda", "Zubat", "Golbat", "Gastly", "Haunter", "Clauncher", "Clawitzer", "Froslass", "Cutiefly", "Ribombee" ], 
    }

# Reference categories dynamically
repeat_ball = POKEMON_CATEGORIES["legendary"]
regular_ball = POKEMON_CATEGORIES["regular"]
cooldown = random.randint(1, 2)
low_lvl = False

@client.on(events.NewMessage(from_users=572621020))
async def hunt_or_pass(event):
    global cooldown

    if "✨ Shiny Pokémon found!" in event.raw_text:
        await notify_shiny_found(event)
        return

    if "A wild" in event.raw_text:
        pok_name = extract_pokemon_name(event.raw_text)
        print(f"Encountered: {pok_name}")

        if pok_name in POKEMON_CATEGORIES["regular"] or pok_name in POKEMON_CATEGORIES["legendary"]:
            await attempt_catch(event, pok_name)
        else:
            await asyncio.sleep(cooldown)
            await client.send_message(572621020, '/hunt')


async def notify_shiny_found(event):
    """Notify when a shiny Pokémon is found."""
    await event.client.send_message(
        -1002235680545,
        "@Mr_animosity @Xander_sama 4mar shiny aaya Whatsapp kar"
    )
    await client.disconnect()


def extract_pokemon_name(raw_text):
    """Extract Pokémon name from raw text."""
    return raw_text.split("wild ")[1].split(" (")[0]


async def attempt_catch(event, pok_name):
    """Attempt to catch the Pokémon."""
    await asyncio.sleep(cooldown)
    try:
        await event.click(0, 0)
    except MessageIdInvalidError:
        print(f"Failed to click the button for {pok_name}")
        
@client.on(events.NewMessage(from_users=572621020))
async def battlefirst(event):
    """Handle the start of a battle."""
    if "Battle begins!" in event.raw_text:
        wild_pokemon = parse_pokemon_battle_data(event.raw_text)
        if wild_pokemon and wild_pokemon["max_hp"] <= 50:
            await handle_low_level_battle(event)
        else:
            await attack_pokemon(event)


@client.on(events.MessageEdited(from_users=572621020))
async def battle(event):
    """Handle ongoing battle events."""
    if "Wild" in event.raw_text:
        wild_pokemon = parse_pokemon_battle_data(event.raw_text)
        if wild_pokemon:
            health_percentage = calculate_health_percentage(
                wild_pokemon["max_hp"], wild_pokemon["current_hp"]
            )

            if low_lvl:
                await handle_low_health_battle(event, wild_pokemon)
            elif health_percentage > 50:
                await attack_pokemon(event)
            else:
                await handle_low_health_battle(event, wild_pokemon)


def parse_pokemon_battle_data(raw_text):
    """Extract Pokémon details from battle text."""
    match = re.search(r"Wild (\w+) \[.*\]\nLv\. \d+  •  HP \d+/\d+", raw_text)
    if match:
        return {
            "name": match.group(1),
            "current_hp": int(match.group(2)),
            "max_hp": int(match.group(3)),
        }
    return None


async def handle_low_level_battle(event):
    """Handle low-level Pokémon battles."""
    global low_lvl, cooldown
    low_lvl = True
    await asyncio.sleep(cooldown)
    try:
        await event.click(text="Poke Balls")
    except MessageIdInvalidError:
        print("Failed to click Poke Balls for low-level Pokémon.")


async def handle_low_health_battle(event, wild_pokemon):
    """Handle battles when the Pokémon has low health."""
    global cooldown
    await asyncio.sleep(cooldown)
    try:
        await event.click(text="Poke Balls")
        ball_type = (
            "Repeat" if wild_pokemon["name"] in POKEMON_CATEGORIES["legendary"] else "Regular"
        )
        await asyncio.sleep(1)
        await event.click(text=ball_type)
    except MessageIdInvalidError:
        print(f"Failed to click Poke Balls for {wild_pokemon['name']}.")


async def attack_pokemon(event):
    """Attack the Pokémon."""
    await asyncio.sleep(1)
    try:
        await event.click(0, 0)
    except MessageIdInvalidError:
        print("Failed to attack the Pokémon.")
        
@client.on(events.MessageEdited(from_users=572621020))
async def skip(event):
    """Handle events that allow skipping to the next action."""
    if should_skip(event.raw_text):
        await reset_and_hunt()


@client.on(events.MessageEdited(from_users=572621020))
async def pokeSwitch(event):
    """Handle Pokémon switching during a battle."""
    if "Choose your next pokemon." in event.raw_text:
        await switch_pokemon(event, ["Sceptile", "Snorlax", "Sliggoo", "Scizor", "Solgaleo"])


def should_skip(raw_text):
    """Check if the event allows skipping."""
    return any(substring in raw_text for substring in ["fled", "💵", "You caught"])


async def reset_and_hunt():
    """Reset variables and send the hunt command."""
    global cooldown, low_lvl
    low_lvl = False
    await asyncio.sleep(cooldown)
    await client.send_message(572621020, '/hunt')


async def switch_pokemon(event, pokemon_list):
    """Switch to the next Pokémon from the list."""
    for pokemon in pokemon_list:
        try:
            await event.click(text=pokemon)
            print(f"Switched to {pokemon}.")
            return  # Exit loop after a successful click
        except MessageIdInvalidError:
            print(f"Failed to click button for {pokemon}.")
            
@client.on(events.MessageEdited(from_users=572621020))
async def forward_caught_pokemon(event):
    """Forward caught Pokémon messages to the log channel."""
    if is_pokemon_caught(event.raw_text):
        await forward_message(event, LOG_CHANNEL_ID)


def is_pokemon_caught(raw_text):
    """Check if a Pokémon has been caught."""
    return "You caught" in raw_text


async def forward_message(event, channel_id):
    """Forward a message to the specified channel."""
    try:
        await event.forward_to(channel_id)
        print(f"Message forwarded to channel {channel_id}.")
    except Exception as e:
        print(f"Failed to forward message: {e}")
        
client.start()
client.run_until_disconnected()