import asyncio
import re
import random
from collections import deque
from telethon import TelegramClient, events
from telethon.errors import MessageIdInvalidError

# Telegram API credentials
API_ID = '29848170'
API_HASH = 'e2b1cafae7b2492c625e19db5ec7f513'
SESSION_STRING = '"1BVtsOH8Bu4FVmqgUEOPlLr_eCNE1LLZG6HYP-byyEwqkhlgqEBSnKD-E5R4mxJolZHfOx-X0Lpgjr3ApU_a0E-q2kaz7wUErqCWCVJxU4ZsMYasvF63OJEn553RXpFIi0SMnmJS1XHCQthYKksRnNba_Of3eOzUEyM95ftNoqTurHv_Ft-M0_tgmmM7x9ZYKf6EfFGEwjbsIlmf7rjcDv6gsOHt9vlQiRWiGc48tXAT02QHAuYMOy-e6nSOPB40p4l3BO6GufwiSnOkCtVdkIbQq9zukLHPLHq18iNlpUI6-Khx87E3McikCNEBVeEn_36KSurj6k9Pm67qCHfo0fAaOL1VXjzA="'

# Initialize Telegram Client
client = TelegramClient('your_session_file.session', API_ID, API_HASH)

# Globals
clicked_4th_button = False  # Tracks whether the 4th button has been clicked
last_two_messages = deque(maxlen=2)  # Stores the last two messages for context
LOG_CHANNEL_ID = -1002366595362  # Replace with your log channel ID

legendary_poks = ["Zapdos", "Mewtwo", "Lugia", "Ho-Oh", "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys", "Dialga", "Palkia", "Regigigas", "Giratina", "Shaymin", "Arceus", "Victini", "Cobalion", "Terrakion", "Virizion", "Reshiram", "Zekrom", "Landorus", "Kyurem", "Keldeo", "Genesect", "Xerneas", "Yveltal", "Zygarde", "Diancie", "Hoopa", "Cosmog", "Cosmoem", "Buzzwole", "Pheromosa", "Kartana", "Necrozma", "Magearna", "Marshadow", "Blacephalon", "Zeraora", "Zacian", "Zamazenta", "Eternatus", "Kubfu", "Spectrier", "Glastrier", "Regieleki", "Aerodactyl", "Lopunny", "Charizard", "Gallade", "Manectric", "Sceptile", "Salamence", "Pidgeot", "Venusaur", "Blastoise", "Beedrill", "Alakazam", "Gyarados", "Lopunny", "Audino", "Abomasnow", "Steelix", "Ampharos","Lucario"]

regular_ball = ["Darumaka", "Darmanitan", "Wishiwashi", "Drakloak", "Duraludon", "Rotom", "Tentacruel", "Snorlax", "Overqwil", "Munchlax", "Kleavor", "Fennekin", "Delphox", "Dunsparce", "Braixen", "Axew", "Fraxure", "Haxorus", "Floette", "Flabebe", "Rufflet", "Porygon", "Porygon2", "Mankey", "Primeape", "Dratini", "Shellder", "Gible", "Gabite", "Dragonair", "Golett", "Goomy", "Greninja", "Vikavolt", "Vullaby", "Litwick", "Lampent", "Wimpod", "Buneary", "Ursaring", "Teddiursa", "Hawlucha", "Abra", "Kadabra", "Turtonator", "Jolteon", "Dwebble", "Crustle", "Starly", "Stantler", "Rhyhorn", "Staryu", "Starmie", "Tauros", "Lapras", "Vaporeon", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Espeon", "Slakoth", "Vigoroth", "Lotad", "Lombre", "Ludicolo", "Treecko", "Grovyle", "Electrike", "Manectric", "Growlithe", "Monferno", "Piplup", "Prinplup", "Chimchar", "Sirfetch'd", "Staravia", "Bagon", "Shelgon", "Salamence", "Tepig", "Pignite", "Spiritomb", "Togekiss", "Skorupi", "Drilbur", "Timburr", "Gurdurr", "Scraggy", "Scrafty", "Yamask", "Cofagrigus", "Ducklett", "Swanna", "Zorua", "Zoroark", "Cinccino", "Frillish", "Jellicent", "Karrablast", "Escavalier", "Ferroseed", "Mienfoo", "Mienshao", "Cryogonal", "Shelmet", "Accelgor", "Helioptile", "Heliolisk", "Tyrunt", "Tyrantrum", "Sylveon", "Litleo", "Pyroar", "Chespin", "Quilladin", "Chesnaught", "Durant", "Deino", "Phantump", "Trevenant", "Pumpkaboo", "Gourgeist", "Popplio", "Brionne", "Litten", "Torracat", "Rowlet", "Dartrix", "Grookey", "Thwackey", "Rillaboom", "Scorbunny", "Raboot", "Orbeetle", "Rookidee", "Corvisquire", "Sobble", "Drizzile", "Inteleon", "Dracozolt", "Dracovish", "Morpeko", "Sneasler", "Toxapex", "Mareanie", "Volcarona", "Tentacool", "Larvesta", "Charmeleon", "Charmander", "Togetic", "Togepi", "Druddigon", "Dhelmise","Runerigus", "Lucario", "Unfezant", "Tranquill", "Pidove", "Barraskewda", "Arrokuda", "Zubat", "Golbat", "Gastly", "Haunter", "Clauncher", "Clawitzer", "Froslass", "Cutiefly", "Ribombee"]

repeat_ball = legendary_poks
cooldown = random.randint(1, 2)
low_lvl = False

@client.on(events.NewMessage(from_users=572621020))
async def daily_limit(event):
    """
    Handles the event when the daily hunt limit is reached.
    Disconnects the client gracefully.
    """
    if "Daily hunt limit reached" in event.raw_text:
        print("Daily hunt limit reached. Disconnecting the client...")
        
        async def disconnect_with_retry(retries=3, delay=1):
            """Retries disconnecting the client in case of transient errors."""
            for attempt in range(retries):
                try:
                    await client.disconnect()
                    print("Client disconnected successfully.")
                    return
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed to disconnect: {e}")
                    if attempt < retries - 1:
                        await asyncio.sleep(delay)
                    else:
                        print("Failed to disconnect the client after multiple attempts.")

        await disconnect_with_retry()
        
@client.on(events.NewMessage(from_users=572621020))
async def hunt_or_pass(event):
    """
    Handles the hunting event by reacting to shiny Pokémon, wild Pokémon, or sending new hunt commands.
    """
    global cooldown

    # Notify and disconnect if a shiny Pokémon is found
    if "✨ Shiny Pokémon found!" in event.raw_text:
        await event.client.send_message(
            -1002235680545,
            "@Mr_animosity @Xander_sama 4mar shiny aaya Whatsapp kar"
        )
        print("Shiny Pokémon found! Notified and disconnecting...")
        await disconnect_with_retry()
        return

    # Handle wild Pokémon events
    elif "A wild" in event.raw_text:
        try:
            pok_name = event.raw_text.split("wild ")[1].split(" (")[0]
            print(f"Encountered Pokémon: {pok_name}")

            if pok_name in  regular_ball  or pok_name in repeat_ball:
                await asyncio.sleep(cooldown)
                await click_with_retry(event, 0, 0)
            else:
                # Continue hunting for the next Pokémon
                await asyncio.sleep(cooldown)
                await event.client.send_message(572621020, '/hunt')

        except IndexError:
            print("Failed to extract Pokémon name from the event text.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


async def click_with_retry(event, row, col, retries=3, delay=1):
    """
    Retries clicking a button in the Pokémon hunting event.

    Args:
        event (Event): The Telegram event object.
        row (int): Row index of the button.
        col (int): Column index of the button.
        retries (int): Number of retry attempts.
        delay (int): Delay between retries in seconds.
    """
    for attempt in range(retries):
        try:
            await event.click(row, col)
            print("Successfully clicked the button.")
            return
        except MessageIdInvalidError:
            print(f"Attempt {attempt + 1} failed to click the button.")
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                print("Failed to click the button after multiple attempts.")


async def disconnect_with_retry(retries=3, delay=1):
    """
    Retries disconnecting the Telegram client gracefully.

    Args:
        retries (int): Number of retry attempts.
        delay (int): Delay between retries in seconds.
    """
    for attempt in range(retries):
        try:
            await client.disconnect()
            print("Client disconnected successfully.")
            return
        except Exception as e:
            print(f"Attempt {attempt + 1} failed to disconnect: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                print("Failed to disconnect the client after multiple attempts.")
                
@client.on(events.NewMessage(from_users=572621020))
async def battlefirst(event):
    """
    Handles battle initiation and decides actions based on Pokémon's level and HP.
    """
    global low_lvl
    global cooldown

    if "Battle begins!" in event.raw_text:
        print("Battle initiated!")
        try:
            wild_pokemon_name_match = re.search(
                r"Wild (\w+) \[.*\]\nLv\. \d+  •  HP \d+/\d+", event.raw_text
            )
            if not wild_pokemon_name_match:
                print("Could not find Pokémon name.")
                return

            pok_name = wild_pokemon_name_match.group(1)
            print(f"Encountered Pokémon: {pok_name}")

            wild_pokemon_hp_match = re.search(
                r"Wild .* \[.*\]\nLv\. \d+  •  HP (\d+)/(\d+)", event.raw_text
            )
            if not wild_pokemon_hp_match:
                print("Could not find Pokémon HP.")
                return

            wild_max_hp = int(wild_pokemon_hp_match.group(2))
            print(f"Pokémon Max HP: {wild_max_hp}")

            if wild_max_hp <= 50:
                low_lvl = True
                print("Low level Pokémon detected. Attempting to catch...")
                await asyncio.sleep(cooldown)
                await click_with_retry(event, text="Poke Balls")
            else:
                print("High-level Pokémon detected. Initiating attack...")
                await asyncio.sleep(2)
                await click_with_retry(event, row=0, col=0)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")


async def click_with_retry(event, row=None, col=None, text=None, retries=3, delay=1):
    """
    Retries clicking a button in the Pokémon event.

    Args:
        event (Event): The Telegram event object.
        row (int): Row index of the button (optional).
        col (int): Column index of the button (optional).
        text (str): Button text to click (optional).
        retries (int): Number of retry attempts.
        delay (int): Delay between retries in seconds.
    """
    for attempt in range(retries):
        try:
            if text:
                await event.click(text=text)
            elif row is not None and col is not None:
                await event.click(row, col)
            else:
                raise ValueError("Either 'text' or 'row' and 'col' must be provided.")
            print("Successfully clicked the button.")
            return
        except MessageIdInvalidError:
            print(f"Attempt {attempt + 1} failed to click the button.")
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                print("Failed to click the button after multiple attempts.")
        except Exception as e:
            print(f"An unexpected error occurred during clicking: {e}")


def calculate_health_percentage(max_hp, current_hp):
    """
    Calculates the health percentage of a Pokémon.

    Args:
        max_hp (int): Maximum HP of the Pokémon.
        current_hp (int): Current HP of the Pokémon.

    Returns:
        int: Health percentage.

    Raises:
        ValueError: If the health values are invalid.
    """
    if max_hp <= 0:
        raise ValueError("Total health must be greater than zero.")
    if current_hp < 0 or current_hp > max_hp:
        raise ValueError("Current health must be between 0 and the total health.")
    return round((current_hp / max_hp) * 100)
    
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
    """
    Handles the skip event after a battle or encounter based on specific keywords.
    """
    global cooldown
    global low_lvl

    try:
        # Check if any of the specific substrings are in the message.
        if any(substring in event.raw_text for substring in ["fled", "💵", "You caught"]):
            low_lvl = False  # Reset low-level flag after catching or fleeing.
            print("Battle outcome detected. Resetting low_lvl flag.")
            
            # Delay before proceeding to next hunt
            await asyncio.sleep(cooldown)

            # Send /hunt command to continue the process
            await client.send_message(572621020, '/hunt')
            print("Sent /hunt command after battle/flee.")
    except Exception as e:
        print(f"Error in skip event handler: {e}")
        
@client.on(events.NewMessage(from_users=572621020))
async def skipTrainer(event):
    """
    Handles the event where the message contains "An expert trainer" and sends the /hunt command.
    """
    global cooldown

    try:
        # Check if the message indicates the presence of an expert trainer.
        if "An expert trainer" in event.raw_text:
            print("Expert trainer encountered. Sending /hunt command after cooldown.")
            
            # Wait for the cooldown period before sending the command.
            await asyncio.sleep(cooldown)

            # Send /hunt command to continue the process.
            await client.send_message(572621020, '/hunt')
            print("Sent /hunt command after encountering an expert trainer.")
    
    except Exception as e:
        # Log any errors that occur during the process.
        print(f"Error in skipTrainer event handler: {e}")
      
@client.on(events.MessageEdited(from_users=572621020))
async def pokeSwitch(event):
    """
    Handles the event when the message contains 'Choose your next pokemon.' and attempts to click specified buttons.
    """
    try:
        if "Choose your next pokemon." in event.raw_text:
            # List of buttons to click for selecting the next pokemon
            buttons_to_click = ["Sceptile", "Snorlax", "Sliggoo", "Scizor", "Solgaleo"]
            for button in buttons_to_click:
                success = False
                retries = 3  # Number of retries before failing

                for _ in range(retries):
                    try:
                        # Try to click the button with the text matching the pokemon's name
                        await event.click(text=button)
                        print(f"Clicked button for {button}")
                        success = True
                        break  # Exit retry loop if click is successful
                    except MessageIdInvalidError:
                        print(f"Failed to click button {button}. Retrying...")
                        await asyncio.sleep(1)  # Small delay before retrying

                if not success:
                    print(f"Failed to click button {button} after {retries} retries.")
                    
    except Exception as e:
        # Catch any unexpected errors during the process
        print(f"Error in pokeSwitch event handler: {e}")
        
@client.on(events.MessageEdited(from_users=572621020))
async def forward_caught_pokemon(event):
    if "You caught" in event.raw_text:
        # Forward the message to the log channel
        await event.forward_to(LOG_CHANNEL_ID)
        
client.start()
client.run_until_disconnected()