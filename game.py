from src.utils.codex import DUNGEON, CITY
from src.utils.menu import (
    MainMenu,
    AdventureMenu,
    CitySelectMenu,
    CityMenu,
    ShopSelectMenu,
    ShopMenu,
    DungeonInteractMenu,
    DungeonSelectMenu,
    HouseMenu,
)
from src.utils.core import (
    SaveManager,
    DungeonManager,
    C,
    show_intro,
    clear_screen,
    type_text,
    progress_bar,
)
from src.entities.player import Player, House
from time import sleep
import json

sm = SaveManager()


class Game:
    def __init__(self):
        self.menu = MainMenu(self)

    def run(self):
        show_intro()
        self.menu.run(menu=True)

    def new_game(self):
        clear_screen()
        slot = sm.select_slot(new=True)
        if slot:
            clear_screen()
            name = self.validate_name()
            player = Player(name)
            sm.save(player, slot)
            self.adventure_menu(player, slot)

    def continue_game(self):
        clear_screen()
        slot = sm.select_slot(new=False)
        if slot:
            try:
                data = sm.load(slot)
                player = Player.from_dict(data)
                self.adventure_menu(player, slot)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                clear_screen()
                type_text(f"{str(e)}", color=C.RED)
                sleep(1.5)

    def quit_game(self):
        clear_screen()
        type_text("Goodbye, hunter!", color=C.RED)
        sleep(1.5)
        print(f"{C.RESET}", end="")
        clear_screen()
        exit()

    def save_game(self, player, slot_file):
        sm.save(player, slot_file)

    def validate_name(self):
        name = False
        while not name:
            name = input(f"\n{C.BLA}Enter your character's name:\n{C.WHI}> {C.BLA}")
            if name:
                return name

    # MENUS

    def adventure_menu(self, player, slot_file):
        menu = AdventureMenu(self, player, slot_file)
        menu.run(True)

    def cityselect_menu(self, player):
        menu = CitySelectMenu(self, player)
        menu.run()

    def city_menu(self, player):
        menu = CityMenu(self, player)
        menu.run()

    def shopselect_menu(self, player):
        menu = ShopSelectMenu(self, player)
        menu.run(True)

    def shop_menu(self, shop, player):
        menu = ShopMenu(shop, player)
        menu.run()

    def dungeonselect_menu(self, player):
        menu = DungeonSelectMenu(self, player)
        menu.run()

    def house_menu(self, player):
        if not hasattr(player, "house"):
            player.house = House(player)
        menu = HouseMenu(player)
        menu.run()

    def exit_menu(self, player, slot_file):
        clear_screen()
        type_text(f"Save before exit?", color=C.CYA)
        i = input(" [y/n]\n>")
        if i.lower() == "y" or i.lower() == "s" or i == "1":
            sm.save(player, slot_file)
            self.menu.run()
        elif i.lower() == "n" or i == "0":
            self.menu.run()
        else:
            self.adventure_menu(player, slot_file)

    # OTHER

    def travel(self, player, city_id):
        if city_id and city_id in CITY:
            city = CITY[city_id]
            travel_time = int(min((city.level * 48) - (player.location * 12), 1))
            clear_screen()
            print(
                f"{C.BLU}You started your journey to {C.CYA}{city.name}{C.BLU}.\nThis will take {int(travel_time / 24)} days."
            )
            input(travel_time)
            player.pass_time(travel_time)
            progress_bar(travel_time)
            clear_screen()
            type_text(f"You arrived at {city.name}!", C.GRE)
            sleep(0.5)
            clear_screen()
            player.location = city_id
            sleep(1)
            return


if __name__ == "__main__":
    game = Game()
    game.run()
