from src.menus import MainMenu, AdventureMenu, DungeonMenu, HouseMenu, DungeonsMenu
from src.enemy import (
    Enemy,
    Boss,
    DUNGEON_LEVELS,
    DUNGEON_ENEMIES,
    DUNGEON_ITEMS,
)
from src.utils import (
    C,
    SaveManager,
    clear_screen,
    show_intro,
    type_text,
    title_text,
    roll_check,
    gen_shop,
    progress_bar,
    INVALID_CHOICE,
    PRESS_ENTER,
)
from src.player import Player
from src.house import House
from src.fight import Fight
from time import sleep
import json

sm = SaveManager()


class Game:
    def __init__(self):
        self.main_menu = MainMenu(self)

    def run(self):
        # show_intro()
        self.main_menu.run(menu=True)

    def new_game(self):
        clear_screen()
        slot = sm.select_slot(new=True)
        clear_screen()
        name = self.validate_name()
        player = Player(name)
        if slot:
            sm.save(player, slot)
            self.start_adventure(player, slot)

    def validate_name(self):
        name = False
        while not name:
            name = input(f"\n{C.BLA}Enter your character's name:\n{C.WHI}> {C.BLA}")
            if name : return name

    def continue_game(self):
        clear_screen()
        slot = sm.select_slot(new=False)
        if slot:
            try:
                data = sm.load(slot)
                player = Player.from_dict(data)
                self.start_adventure(player, slot)
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

    def start_adventure(self, player, slot_file):
        adventure_menu = AdventureMenu(self, player, slot_file)
        adventure_menu.run()

    def explore_dungeon(self, player):
        dungeons_menu = DungeonsMenu(self, player)
        dungeons_menu.run(True)

    def travel_dungeon(self, player, level):
        if level and level in DUNGEON_LEVELS:
            dungeon = DUNGEON_LEVELS[level]
            travel_time = int(dungeon.level * 48)  # 2 days per level
            clear_screen()
            print(
                f"{C.BLUL}You started your journey to {C.CYA}{dungeon.name}{C.BLUL}. This will take {int(travel_time / 24)} days."
            )
            player.pass_time(travel_time)

            # Create progress bar
            progress_bar(travel_time)
            clear_screen()
            type_text(f"\nYou arrived at {dungeon.name}!", C.GRE)
            sleep(1)

            self.start_dungeon(player, dungeon)

    def start_dungeon(self, player, dungeon):
        clear_screen()
        type_text(f"Entering {dungeon.name}...", C.MAG)
        sleep(1)

        # Create new enemies for the dungeon based on level
        dungeon.enemies = []
        for enemy in DUNGEON_ENEMIES[dungeon.level]:
            if isinstance(enemy, Boss):
                dungeon.boss = Boss(
                    enemy.name,
                    enemy.hp,
                    enemy.attack,
                    enemy.xp_reward,
                    enemy.coin_reward,
                    enemy.defense,
                )
                # Add legendary drops to the boss
                chance = roll_check(mod=0, sides=100)
                if chance == 1:
                    legendary_items = [
                        item
                        for item in DUNGEON_ITEMS[dungeon.level]
                        if item.get("rarity") == "legendary"
                    ]
                    if legendary_items:
                        dungeon.boss.set_item(legendary_items)
                elif chance <= 10:
                    epic_items = [
                        item
                        for item in DUNGEON_ITEMS[dungeon.level]
                        if item.get("rarity") == "epic"
                    ]
                    if epic_items:
                        dungeon.boss.set_item(epic_items)
                elif chance <= 20:
                    rare_items = [
                        item
                        for item in DUNGEON_ITEMS[dungeon.level]
                        if item.get("rarity") == "rare"
                    ]
                    if rare_items:
                        dungeon.boss.set_item(rare_items)
                elif chance <= 50:
                    common_items = [
                        item
                        for item in DUNGEON_ITEMS[dungeon.level]
                        if item.get("rarity") == "common"
                    ]
                    if common_items:
                        dungeon.boss.set_item(common_items)
            else:
                chance = roll_check(sides=3)
                if chance == 1:
                    for i in range(1):
                        dungeon.enemies.append(
                            Enemy(
                                enemy.name,
                                enemy.hp,
                                enemy.attack,
                                enemy.xp_reward,
                                enemy.coin_reward,
                                enemy.defense,
                                enemy.agility,
                            )
                        )
                        i += 1
                elif chance == 2:
                    dungeon.enemies.append(
                        Enemy(
                            enemy.name,
                            enemy.hp,
                            enemy.attack,
                            enemy.xp_reward,
                            enemy.coin_reward,
                            enemy.defense,
                            enemy.agility,
                        )
                    )

        # Check if dungeon is empty
        if not dungeon.enemies and not dungeon.has_boss():
            print(f"{C.YEL}⚠️ This dungeon is empty!")
            sleep(1)
            return

        dungeon_menu = DungeonMenu(self, player, dungeon)
        dungeon_menu.run()

    def explore_dungeon_area(self, player, dungeon):
        # Chance to find enemy or boss
        roll = roll_check(mod=0, sides=100)
        input(f"{C.WHI}Chance: {C.BLA}{roll}")
        if roll >= 75:  # 25% Chance to find an enemy
            if dungeon.has_boss() and roll >= 95:
                print(f"{C.RED}⚠️ You found the dungeon boss!")
                sleep(1)
                fight = Fight()
                fight.start(player, dungeon.boss)
                if not player.is_alive():
                    player.game_over()
                if not dungeon.boss.is_alive():
                    print(f"{C.MAG}🎉 You defeated the boss of {dungeon.name}!")
                    # Check legendary drops
                    if dungeon.boss.item_reward:
                        for item in dungeon.boss.item_reward:
                            print(
                                f"{C.MAG}✨ You found a legendary item: {item['name']}!"
                            )
                            player.add_item(item, item["type"])
                    sleep(1)
                    dungeon.remove_boss()
            else:
                enemy = dungeon.get_enemy()
                if enemy:
                    fight = Fight()
                    fight.start(player, enemy)
                    if not player.is_alive():
                        player.game_over()
                    if not enemy.is_alive():
                        dungeon.remove_enemy(enemy)
        elif roll >= 60:  # 15% Chance to find an item
            chance = roll_check(sides=100)
            if chance > (95):  # 5% EPIC
                items = [
                    item
                    for item in DUNGEON_ITEMS[dungeon.level]
                    if item.get("rarity") == "epic"
                ]
            elif chance > (80):  # 15% RARE
                items = [
                    item
                    for item in DUNGEON_ITEMS[dungeon.level]
                    if item.get("rarity") == "rare"
                ]
            else:  # 80% COMMON
                items = [
                    item
                    for item in DUNGEON_ITEMS[dungeon.level]
                    if item.get("rarity") != "common"
                ]

            # Calculate total drop chance
            total_chance = sum(item["chance"] for item in items)

            # Verificar se há itens disponíveis e se total_chance é maior que 0
            if items and total_chance > 0:
                roll = roll_check(mod=0, sides=total_chance)

                # Find item based on chance
                current_chance = 0
                for item in items:
                    current_chance += item["chance"]
                    if roll <= current_chance:
                        print(f"{C.GRE}🎁 You found an item: {item['name']}!")
                        if item.get("rarity") == "rare":
                            print(f"{C.MAG}✨ It's a rare item!")
                        player.add_item(item, item["type"])
                        break
                sleep(1)
            else:
                print(f"{C.GRE}You explored the area and found nothing...")
                sleep(1)
        # elif roll >= 50: # TODO: 10% Chance to ???
        else:
            print(f"{C.GRE}You explored the area and found nothing...")
            sleep(1)

    def shop_menu(self, player):
        clear_screen()
        shop_items = gen_shop()

        while True:
            # Display shop header
            title_text("Shop")

            # Organize items by category
            items_by_category = {
                "potions": [],
                "weapons": [],
                "armors": [],
                "items": [],
            }
            for item in shop_items:
                items_by_category[item["type"]].append(item)

            # Display items
            i = 1
            item_indices = []
            for category in ["potions", "weapons", "armors", "items"]:
                if not items_by_category[category]:
                    continue

                print(f"\n{C.CYA}{C.NEG}{category.capitalize()}:{C.RESET}")
                for item in items_by_category[category]:
                    item_indices.append(shop_items.index(item))

                    # Determine rarity color
                    rarity_color = C.WHI
                    if item.get("rarity") == "rare":
                        rarity_color = C.GRE
                    elif item.get("rarity") == "epic":
                        rarity_color = C.MAG
                    elif item.get("rarity") == "legendary":
                        rarity_color = C.YEL

                    # Display item
                    status = (
                        f"- {C.BLA}{item['price']}c"
                        if item.get("available", True)
                        else f"- {C.REDL}SOLD OUT"
                    )
                    print(
                        f"{C.WHI}[{C.BLA}{i}{C.WHI}]{C.RESET} {rarity_color}{item['name']} {C.RESET}{status}"
                    )
                    i += 1

            # Exit option
            print(f"\n{C.WHI}[{C.BLA}{0}{C.WHI}] {C.BLA}Exit")
            print(f"\n{C.BLA}Available coins: {C.GRE}{player.coins}c")
            print(f"\n{C.BLUL}Press [Enter] to exit")
            choice = input("\nChoose an item to buy (number):\n> ")

            # Exit shop
            if choice == "0" or choice == "":
                clear_screen()
                type_text("Thanks for visiting the shop!", C.GRE)
                sleep(1)
                break

            # Process choice
            try:
                choice = int(choice)
                if not (1 <= choice <= len(item_indices)):
                    print()
                    continue

                item_index = item_indices[choice - 1]
                item = shop_items[item_index]

                if not item.get("available", True):
                    print(f"{C.RED}[x] This item is sold out!")
                elif player.coins < item["price"]:
                    print(f"{C.RED}[x] You don't have enough coins!")
                else:
                    player.coins -= item["price"]
                    player.add_item(item, item["type"])
                    item["available"] = False
                    print(f"{C.GRE}You bought {item['name']}!")

                    if item.get("rarity") == "rare":
                        print(f"{C.MAG}✨ It's a rare item!")
                    elif item.get("rarity") == "epic":
                        print(f"{C.RED}🔥 It's an epic item!")

            except ValueError:
                print(f"{C.RED}[x] Invalid input!")

            input(f"{C.BLUL}[i] Press Enter to continue.")
            clear_screen()

    def house_menu(self, player):
        if not hasattr(player, "house"):
            player.house = House(player)
        house_menu = HouseMenu(player)
        house_menu.run()

    def save_game(self, player, slot_file):
        sm.save(player, slot_file)

    def exit_menu(self, player, slot_file):
        clear_screen()
        type_text(f"Save before exit?", color=C.CYA)
        i = input(" [y/n]\n>")
        if i.lower() == "y" or i.lower() == "s" or i == "1":
            sm.save(player, slot_file)
        else:
            self.main_menu.run()


if __name__ == "__main__":
    game = Game()
    game.run()
