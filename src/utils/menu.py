from src.utils.codex import DUNGEON, CITY, ROOMS, ITEM
from src.utils.core import (
    C,
    clear_screen,
    title_text,
    option_text,
    INVALID_CHOICE,
    PRESS_ENTER,
)
from time import sleep


class BaseMenu:  # Base
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

    def select(self, menu=False):
        while True:
            try:
                choice = input(f"\n{C.BLA}Choose an option:\n{C.WHI}> {C.BLA}")
                if choice == "0" or choice == "":
                    return 0
                choice = int(choice)
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
            choice = self.select(menu)
            if not menu:
                if choice == 0 or choice == "" or choice == None:
                    return
            _, action = self.options[choice - 1]
            action()


class MainMenu(BaseMenu):  # Main Menu
    def __init__(self, game):
        super().__init__(
            "Main Menu",
            [
                ("New Game", game.new_game),
                ("Continue", game.continue_game),
                ("Exit", game.quit_game),
            ],
        )


class AdventureMenu(BaseMenu):  # Adventure Menu
    def __init__(self, game, player, slot_file):
        super().__init__(
            "Adventure",
            [
                (f"{CITY[player.location].name}", lambda: game.city_menu(player)),
                ("Dungeons", lambda: game.dungeonselect_menu(player)),
                ("Player Status", lambda: self.show_status(player)),
                ("Inventory", lambda: player.show_inventory(True)),
                ("House", lambda: game.house_menu(player)),
                ("Save", lambda: game.save_game(player, slot_file)),
                ("Main Menu", lambda: game.exit_menu(player, slot_file)),
            ],
        )

    def show_status(self, player):
        clear_screen()
        print(player)
        sleep(1)
        input(PRESS_ENTER)


class CitySelectMenu(BaseMenu):  # City Selection Menu
    def __init__(self, game, player):
        self.game = game
        available_cities = [
            (
                f"{city.name} {C.WHI}- {C.BLA}Level {city.level} {C.WHI}/ {C.BLA}{(city.level * 2) - player.location} days of travel{C.RESET}",
                lambda c=city, i=i: self.details(player, i),
            )
            for i, city in enumerate(CITY.values())
            if city.level <= player.level
        ]
        super().__init__("Select a City", available_cities + [("Exit", lambda: None)])

    def details(self, player, city_id):
        city = CITY[city_id]
        clear_screen()
        print(f"{C.BLA}City: {C.WHI}{city.name}")
        print(f"{C.BLA}Level: {C.WHI}{city.level}")
        print(f"{C.BLA}Travel Time: {C.WHI}{(city.level * 2) - player.location} days")
        choice = input(
            f"\n{C.WHI}[{C.CYA}i{C.WHI}] Do you want to travel to this city? (y/n){C.BLA}:\n{C.WHI}> {C.BLA}"
        ).lower()
        if choice == "y" or choice == "1":
            self.game.travel(player, city_id)
        else:
            print(f"{C.YEL}[i] Travel canceled.")
        input(PRESS_ENTER)


class CityMenu(BaseMenu):  # City Menu
    def __init__(self, game, player):
        self.city = CITY[player.location]
        super().__init__(
            self.city.name,
            [
                ("Shops", lambda: game.shopselect_menu(player)),
                ("Neighborhood", lambda: self.city.neighborhood),
                ("Guild", lambda: self.city.guild),
                ("Travel", lambda: game.cityselect_menu(player)),
            ],
        )


class ShopSelectMenu(BaseMenu):  # Shop Selection Menu
    def __init__(self, game, player):
        self.city = CITY[player.location]
        super().__init__(
            "Select a Shop",
            [
                (shop.name, lambda s=shop: game.shop_menu(s, player))
                for shop in self.city.shops
            ],
            # + [("Exit", lambda: None)],
        )


class ShopMenu(BaseMenu):  # Shop Menu
    def __init__(self, shop, player):
        self.player = player
        super().__init__(
            "Shop",
            [
                (
                    f"{ITEM[item_id].name} {C.BLA}- {C.GRE}₵{ITEM[item_id].price}{C.RESET}",
                    lambda i=item_id: (self.buy_item(shop, i)),
                )
                for item_id in shop.items
            ]
            + [(f"{C.BLA}Exit", lambda: None)],
        )

    def buy_item(self, shop, item_id):
        item = ITEM[item_id]
        clear_screen()
        print(f"{C.BLA}Item: {C.WHI}{item.name}")
        print(f"{C.BLA}Price: {C.WHI}{item.price}")
        if item.type == "potion":
            print(f"{C.BLA}Effect: {C.WHI}+{item.mod} {item.effect.upper()}")
        elif item.type == "weapon":
            print(f"{C.BLA}Damage: {C.WHI}+{item.damage} DMG")
        elif item.type == "armor":
            print(f"{C.BLA}Defense: {C.WHI}+{item.defense}")

        choice = input(
            f"\n{C.WHI}[{C.CYA}i{C.WHI}] Do you want to buy this item? (y/n){C.BLA}:\n{C.WHI}> {C.BLA}"
        ).lower()
        if choice == "y" or choice == "1":
            if shop.buy(self.player, item_id):
                print(f"{C.GRE}[✓] You bought {ITEM[item_id].name}!")
            else:
                print(f"{C.RED}[x] You don't have enough gold!")
        else:
            print(f"{C.YEL}[i] Purchase canceled.")
        input(PRESS_ENTER)

    def display(self, x=False):
        print(f"{C.WHI}Coins{C.BLA}: {C.GRE}{self.player.coins}¢{C.RESET}")
        super().display(x)


class DungeonSelectMenu(BaseMenu):
    def __init__(self, game, player):
        super().__init__(
            "Dungeons",
            [
                (
                    f"{dungeon.name} {C.BLA}- {C.WHI}Lv. {dungeon.level} {C.BLA}/ {C.WHI}{dungeon.level * 2} days of travel{C.RESET}",
                    lambda d=dungeon: game.travel_dungeon(player, d.level),
                )
                for dungeon in DUNGEON.values()
            ]
            + [("Exit", lambda: None)],
        )


class DungeonInteractMenu(BaseMenu):
    def __init__(self, manager, player, dungeon):
        super().__init__(
            dungeon.name,
            [
                ("Explore", lambda: manager.explore()),
                ("Player Status", lambda: self.show_status(player)),
                ("Inventory", lambda: player.show_inventory(use=True)),
                ("Exit", lambda: manager.exit()),
            ],
        )

    def show_status(self, player):
        clear_screen()
        print(player)
        input(PRESS_ENTER)


class HouseMenu(BaseMenu):
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
            print(f"{C.BLU}[{i}] {recipe}: {ingredients}")

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
