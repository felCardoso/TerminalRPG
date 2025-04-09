import os
import time
from src.player import Player
from src.enemy import Enemy
from src.fight import Fight
from src.utils import Colors, SaveManager, clear_screen, type_text

sm = SaveManager()


def main_menu():
    while True:
        clear_screen()
        print(f"{Colors.MAG}🎮 DUNGEON AWAKENING RPG\n")
        print(f"{Colors.WHI}[1] Novo Jogo")
        print("[2] Continuar")
        print("[3] Sair")
        i = input("\nEscolha uma opção:\n> ")

        if i == "1":
            clear_screen()
            slot = sm.select_slot(new=True)
            if slot:
                new_game(slot)
        elif i == "2":
            clear_screen()
            slot = sm.select_slot(new=False)
            if slot:
                continue_game(slot)
        elif i == "3":
            print("Até logo, caçador!")
            break
        else:
            clear_screen()
            print(f"{Colors.RED}[x] Escolha inválida!")
            time.sleep(1)
            input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")


def new_game(slot_file):
    clear_screen()
    name = input("Digite o nome do seu personagem: ")
    player = Player(name)
    sm.save(player, os.path.basename(slot_file))
    start_adventure(player, slot_file)


def continue_game(slot_file):
    try:
        data = sm.load(slot_file)
        player = Player.from_dict(data)
        start_adventure(player, slot_file)
    except FileNotFoundError:
        print(f"{Colors.RED}[x] Arquivo de save não encontrado!\n")
        time.sleep(1)
        input(f"{Colors.LBLU}[i] Pressione Enter para voltar ao menu principal.")
        main_menu()


def start_adventure(player, slot_file):
    while True:
        clear_screen()
        print(f"{player.name} entra na dungeon...\n")
        print("O que você deseja fazer?")
        print(f"{Colors.LBLU}1. Explorar (combate)")
        print(f"2. Ver status do personagem")
        print(f"3. Salvar e sair")
        choice = input("> ")

        if choice == "1":
            clear_screen()
            enemy = Enemy("Goblin", 20, 3, 10, 5)
            fight = Fight()
            fight.start(player, enemy)
        elif choice == "2":
            clear_screen()
            print(player)
            input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")
        elif choice == "3":
            clear_screen()
            sm.save(player, os.path.basename(slot_file))
            print("Saindo para o menu principal...")
            time.sleep(1)
            break
        else:
            clear_screen()
            print(f"{Colors.RED}[x] Escolha inválida!")


if __name__ == "__main__":
    main_menu()
