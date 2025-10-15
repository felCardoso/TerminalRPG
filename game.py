from src.utils.codex import DUNGEON, CITY
from src.utils.menu import (
    MainMenu,
    AdventureMenu,
    CitySelectMenu,
    CityMenu,
    GuildMenu,
    ShopSelectMenu,
    ShopMenu,
    DungeonSelectMenu,
    HouseMenu,
)
from src.utils.core import (
    SaveManager,
    DungeonManager,
    C,
    # show_intro,
    clear_screen,
    type_text,
    progress_bar,
    X,
)
from src.entities.player import Player, House
from time import sleep
import json

sm = SaveManager()


class Game:
    def __init__(self):
        self.menu = MainMenu(self)
        self.slot_file = None

    def run(self):
        # show_intro()
        self.menu.run()

    def new_game(self):
        def validate_name():
            name = False
            while not name:
                name = input(f"{C.BLA}Enter your character's name:\n{C.WHI}> {C.BLA}")
                if name:
                    return name

        clear_screen()
        self.slot_file = sm.select_slot(new=True)
        if self.slot_file:
            clear_screen()
            name = validate_name()
            player = Player(name)
            sm.save(player, self.slot_file)
            self.adventure_menu(player, self.slot_file)

    def continue_game(self):
        clear_screen()
        self.slot_file = sm.select_slot(new=False)
        if self.slot_file:
            try:
                data = sm.load(self.slot_file)
                player = Player.from_dict(data)
                self.adventure_menu(player, self.slot_file)
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
        if self.slot_file:
            sm.save(player, self.slot_file)
        else:
            sm.save(player, slot_file)

    # MENUS

    def adventure_menu(self, player, slot_file=None):
        if not slot_file:
            menu = AdventureMenu(self, player, self.slot_file)
        else:
            menu = AdventureMenu(self, player, slot_file)
        menu.run()

    def cityselect_menu(self, player):
        menu = CitySelectMenu(self, player)
        menu.run()

    def city_menu(self, player):
        menu = CityMenu(self, player)
        menu.run()

    def guild_menu(self, player):
        from src.locations.world import Guild

        if player.guild:
            menu = GuildMenu(self, player)
            menu.run()
        else:
            if player.level >= 5:
                player.guild = Guild(name="Adventurer's Guild", player=player)
            else:
                input(f"{X} {C.RED}You need to be at least level 5 to join the Guild")

    def shopselect_menu(self, player):
        menu = ShopSelectMenu(self, player)
        menu.run()

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

    def travel(self, player, id, opt):
        def pass_time(x, travel_time):
            print(
                f"{C.BLU}You started your journey to {C.CYA}{x.name}{C.BLU}.\nThis will take {int(travel_time / 24)} days."
            )
            player.pass_time(travel_time)
            progress_bar(travel_time * 24)
            clear_screen()
            type_text(f"You arrived at {x.name}!", C.GRE)

        if opt == "c":
            if id in CITY:
                city = CITY[id]
                travel_time = int(abs((city.level * 2) - player.location))
                pass_time(city, travel_time)
                player.location = id
                sleep(0.5)
                self.adventure_menu(player, slot_file=self.slot_file)
        elif opt == "d":
            if id in DUNGEON:
                dungeon = DUNGEON[id]
                travel_time = int(abs((dungeon.level * 2) - player.location))
                pass_time(dungeon, travel_time)
                dm = DungeonManager(self, dungeon, player)
                dm.start()
                sleep(0.5)


if __name__ == "__main__":
    Game().run()
