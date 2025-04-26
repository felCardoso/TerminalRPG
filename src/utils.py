from colorama import Fore, Style
import random
import time
import json
import os

SAVE_FOLDER = "saves"


class Colors:
    RESET = Style.RESET_ALL

    CYA = Fore.CYAN
    YEL = Fore.YELLOW
    MAG = Fore.MAGENTA
    GRE = Fore.GREEN
    BLU = Fore.BLUE
    WHI = Fore.WHITE
    RED = Fore.RED

    LBLU = Fore.LIGHTBLUE_EX
    LGRE = Fore.LIGHTGREEN_EX
    LRED = Fore.LIGHTRED_EX
    LMAG = Fore.LIGHTMAGENTA_EX


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def type_text(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def show_intro():
    clear_screen()
    print(f"{Fore.MAG}DUNGEON AWAKENING RPG")
    print(f"{Fore.CYA} ")
    type_text("Welcome to the Dungeon Awakening RPG!", delay=0.05)
    time.sleep(1.5)


def roll_dice(sides=20, times=1):
    return [random.randint(1, sides) for _ in range(times)]


def roll_check(mod=0, sides=20):
    result = random.randint(1, sides)  # 1d20
    total = result + mod  # Add modifier
    return total


def type_text(text, color=Fore.WHITE, delay=0.03):
    print(color, end="", flush=True)
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


class SaveManager:
    def __init__(self, folder=SAVE_FOLDER):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)

    def select_slot(self, new=False):
        clear_screen()
        if new:
            print(f"{Colors.MAG}🎮 Novo Jogo")
        else:
            if not os.path.exists(self.folder):
                print(f"{Colors.RED}[x] Nenhum jogo salvo encontrado.")
                return None
            else:
                print(f"{Colors.MAG}🎮 Continuar Jogo")
        print(
            f"{Colors.MAG}[1] Slot 1 - {'Existe 'if (os.path.exists(os.path.join(self.folder, 'save1.json'))) else 'Vazio'}"
        )
        print(
            f"{Colors.MAG}[2] Slot 2 - {'Existe 'if os.path.exists(os.path.join(self.folder, 'save2.json')) else 'Vazio'}"
        )
        print(
            f"{Colors.MAG}[3] Slot 3 - {'Existe 'if os.path.exists(os.path.join(self.folder, 'save3.json')) else 'Vazio'}"
        )
        opt = input(
            f"{Colors.CYA}\nDigite o número do slot (ou Enter pra cancelar):\n> "
        )
        if opt not in ["1", "2", "3"]:
            return None

        slot_path = os.path.join(self.folder, f"save{opt}.json")

        if new and os.path.exists(slot_path):
            overwrite = input(
                "\n[i] Esse slot já contém um jogo salvo. Deseja sobrescrever? [s/n]\n> "
            ).lower()
            if overwrite != "s":
                return None
        return slot_path

    def load(self, slot_path):
        if not os.path.exists(slot_path):
            raise FileNotFoundError(
                f"{Colors.RED}[x]Arquivo {slot_path} não encontrado."
            )
        with open(slot_path, "r") as f:
            data = json.load(f)
        return data

    def save(self, player, slot_path):
        with open(slot_path, "w") as f:
            json.dump(player.to_dict(), f, indent=4)
        print(f"\n{Colors.GRE}💾 Progresso salvo com sucesso!{Colors.RESET}")


ABILITIES = {
    "Bola de Fogo": {
        "dmg": 5,
        "cost": 5,
        "desc": "Lança uma bola de fogo que causa dano ao inimigo.",
        "lvl": 1,
    },
    "Cura": {
        "heal": 5,
        "cost": 5,
        "desc": "Cura uma quantidade de HP.",
        "lvl": 1,
    },
    "Corte Sucessivo": {
        "dmg": 3,
        "cost": 3,
        "desc": "Causa dano ao inimigo com uma série de ataques rápidos.",
        "lvl": 1,
    },
}

# Itens disponíveis na loja
SHOP_ITEMS = {
    "potions": [
        {
            "name": "Poção de Vida",
            "type": "potions",
            "effect": {"heal": 50},
            "price": 20,
            "rarity": "comum",
        },
        {
            "name": "Poção de Mana",
            "type": "potions",
            "effect": {"mp": 30},
            "price": 25,
            "rarity": "comum",
        },
        {
            "name": "Poção de Vida Grande",
            "type": "potions",
            "effect": {"heal": 100},
            "price": 40,
            "rarity": "comum",
        },
        {
            "name": "Poção de Mana Grande",
            "type": "potions",
            "effect": {"mp": 60},
            "price": 45,
            "rarity": "comum",
        },
        {
            "name": "Poção de Vida Suprema",
            "type": "potions",
            "effect": {"heal": 200},
            "price": 80,
            "rarity": "raro",
        },
        {
            "name": "Poção de Mana Suprema",
            "type": "potions",
            "effect": {"mp": 120},
            "price": 85,
            "rarity": "raro",
        },
    ],
    "weapons": [
        {
            "name": "Espada de Ferro",
            "type": "weapons",
            "effect": {"dmg": 10},
            "price": 50,
            "rarity": "comum",
        },
        {
            "name": "Espada de Aço",
            "type": "weapons",
            "effect": {"dmg": 20},
            "price": 100,
            "rarity": "comum",
        },
        {
            "name": "Espada de Gelo",
            "type": "weapons",
            "effect": {"dmg": 35},
            "price": 200,
            "rarity": "raro",
        },
        {
            "name": "Espada Sagrada",
            "type": "weapons",
            "effect": {"dmg": 50},
            "price": 400,
            "rarity": "raro",
        },
        {
            "name": "Espada Sombria",
            "type": "weapons",
            "effect": {"dmg": 70},
            "price": 800,
            "rarity": "épico",
        },
    ],
    "armors": [
        {
            "name": "Armadura de Couro",
            "type": "armors",
            "effect": {"dfc": 5},
            "price": 40,
            "rarity": "comum",
        },
        {
            "name": "Armadura de Aço",
            "type": "armors",
            "effect": {"dfc": 10},
            "price": 80,
            "rarity": "comum",
        },
        {
            "name": "Armadura de Gelo",
            "type": "armors",
            "effect": {"dfc": 20},
            "price": 160,
            "rarity": "raro",
        },
        {
            "name": "Armadura Sagrada",
            "type": "armors",
            "effect": {"dfc": 30},
            "price": 320,
            "rarity": "raro",
        },
        {
            "name": "Armadura Sombria",
            "type": "armors",
            "effect": {"dfc": 40},
            "price": 640,
            "rarity": "épico",
        },
    ],
    "items": [
        {
            "name": "Bomba",
            "type": "items",
            "effect": {"dmg": 20},
            "price": 30,
            "rarity": "comum",
        },
        {
            "name": "Bomba Explosiva",
            "type": "items",
            "effect": {"dmg": 40},
            "price": 50,
            "rarity": "comum",
        },
        {
            "name": "Bomba Atômica",
            "type": "items",
            "effect": {"dmg": 80},
            "price": 100,
            "rarity": "raro",
        },
        {
            "name": "Bomba Sagrada",
            "type": "items",
            "effect": {"dmg": 160},
            "price": 200,
            "rarity": "raro",
        },
        {
            "name": "Bomba Sombria",
            "type": "items",
            "effect": {"dmg": 320},
            "price": 400,
            "rarity": "épico",
        },
    ],
}

# Número de itens que aparecem na loja por categoria
ITEMS_PER_CATEGORY = {"comum": 5, "raro": 2, "épico": 1}


# Função para gerar itens aleatórios da loja
def gen_shop():
    shop_items = []
    for category in SHOP_ITEMS:
        items = SHOP_ITEMS[category]

        # Separar itens por raridade
        common_items = [item for item in items if item.get("rarity") == "comum"]
        rare_items = [item for item in items if item.get("rarity") == "raro"]
        epic_items = [item for item in items if item.get("rarity") == "épico"]

        # Selecionar itens de cada raridade
        if common_items:
            selected_common = random.sample(
                common_items, min(ITEMS_PER_CATEGORY["comum"], len(common_items))
            )
            shop_items.extend(selected_common)

        if rare_items:
            selected_rare = random.sample(
                rare_items, min(ITEMS_PER_CATEGORY["raro"], len(rare_items))
            )
            shop_items.extend(selected_rare)

        if epic_items:
            selected_epic = random.sample(
                epic_items, min(ITEMS_PER_CATEGORY["épico"], len(epic_items))
            )
            shop_items.extend(selected_epic)

    return shop_items
