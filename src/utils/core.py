from colorama import Fore, Style
from random import randint, choice
from time import sleep
import json
import os

SAVE_FOLDER = "saves"


# Utility Classes
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
        data = player.to_dict()
        with open(slot_path, "w") as f:
            json.dump(data, f, indent=4)
        type_text(f"[i] Progress saved successfully!", color=C.GRE)  # 💾
        print(f"{C.RESET}", end="")
        sleep(1.5)


class C:
    RESET = Style.RESET_ALL  # Reset

    # Text Colors
    CYA = Fore.CYAN
    YEL = Fore.YELLOW
    MAG = Fore.MAGENTA
    RED = Fore.RED
    GRE = Fore.GREEN
    BLU = Fore.BLUE
    WHI = Fore.WHITE
    BLA = Fore.BLACK

    # Text Styles
    BOL = Style.BRIGHT  # BOLrito
    FAD = Style.DIM  # Fade
    NOR = Style.NORMAL  # Normal


# Constant Strings

X = f"{C.BLA}[{C.RED}x{C.BLA}] "
I = f"{C.WHI}[{C.CYA}x{C.WHI}] "
INVALID_CHOICE = f"{X}{C.RED}Invalid choice!"
PRESS_ENTER = f"{I}{C.BLU}Press Enter to continue\n"


def show_intro():
    clear_screen()
    logo = """
 _____                   _             _ ____  ____   ____ 
|_   _|__ _ __ _ __ ___ (_)_ __   __ _| |  _ \|  _ \ / ___|
  | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | | |_) | |_) | |  _ 
  | |  __/ |  | | | | | | | | | | (_| | |  _ <|  __/| |_| |
  |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|_|_| \_\_|    \____|
  """
    # print(f"{C.BLA}{logo}\n")
    type_text(f"{logo}", color=C.WHI, delay=0.002)
    sleep(1.5)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def type_text(text, color=Fore.WHITE, delay=0.03):
    print(color, end="", flush=True)
    for char in text:
        print(char, end="", flush=True)
        sleep(delay)
    print(C.RESET, end="")
    print()


def title_text(title):
    print(f"{C.BOL}{C.WHI}-- {C.MAG}[ {title} ] {C.WHI}--{C.RESET}")


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


def chance(mod=0, sides=100):
    result = randint(1, int(sides))  # 1d20
    total = result + mod  # Add modifier
    return total


def progress_bar(time, delay=0.15, length=50):
    for i in range(int(time)):
        progress = (i + 1) / time
        filled_length = int(length * progress)
        bar = f"{C.BLU}[{'▮' * filled_length}{' ' * (length - filled_length)}] {int(progress * 100)}%"
        print(f"\r{bar}", end="")
        sleep(delay)


class DungeonManager:

    def __init__(self, game, dungeon, player):
        self.game = game
        self.dungeon = dungeon
        self.level = dungeon.level
        self.player = player

    def start(self):
        from utils.menu import DungeonInteractMenu

        self.set_enemies_random()
        self.set_items()
        type_text(f"Entering {self.dungeon.name}...")
        sleep(1)
        self.dungeon_menu = DungeonInteractMenu(self, self.player, self.dungeon)
        self.dungeon_menu.run()

    def set_enemies_random(self):
        from utils.codex import DUNGEON_ENEMIES, BOSS

        self.dungeon.boss = BOSS[self.level]

        i = self.level * self.level
        for _ in range(4):
            pct = chance()
            if pct <= 10:
                for _ in range(3):
                    self.dungeon.enemies.append(choice(DUNGEON_ENEMIES[self.level]))
            elif pct <= 30:
                for _ in range(2):
                    self.dungeon.enemies.append(choice(DUNGEON_ENEMIES[self.level]))
            elif pct <= 80:
                self.dungeon.enemies.append(choice(DUNGEON_ENEMIES[self.level]))

    def set_items(self):
        self.dungeon.items = []

    def remove_item(self, item):
        self.dungeon.items.remove(item)

    def explore(self):
        from utils.codex import DUNGEON_ITEMS
        from combat.combat import Combat
        from utils.item import get_rarity

        roll = chance()
        if roll >= 75:  # 25% Chance to find an enemy
            if self.dungeon.has_boss() and roll >= 95:
                type_text("[!] You found the dungeon boss!", C.RED)
                sleep(1)
                fight = Combat()
                fight.start(self.player, self.dungeon.boss)
                if not self.player.is_alive():
                    self.player.game_over()
                if not self.dungeon.boss.is_alive():
                    print(f"{C.MAG}[i] You defeated the boss of {self.dungeon.name}!")
                    # Check legendary drops
                    if self.dungeon.boss.item_reward:
                        for item in self.dungeon.boss.item_reward:
                            print(
                                f"{C.MAG}✨ You found a legendary item: {item['name']}!"
                            )
                            self.player.add_item(item, item["type"])
                    sleep(1)
                    self.dungeon.remove_boss()
            else:
                enemy = self.dungeon.get_enemy()
                if enemy:
                    fight = Combat()
                    fight.start(self.player, enemy)
                    if not self.player.is_alive():
                        self.player.game_over()
                    if not enemy.is_alive():
                        self.dungeon.remove_enemy(enemy)
        elif roll >= 60:  # 15% Chance to find an item
            roll = chance()
            if roll > (95):  # 5% EPIC
                item = choice(get_rarity("epic", DUNGEON_ITEMS[self.level]))
            elif roll > (80):  # 15% RARE
                item = choice(get_rarity("rare", DUNGEON_ITEMS[self.level]))
            else:  # 80% COMMON
                item = choice(get_rarity("common", DUNGEON_ITEMS[self.level]))

            self.player.add_item(item)
            type_text(f"You found {item}!", C.BLU)
            sleep(1.5)
        # elif roll >= 50: # TODO: 10% Chance to ???
        else:
            print(f"{C.GRE}You explored the area and found nothing...")
            sleep(1)

    def exit(self):
        self.game.adventure()
