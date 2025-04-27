from src.utils import (
    C,
    clear_screen,
    title_text,
    option_text,
    INVALID_CHOICE,
    PRESS_ENTER,
)
from src.house import ROOMS
from time import sleep
from src.enemy import DUNGEON_LEVELS


class Menu:
    def __init__(self, title, options):
        self.title = title
        self.options = options

    def display(self, x=False):
        clear_screen()
        title_text(self.title)
        if x:
            for i, (option, _) in enumerate(self.options, 1):
                if i <= len(self.options):
                    option_text(i, option)

        else:
            for i, (option, _) in enumerate(self.options, 1):
                if i < len(self.options):
                    option_text(i, option)
                else:
                    option_text(0, option)

    def get_choice(self, menu=False):
        while True:
            try:
                choice = int(input(f"\n{C.BLA}Choose an option:\n{C.WHI}> {C.BLA}"))
                if not menu:
                    if 0 <= choice <= len(self.options):
                        return choice
                else:
                    if 1 <= choice <= len(self.options):
                        return choice
                raise ValueError
            except ValueError:
                print(INVALID_CHOICE)
                sleep(1)
                clear_screen()
                self.display(menu)

    def run(self, menu=False):
        while True:
            clear_screen()
            self.display(menu)
            choice = self.get_choice(menu)
            if not menu:
                if choice == 0:
                    return
            _, action = self.options[choice - 1]
            action()


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(
            "Main Menu",
            [
                ("New Game", game.new_game),
                ("Continue", game.continue_game),
                ("Exit", game.quit_game),
            ],
        )


class AdventureMenu(Menu):
    def __init__(self, game, player, slot_file):
        super().__init__(
            "Adventure",
            [
                ("Dungeons", lambda: game.explore_dungeon(player)),
                ("Player Status", lambda: self.show_status(player)),
                ("Shop", lambda: game.shop_menu(player)),
                ("Inventory", lambda: player.show_inventory(True)),
                ("House", lambda: game.house_menu(player)),
                ("Save", lambda: game.save_game(player, slot_file)),
                ("Main Menu", lambda: game.exit_menu(player, slot_file)),
            ],
        )

    def show_status(self, player):
        clear_screen()
        print(player)
        input(PRESS_ENTER)


class DungeonsMenu(Menu):
    def __init__(self, game, player):
        super().__init__(
            "Dungeons",
            [
                (
                    f"{dungeon.name} {C.BLA}- {C.WHI}Lv. {dungeon.level} {C.BLA}/ {C.WHI}{dungeon.level * 2} days of travel{C.RESET}",
                    lambda d=dungeon: game.travel_dungeon(player, d.level),
                )
                for dungeon in DUNGEON_LEVELS.values()
            ],
        )


class DungeonMenu(Menu):
    def __init__(self, game, player, dungeon):
        super().__init__(
            dungeon.name,
            [
                ("Explore", lambda: game.explore_dungeon_area(player, dungeon)),
                ("Player Status", lambda: self.show_status(player)),
                ("Inventory", lambda: player.show_inventory(use=True)),
                ("Exit", lambda: game.adventure_menu.run()),
            ],
        )

    def show_status(self, player):
        clear_screen()
        print(player)
        input(PRESS_ENTER)


class HouseMenu(Menu):
    def __init__(self, player):
        super().__init__(
            "Home",
            [
                ("House Status", lambda: player.house.show_status()),
                ("Upgrade Room", lambda: self.upgrade_rooms(player)),
                ("Brew Potions", lambda: self.brew_potions(player)),
                ("Craft items", lambda: self.craft_items(player)),
                ("Garden", lambda: self.garden(player)),
                ("Sleep", lambda: self.sleep(player)),
                ("Exit", lambda: None),
            ],
        )

    def upgrade_rooms(self, player):
        clear_screen()
        title_text("Room Upgrades")
        print(f"{C.WHI}Which room would you like to upgrade?")
        rooms = list(player.house.rooms.items())
        for i, (room, level) in enumerate(rooms, 1):
            cost = (
                ROOMS[room]["cost"] * 1.5 if level == 1 else ROOMS[room]["cost"] * level
            )
            option_text(i=i, option=room.title(), category="hupgrade", x=level, y=cost)
        try:
            choice = int(input(f"\n{C.BLA}Choose an option:\n{C.WHI}> {C.BLA}"))
            if choice:
                choice = int(choice)
                if 1 <= choice <= len(rooms):
                    room = rooms[choice - 1][0]
                    player.house.upgrade_room(room)
                elif choice == "" or choice == 0:
                    return
                else:
                    print(f"{C.RED}[x] Invalid room number!")
                input(PRESS_ENTER)
        except ValueError:
            print(f"{C.RED}[x] Please enter a valid number!")
            input(PRESS_ENTER)

    def brew_potions(self, player):
        clear_screen()
        title_text("Brewing")
        print(f"{C.WHI}Available Potions:")
        potion_list = list(player.house.recipes["potions"].keys())
        for i, recipe in enumerate(potion_list, 1):
            ingredients = ", ".join(
                player.house.recipes["potions"][recipe]["ingredients"]
            )
            option_text(i=i, option=recipe, category="brew", x=ingredients)
            print(f"{C.BLUL}[{i}] {recipe}: {ingredients}")

        try:
            choice = int(input(f"\n{C.CYA}[i] Choose a potion number:\n> "))
            if 1 <= choice <= len(potion_list):
                recipe = potion_list[choice - 1]
            else:
                print(f"{C.RED}[x] Invalid potion number!")
                return
        except ValueError:
            print(f"{C.RED}[x] Please enter a valid number!")
            return

        player.house.brew_potion(recipe)
        input(PRESS_ENTER)

    def craft_items(self, player):
        clear_screen()
        title_text("Crafting")
        print(f"{C.WHI}Available Items:")
        item_list = list(player.house.recipes["crafting"].keys())
        for i, recipe in enumerate(item_list, 1):
            ingredients = ", ".join(
                player.house.recipes["crafting"][recipe]["ingredients"]
            )
            option_text(i=i, option=recipe, category="craft", x=ingredients)

        try:
            choice = int(
                input(f"\n{C.CYA}[i] Choose an item number (or 0 to go back):\n> ")
            )
            if choice == 0:
                return
            if 1 <= choice <= len(item_list):
                recipe = item_list[choice - 1]
                player.house.craft_item(recipe)
            else:
                print(f"{C.RED}[x] Invalid item number!")
        except ValueError:
            print(f"{C.RED}[x] Please enter a valid number!")

        input(PRESS_ENTER)

    def garden(self, player):  # TODO
        pass

    def sleep(self, player):
        clear_screen()
        print(f"{C.MAG}Dormir")
        hours = input(f"{C.WHI}Quantas horas você deseja dormir?\n> ")
        try:
            hours = int(hours)
            if hours > 0:
                player.house.sleep(hours)
            else:
                print(f"{C.RED}[x] Horas inválidas!")
        except ValueError:
            print(f"{C.RED}[x] Entrada inválida!")
        input(PRESS_ENTER)
