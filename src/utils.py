from colorama import Fore, Back, Style
import random
from time import sleep
import json
import os

SAVE_FOLDER = "saves"


class C:
    RESET = Style.RESET_ALL  # Reset

    # Text Colors
    CYA = Fore.CYAN
    YEL = Fore.YELLOW
    MAG = Fore.MAGENTA
    GRE = Fore.GREEN
    BLU = Fore.BLUE
    WHI = Fore.WHITE
    RED = Fore.RED
    BLA = Fore.BLACK

    BLUL = Fore.LIGHTBLUE_EX
    GREL = Fore.LIGHTGREEN_EX
    REDL = Fore.LIGHTRED_EX
    MAGL = Fore.LIGHTMAGENTA_EX
    YELL = Fore.LIGHTYELLOW_EX

    # Text Styles
    NEG = Style.BRIGHT  # Negrito
    FAD = Style.DIM  # Fade
    NOR = Style.NORMAL  # Normal

    def show_colors():  # Colors Showcase
        print("\n=== Cores de Texto ===")
        print(f"{C.CYA}CYAN - Colors.CYA")
        print(f"{C.YEL}YELLOW - Colors.YEL")
        print(f"{C.MAG}MAGENTA - Colors.MAG")
        print(f"{C.GRE}GREEN - Colors.GRE")
        print(f"{C.BLU}BLUE - Colors.BLU")
        print(f"{C.WHI}WHITE - Colors.WHI")
        print(f"{C.RED}RED - Colors.RED")
        print(f"{C.BLA}BLACK - Colors.BLA")

        print(f"\n=== Cores Claras ===")
        print(f"{C.BLUL}LIGHT BLUE - Colors.BLUL")
        print(f"{C.GREL}LIGHT GREEN - Colors.GREL")
        print(f"{C.REDL}LIGHT RED - Colors.REDL")
        print(f"{C.MAGL}LIGHT MAGENTA - Colors.MAGL")
        print(f"{C.YELL}LIGHT YELLOW - Colors.YELL")

        print(f"\n=== Estilos de Texto ===")
        print(f"{C.NEG}NEGRITO - Colors.NEG")
        print(f"{C.FAD}FADE - Colors.FAD")

        print(f"\n{C.RESET}Reset - Colors.RESET")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_intro():
    clear_screen()
    logo = """ _____                   _             _ ____  ____   ____ 
|_   _|__ _ __ _ __ ___ (_)_ __   __ _| |  _ \|  _ \ / ___|
  | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | | |_) | |_) | |  _ 
  | |  __/ |  | | | | | | | | | | (_| | |  _ <|  __/| |_| |
  |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|_|_| \_\_|    \____|"""
    print(f"{C.BLA}{logo}\n")
    type_text("Welcome to the Dungeon Awakening RPG!", color=C.WHI, delay=0.05)
    sleep(1.5)


def title_text(title):
    print(f"{C.NEG}{C.WHI}-- {C.MAG}[ {title} ] {C.WHI}--{C.RESET}")


def option_text(
    i,
    option,
    category=None,
    x=None,
    y=None,
):
    if category == "hupgrade":
        print(f"{C.WHI}[{C.BLA}{i}{C.WHI}] {option} - Lv. {x} - {y}c{C.RESET}")
    elif category == "brew":
        print(f"{C.WHI}[{C.BLA}{i}{C.WHI}] {option} - Ingredients: {x}{C.RESET}")
    else:
        print(f"{C.WHI}[{C.BLA}{i}{C.WHI}] {option}{C.RESET}")


def type_text(text, color=Fore.WHITE, delay=0.03):
    print(color, end="", flush=True)
    for char in text:
        print(char, end="", flush=True)
        sleep(delay)
    print()


def roll_check(mod=0, sides=20):
    result = random.randint(1, sides)  # 1d20
    total = result + mod  # Add modifier
    return total


def progress_bar(time, delay=0.15, length=50):
    for i in range(int(time)):
        progress = (i + 1) / time
        filled_length = int(length * progress)
        bar = f"{C.BLUL}[{'▮' * filled_length}{' ' * (length - filled_length)}] {int(progress * 100)}%"
        print(f"\r{bar}", end="")
        sleep(delay)


# Constants
INVALID_CHOICE = f"{C.RED}{C.NEG}[x] {C.NOR}Invalid choice!"

PRESS_ENTER = f"{C.BLU}{C.NEG}[i] {C.NOR}Press Enter to continue.\n"


class SaveManager:
    def __init__(self, folder=SAVE_FOLDER):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)

    def select_slot(self, new=False):
        clear_screen()
        if new:
            title_text("New Game")
        else:
            if not os.path.exists(self.folder):
                print(f"{C.RED}[x] No saved games found.")
                return None
            else:
                title_text("Continue Game")
        print(
            f"{C.WHI}[{C.BLA}1{C.WHI}] Slot 1 - {'Exists' if os.path.exists(os.path.join(self.folder, 'save1.json')) else 'Empty'}{C.RESET}"
        )
        print(
            f"{C.WHI}[{C.BLA}2{C.WHI}] Slot 2 - {'Exists' if os.path.exists(os.path.join(self.folder, 'save2.json')) else 'Empty'}{C.RESET}"
        )
        print(
            f"{C.WHI}[{C.BLA}3{C.WHI}] Slot 3 - {'Exists' if os.path.exists(os.path.join(self.folder, 'save3.json')) else 'Empty'}{C.RESET}"
        )
        opt = input(
            f"{C.BLA}\nEnter the slot number (or press Enter to cancel):\n{C.WHI}> {C.BLA}"
        )
        if opt not in ["1", "2", "3", ""]:
            print(INVALID_CHOICE)
            sleep(1)
            return None
        if opt == "":
            return None

        slot_path = os.path.join(self.folder, f"save{opt}.json")

        if new and os.path.exists(slot_path):
            clear_screen()
            overwrite = input(
                f"{C.CYA}\n[i] {C.WHI}This slot already contains a saved game. Overwrite? [y/n]\n{C.WHI}> {C.BLA}"
            ).lower()
            if overwrite.lower() != "s" and overwrite.lower() != "y":
                return None
        return slot_path

    def load(self, slot_path):
        if not os.path.exists(slot_path):
            raise FileNotFoundError(f"{C.RED}[x] File {slot_path} not found.")

        try:
            with open(slot_path, "r") as f:
                content = f.read().strip()
                if not content:
                    raise json.JSONDecodeError("Empty file", "", 0)
                data = json.loads(content)
            return data
        except json.JSONDecodeError:
            raise json.JSONDecodeError(
                f"{C.RED}[x] Save file is corrupted or empty.", "", 0
            )

    def save(self, player, slot_path):
        clear_screen()
        with open(slot_path, "w") as f:
            json.dump(player.to_dict(), f, indent=4)
        type_text(f"[i] Progress saved successfully!", color=C.GRE)  # 💾
        print(f"{C.RESET}", end="")
        sleep(1.5)


ABILITIES = {
    "Fireball": {
        "dmg": 5,
        "cost": 5,
        "desc": "Launches a fireball that deals damage to the enemy.",
        "lvl": 1,
    },
    "Heal": {
        "heal": 5,
        "cost": 5,
        "desc": "Heals a certain amount of HP.",
        "lvl": 1,
    },
    "Successive Cut": {
        "dmg": 3,
        "cost": 3,
        "desc": "Deals damage to the enemy with a series of quick attacks.",
        "lvl": 1,
    },
}

# Items available in the shop
SHOP_ITEMS = {
    "potions": [
        {
            "name": "Health Potion",
            "type": "potions",
            "effect": {"heal": 50},
            "price": 20,
            "rarity": "common",
        },
        {
            "name": "Mana Potion",
            "type": "potions",
            "effect": {"mp": 30},
            "price": 25,
            "rarity": "common",
        },
        {
            "name": "Greater Health Potion",
            "type": "potions",
            "effect": {"heal": 100},
            "price": 40,
            "rarity": "common",
        },
        {
            "name": "Greater Mana Potion",
            "type": "potions",
            "effect": {"mp": 60},
            "price": 45,
            "rarity": "common",
        },
        {
            "name": "Supreme Health Potion",
            "type": "potions",
            "effect": {"heal": 200},
            "price": 80,
            "rarity": "rare",
        },
        {
            "name": "Supreme Mana Potion",
            "type": "potions",
            "effect": {"mp": 120},
            "price": 85,
            "rarity": "rare",
        },
    ],
    "weapons": [
        {
            "name": "Iron Sword",
            "type": "weapons",
            "effect": {"dmg": 10},
            "price": 50,
            "rarity": "common",
        },
        {
            "name": "Steel Sword",
            "type": "weapons",
            "effect": {"dmg": 20},
            "price": 100,
            "rarity": "common",
        },
        {
            "name": "Ice Sword",
            "type": "weapons",
            "effect": {"dmg": 35},
            "price": 200,
            "rarity": "rare",
        },
        {
            "name": "Holy Sword",
            "type": "weapons",
            "effect": {"dmg": 50},
            "price": 400,
            "rarity": "rare",
        },
        {
            "name": "Dark Sword",
            "type": "weapons",
            "effect": {"dmg": 70},
            "price": 800,
            "rarity": "epic",
        },
    ],
    "armors": [
        {
            "name": "Leather Armor",
            "type": "armors",
            "effect": {"dfc": 5},
            "price": 40,
            "rarity": "common",
        },
        {
            "name": "Steel Armor",
            "type": "armors",
            "effect": {"dfc": 10},
            "price": 80,
            "rarity": "common",
        },
        {
            "name": "Ice Armor",
            "type": "armors",
            "effect": {"dfc": 20},
            "price": 160,
            "rarity": "rare",
        },
        {
            "name": "Holy Armor",
            "type": "armors",
            "effect": {"dfc": 30},
            "price": 320,
            "rarity": "rare",
        },
        {
            "name": "Dark Armor",
            "type": "armors",
            "effect": {"dfc": 40},
            "price": 640,
            "rarity": "epic",
        },
    ],
    "items": [
        {
            "name": "Bomb",
            "type": "items",
            "effect": {"dmg": 20},
            "price": 30,
            "rarity": "common",
        },
        {
            "name": "Explosive Bomb",
            "type": "items",
            "effect": {"dmg": 40},
            "price": 50,
            "rarity": "common",
        },
        {
            "name": "Atomic Bomb",
            "type": "items",
            "effect": {"dmg": 80},
            "price": 100,
            "rarity": "rare",
        },
        {
            "name": "Holy Bomb",
            "type": "items",
            "effect": {"dmg": 160},
            "price": 200,
            "rarity": "rare",
        },
        {
            "name": "Dark Bomb",
            "type": "items",
            "effect": {"dmg": 320},
            "price": 400,
            "rarity": "epic",
        },
    ],
}


# Function to generate random shop items
def gen_shop():
    shop_items = []

    for category in SHOP_ITEMS:
        # Filter items by category
        category_items = SHOP_ITEMS[category]

        # Generate 3 random items for each category
        for _ in range(3):
            # Determine item rarity
            roll = roll_check(mod=0, sides=100)

            if roll <= 70:
                # Select a common item
                common_items = [
                    item for item in category_items if item.get("rarity") == "common"
                ]
                if common_items:
                    item = random.choice(common_items)
                    item = item.copy()  # Create a copy of the item
                    item["available"] = True  # Mark as available
                    shop_items.append(item)
            elif roll <= 95:
                # Select a rare item
                rare_items = [
                    item for item in category_items if item.get("rarity") == "rare"
                ]
                if rare_items:
                    item = random.choice(rare_items)
                    item = item.copy()  # Create a copy of the item
                    item["available"] = True  # Mark as available
                    shop_items.append(item)
            elif roll <= 99:
                # Select an epic item
                epic_items = [
                    item for item in category_items if item.get("rarity") == "epic"
                ]
                if epic_items:
                    item = random.choice(epic_items)
                    item = item.copy()  # Create a copy of the item
                    item["available"] = True  # Mark as available
                    shop_items.append(item)
            else:
                # Select a legendary item
                legendary_items = [
                    item for item in category_items if item.get("rarity") == "legendary"
                ]
                if legendary_items:
                    item = random.choice(legendary_items)
                    item = item.copy()  # Create a copy of the item
                    item["available"] = True  # Mark as available
                    shop_items.append(item)

    # Organize items by rarity
    rarity_order = {"common": 0, "rare": 1, "epic": 2, "legendary": 3}
    shop_items.sort(key=lambda x: rarity_order.get(x.get("rarity", "common"), 0))

    return shop_items
