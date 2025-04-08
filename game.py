from src.player import Player
import json
import os


class Game:
    def __init__(self) -> None:
        self.day = 0
        self.player = None
        self.save = None

    def explore(self) -> None:  # Temp
        self.loop()

    def inventory(self) -> None:  # Temp
        self.loop()

    def start(self) -> None:
        self.menu_start()
        self.loop()

    def loop(self) -> None:
        self.clear_screen()

        print(f"[Dia {self.day}]")
        print("[1] Explorar")
        print("[2] Inventário")
        print("[3] Status")
        print("[9] Salvar Jogo")
        print("[0] Sair")

        opt = input("> ")

        if opt == "1":
            self.explore()
        elif opt == "2":
            self.inventory()
            self.loop()
        elif opt == "3":
            self.clear_screen()
            print(self.player)
            input("[Enter] Voltar")
            self.loop()
        elif opt == "0":
            print("[i] Salvar jogo? (s/n)")
            opt = input("> ").lower()
            if opt == "s":
                self.clear_screen()
                print("[i] Salvando jogo...")
                self.save_game()
                print("[i] Jogo salvo com sucesso!")
                input("[Enter] Sair")
                exit(0)
            elif opt == "n":
                exit(0)
            else:
                self.clear_screen()
                print("[x] Opção Inválida.")
                input("[Enter] Voltar")
                self.loop()
        elif opt == "9":
            self.clear_screen()
            print("[i] Salvando jogo...")
            self.save_game()
            print("[i] Jogo salvo com sucesso!")
            input("[Enter] Voltar")
            self.loop()
        else:
            self.clear_screen()
            print("[x] Opção Inválida.")
            input("[Enter] Voltar")
            self.loop()

    def menu_start(self) -> None:
        self.clear_screen()

        print("Bem-vindo ao RPG!")
        print("[1] Novo Jogo")
        print("[2] Carregar Jogo")
        print("[3] Sair")

        opt = input("> ")

        if opt == "1":
            self.new_game()
        elif opt == "2":
            self.load_game()
        elif opt == "3":
            exit(0)
        else:
            self.clear_screen()
            print("[x] Opção Inválida.")
            input("[Enter] Voltar")
            self.menu_start()

    def new_game(self) -> None:
        self.clear_screen()
        name = input("Digite o nome do seu personagem:\n> ")
        self.player = Player(name=name)
        self.player.title = ", o Iniciante"

    def load_game(self) -> None:
        with open("save.json", "r") as file:
            data = json.load(file)
            self.player = Player(name=data["name"])
            self.player.att = data["att"]
            self.player.lvl = data["lvl"]
            self.player.xp = data["xp"]
            self.player.coins = data["coins"]
            self.player.hp = data["hp"]
            self.player.mp = data["mp"]
            self.player.inv = data["inv"]
            self.player.equip = data["equip"]
            self.player.title = data["title"]

            self.day = data["day"]

    def save_game(self) -> None:  # Temp
        data = {
            "name": self.player.name,
            "att": self.player.att,
            "lvl": self.player.lvl,
            "xp": self.player.xp,
            "coins": self.player.coins,
            "hp": self.player.hp,
            "mp": self.player.mp,
            "inv": self.player.inv,
            "equip": self.player.equip,
            "title": self.player.title,
            "day": self.day,
        }

        with open("save.json", "w") as file:
            json.dump(data, file, indent=4)

    def clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    game = Game()
    game.start()
