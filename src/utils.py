import os
import time
import json
import random
import time
from colorama import Fore, Style

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
    time.sleep(1)


def roll_dice(sides=20, times=1):
    return [random.randint(1, sides) for _ in range(times)]


def roll_check(mod=0, sides=20):
    result = random.randint(1, sides)
    total = result + mod
    print(f"🎲 Roll: {result} + {mod} = {total}")
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

    def list_slots(self):
        return [
            {
                "file": os.path.join(self.folder, slot),
                "exists": os.path.exists(os.path.join(self.folder, slot)),
            }
            for slot in os.listdir(self.folder)
        ]

    def select_slot(self, new=False):
        clear_screen()
        print(f"{Colors.CYA}Escolha um slot de save:\n")
        for i, slot in enumerate(self.list_slots(), 1):
            status = "Vazio" if not slot["exists"] else f"Existe"
            print(f"{Colors.WHI}[{i}] Slot {i} - {status}")

        opt = input(
            f"{Colors.CYA}\n[i] Digite o número do slot (ou Enter pra cancelar):\n> "
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

    def save_progress(player, slot_file):
        with open(slot_file, "w") as f:
            json.dump(player.to_dict(), f, indent=4)

        def load(self, slot_path):
            with open(slot_path, "r") as f:
                data = json.load(f)
            return data
