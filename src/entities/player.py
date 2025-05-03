from src.utils.codex import ROOMS, ITEM
from src.utils.core import (
    PRESS_ENTER,
    clear_screen,
    type_text,
    title_text,
    option_text,
    progress_bar,
    chance,
    C,
)
from time import sleep
from random import choice


class Player:
    def __init__(self, name):
        self.name = name  # Player name
        self.level = 1  # Player level
        self.xp = 0  # Player experience points

        self.days = 0  # Count of days in game
        self.hours = 0  # Count of hours in game

        self.location = 0  # Actual location

        self.coins = 100  # Balance
        self.attributes = {"STR": 5, "AGI": 5, "VIT": 5, "INT": 5}  # Attributes

        self.hp_max = self.attributes["VIT"] * 10  # Max HP
        self.hp = self.hp_max  # Health Points
        self.mp_max = self.attributes["INT"] * 10  # Max MP
        self.mp = self.mp_max  # Mana Points
        self.df = 0  # Defense

        self.inventory = {}  # Player inventory / {Item.ID: item, "qnt"}

        self.equipment = {  # Player equipped items
            "weapon": None,
            "armor": None,
            "accessory": [None, None],
        }
        self.abilities = {}  # Player habilities

    # Combat methods
    def take_damage(self, damage):
        df = 0
        if self.equipment["armor"] is not None:
            df = self.equipment["armor"]["effect"]["dfc"]
        if self.equipment["accessory"][0] is not None:
            if "dfc" in self.equipment["accessory"][0]["effect"]:
                df += self.equipment["accessory"][0]["effect"]["dfc"]
        if self.equipment["accessory"][1] is not None:
            if "dfc" in self.equipment["accessory"][1]["effect"]:
                df += self.equipment["accessory"][1]["effect"]["dfc"]

        dmg = max(damage - (self.df + df), 0)
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return dmg

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def restore_mp(self, amount):
        self.mp += amount
        if self.mp > self.mp_max:
            self.mp = self.mp_max

    # Miscellaneous methods
    def pass_time(self, hours):
        self.hours += hours
        if self.hours >= 24:
            self.days += self.hours // 24
            self.hours = self.hours % 24
        if self.hours < 0:
            self.days -= abs(self.hours) // 24
            self.hours = 24 - abs(self.hours) % 24

    def travel(self):  # TODO: List cities and time to travel
        pass

    def sleep(self, hours):

        self.hp_max = self.attributes["VIT"] * 5
        self.mp_max = self.attributes["INT"] * 10

        try:
            time = int(hours)
        except ValueError:
            print(f"{C.RED}[x] Invalid input.")
            return
        if time <= 0:
            print(f"{C.RED}[x] Invalid sleep hours.")
            return
        if time > 24:
            print(f"{C.RED}[x] You can't sleep more than 24 hours.")
            return
        self.pass_time(time)
        self.hp += time * self.attributes["VIT"] * 2
        self.mp += time * self.attributes["INT"] * 2
        if self.hp > self.hp_max:
            self.hp = self.hp_max
        if self.mp > self.mp_max:
            self.mp = self.mp_max
        for i in range(time):
            print(f"{C.BLU}⏳ Sleeping... {C.RESET}", end="\r")
            sleep(1)
        input(PRESS_ENTER)

    # Add methods
    def add_xp(self, amount):
        self.xp += amount
        print(f"{self.name} gained {amount}xp")
        while self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1
            self.attributes["STR"] += 1
            self.attributes["AGI"] += 1
            self.attributes["VIT"] += 2
            self.attributes["INT"] += 1

            self.hp_max = self.attributes["VIT"] * 5
            self.mp_max = self.attributes["INT"] * 10

            # Atualizar HP e MP mantendo a proporção
            if self.hp > 0 and self.hp_max > 0:
                hp_ratio = self.hp / self.hp_max
                self.hp = int(self.hp_max * hp_ratio)
            else:
                self.hp = self.hp_max

            if self.mp > 0 and self.mp_max > 0:
                mp_ratio = self.mp / self.mp_max
                self.mp = int(self.mp_max * mp_ratio)
            else:
                self.mp = self.mp_max

            print(f"⭐ {self.name} leveled up to level {self.level}!")

    def add_coin(self, amount):
        self.coins += amount
        print(f"{self.name} gained {amount}c")

    def add_item(self, item_id, quantity=1):
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity

    def remove_item(self, item_id, quantity=1):
        if item_id in self.inventory:
            self.inventory[item_id] -= quantity
            if self.inventory[item_id] <= 0:
                del self.inventory[item_id]

    # List methods
    def list_abilities(self):
        i = 0
        for ability in self.abilities.items():
            if "dmg" in ability:
                print(
                    f"{C.BLU}  {ability} - Dano: {ability['dmg']} | {ability['cost']} MP"
                )
            elif "heal" in ability:
                print(
                    f"{C.BLU}  {ability} - Cura: {ability['heal']} | {ability['cost']} MP"
                )
            else:
                print(
                    f"{C.BLU}  {ability} - {ability['xp']}/{ability['xp_max']} | {ability['cost']} MP"
                )
            i += 1
        if i == 0:
            print(f"{C.RED}  Nenhuma habilidade aprendida.")
        print(f"{C.RESET}")

    def show_inventory(self, use=False):
        category = ["potion", "weapon", "armor", "item", "accessory"]
        clear_screen()
        title_text("Inventory")
        print(f"{C.BLA}  Balance: {C.GRE}{self.coins}c")

        # Exibir itens
        for x in category:
            self.list_items(x)

        if use and self.inventory:
            while True:
                print(f"{C.BLA}Would you like to use an item?")
                option_text("Y", "Yes")
                option_text("N", "No")
                opt = input(f"{C.BLA}Choose an option:\n{C.WHI}> {C.BLA}")
                clear_screen()
                if opt.lower() == "y" or opt.lower() == "yes" or opt == "1":
                    title_text("Inventory")
                    print()
                    for i, x in enumerate(category, 1):
                        option_text(i, x.capitalize())
                    opt = input(f"\n{C.BLA}Choose a category:\n{C.WHI}> {C.BLA}")
                    if opt == "0" or opt == "":
                        return
                    opt = int(opt)
                    if opt <= 5:
                        opt -= 1
                        item_list = self.list_items(category[opt], True)
                        i_index = input(
                            f"{C.BLA}{category[opt].capitalize()} number:\n{C.WHI}> {C.BLA}"
                        )
                        if i_index == "" or i_index == None:
                            return
                        try:
                            item_list = list(item_list.keys())
                            i_index = int(i_index) - 1
                            if 0 <= i_index < len(item_list):
                                i_selected = item_list[i_index - 1]
                                clear_screen()
                                if category[opt] == "potion" or category[opt] == "item":
                                    self.use_item(i_selected, player=self)
                                    return
                                elif category[opt] == "weapon":
                                    self.equip_weapon(i_selected)
                                    return
                                elif category[opt] == "armor":
                                    self.equip_armor(i_selected)
                                    return
                            else:
                                print(f"{C.RED}[x] Invalid {category[opt]} number.")
                                sleep(1)
                        except ValueError:
                            print(f"{C.RED}[x] Invalid input.")
                            sleep(1)
                    else:
                        print(f"{C.RED}[x] Invalid category!")
                        sleep(1)
                elif (
                    opt.lower() == "n" or opt.lower() == "no" or opt == "0" or opt == ""
                ):
                    print(f"{C.BLU}[i] Exiting inventory...")
                    sleep(0.5)
                    return
                else:
                    print(f"{C.RED}[x] Invalid option!")
                    continue
        input(PRESS_ENTER)

    def list_items(self, category, iterate=False):
        if not self.inventory:
            return
        item_list = {
            item_id: quantity
            for i, (item_id, quantity) in enumerate(self.inventory.items(), start=1)
            if ITEM[item_id].type == category
        }
        if not item_list:
            return
        print(f"{C.WHI}{C.BOL}{category.capitalize()}:{C.RESET}")
        if iterate:
            for i, (item_id, quantity) in enumerate(item_list.items(), 1):
                option_text(i, f"  {ITEM[item_id].name} (x{quantity})")
                return item_list
        else:
            for item_id, quantity in item_list.items():
                print(f"  {ITEM[item_id]} (x{quantity})")

    # Equip methods
    def equip_weapon(self, id):
        if id in self.inventory:
            self.unequip_weapon()
            self.equipment["weapon"] = id
            self.remove_item(id)
            print(f"{C.BLA}{C.FAD}{ITEM[id].name} {C.RESET}{C.BLA}equipped")
            sleep(1)

    def equip_armor(self, armor_id):
        if armor_id in self.inventory:
            self.unequip_armor()
            self.equipment["armor"] = armor_id
            self.remove_item(armor_id)
            print(f"{C.BLA}{C.FAD}{ITEM[armor_id].name} {C.RESET}{C.BLA}equipped")
            sleep(1)

    def equip_accessory(self, accessory):
        if accessory.name in self.inventory:
            for i in range(2):
                if self.equipment["accessory"][i] is None:
                    self.equipment["accessory"][i] = accessory
                    self.inventory["accessory"].remove(accessory)

    # Unequip methods
    def unequip_weapon(self):
        if self.equipment["weapon"] is not None:
            self.add_item(self.equipment["weapon"])
            print(f"{self.name} removeu {self.equipment['weapon']}.")
            self.equipment["weapon"] = None
        # else:
        #     print(f"{Colors.RED}[x] Nenhuma arma equipada.")

    def unequip_armor(self):
        if self.equipment["armor"] is not None:
            self.inventory["armors"].append(self.equipment["armor"])
            print(f"{self.name} removeu {self.equipment['armor']}.")
            self.equipment["armor"] = None
        # else:
        #     print(f"{Colors.RED}[x] Nenhuma armadura equipada.")

    def unequip_accessory(self, accessory):
        if accessory in self.equipment["accessory"]:
            self.inventory["accessory"].append(accessory)
            print(f"{self.name} removeu {accessory}.")
            for i in range(2):
                if self.equipment["accessory"][i] == accessory:
                    self.equipment["accessory"][i] = None
                    return
        # else:
        #     print(f"{Colors.RED}[x] Acessório não encontrado na mochila.")

    # Use methods
    def use_item(self, item_id, enemy=None, player=None):
        if item_id in self.inventory:
            item = ITEM[item_id]
            if item.type == "potion":
                if item.effect == "hp":
                    self.heal(item.mod)
                    print(
                        f"{C.BLA}{self.name} used {item.name} and healed {C.RED}{item.mod} {C.BLA}HP!"
                    )
                elif item.effect == "mp":
                    self.restore_mp(item.mod)
                    print(
                        f"{C.BLA}{self.name} used {item.name} and restored {C.CYA}{item.mod} {C.BLA}MP!"
                    )
                self.inventory[item_id] -= 1
                if self.inventory[item_id] <= 0:
                    del self.inventory[item_id]
            elif item.type == "item":
                if "dmg" in item.effect and enemy:
                    enemy.take_damage(item.effect["dmg"])
                    print(
                        f"{self.name} used {item.name} and dealt {item.effect['dmg']} damage to {enemy.name}!"
                    )
                elif "heal" in item.effect and player:
                    player.heal(item.effect["heal"])
                    print(
                        f"{self.name} used {item.name} and healed {item.effect['heal']} HP!"
                    )
                self.inventory[item_id] -= 1
                if self.inventory[item_id] <= 0:
                    del self.inventory[item_id]
        else:
            print(f"{C.RED}[x] {self.name} doesn't have this item!")

    # Dict method
    def to_dict(self):
        data = {
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "days": self.days,
            "hours": self.hours,
            "location": self.location,
            "coins": self.coins,
            "attributes": self.attributes,
            "hp_max": self.hp_max,
            "hp": self.hp,
            "mp_max": self.mp_max,
            "mp": self.mp,
            "df": self.df,
            "inventory": self.inventory,  # Directly store the new inventory model
            "equipment": {
                "weapon": (
                    self.equipment["weapon"] if self.equipment["weapon"] else None
                ),
                "armor": (self.equipment["armor"] if self.equipment["armor"] else None),
                "accessory": [
                    accessory.id if accessory else None
                    for accessory in self.equipment["accessory"]
                ],
            },
            "abilities": self.abilities,
        }
        if hasattr(self, "house") and not isinstance(self.house, dict):
            data["house"] = self.house.to_dict()
        return data

    # Boolean check methods
    def is_alive(self):
        return self.hp > 0

    def game_over(self):
        clear_screen()
        type_text("Game Over!", color=C.RED)
        sleep(1)
        type_text(f"Você perdeu todas as suas moedas!", color=C.RED)

    # Class methods
    @classmethod
    def from_dict(cls, data):
        player = cls(data["name"])
        if "house" in data:

            player.house = House.from_dict(data["house"], player)
        player.__dict__.update(data)
        return player

    def __str__(self):
        clear_screen()
        title_text(self.name)
        # Formatar equipamento
        weapon = (
            f"{C.WHI}{C.FAD}{ITEM[self.equipment['weapon']].name} {C.RESET}{C.BLA}[{C.WHI}{ITEM[self.equipment['weapon']].damage} DMG{C.RESET}{C.BLA}]{C.RESET}"
            if self.equipment["weapon"]
            else f"{C.BLA}{C.FAD}None{C.RESET}"
        )
        armor = (
            f"{C.WHI}{C.FAD}{ITEM[self.equipment['armor']].name} {C.RESET}{C.BLA}[{C.WHI}{ITEM[self.equipment['weapon']].damage} DEF{C.RESET}{C.BLA}]{C.RESET}"
            if self.equipment["armor"]
            else f"{C.BLA}{C.FAD}None{C.RESET}"
        )
        accessory = []
        for i in self.equipment.get(
            "accessory", [None, None]
        ):  # Use get() with a default
            if i:
                accessory.append(
                    f"{i} (Efeito: {', '.join([f'{i.mod} {i.effect.capitalize()}'])})"
                )
            else:
                accessory.append(f"{C.BLA}{C.FAD}None{C.RESET}")

        return (
            # HP e MP
            f"{C.RED}HP{C.WHI}: [{C.RED}{self.hp}{C.WHI}/{C.RED}{self.hp_max}{C.WHI}] {C.RESET}| {C.CYA}MP{C.WHI}: [{C.CYA}{self.mp}{C.WHI}/{C.CYA}{self.mp_max}{C.WHI}]\n"
            f"{C.YEL}Lv{C.WHI}. {C.YEL}{self.level} {C.WHI}[{C.YEL}{self.xp}{C.WHI}/{C.YEL}{self.level * 100}{C.WHI}] {C.RESET}| {C.GRE}₵{self.coins}\n"
            f"{C.BLU}Attributes{C.WHI}:\n"
            f"  {C.BLU}STR{C.WHI}: {C.BLU}{self.attributes['STR']}  {C.BLU}AGI{C.WHI}: {C.BLU}{self.attributes['AGI']}  "
            f"{C.BLU}VIT{C.WHI}: {C.BLU}{self.attributes['VIT']}  {C.BLU}INT{C.WHI}: {C.BLU}{self.attributes['INT']}{C.RESET}\n"
            f"Equipped{C.BLA}:{C.RESET}\n"
            f"  Weapon: {weapon}\n"
            f"  Armor: {armor}\n"
            f"  Accessories:\n"
            f"    1. {accessory[0]}\n"
            f"    2. {accessory[1]}\n"
            f"{C.RESET}"
        )


class House:
    def __init__(self, owner, location=None):
        self.owner = owner
        self.location = location
        self.level = 1
        self.rooms = {}
        self.recipes = {
            1: {},  # Potions
            2: {},  # Crafting
        }

    def add_room(self, room):
        if room not in ROOMS:
            print(f"{C.RED}[x] Invalid room!")
            return

        if room in self.rooms:
            print(f"{C.RED}[x] You already have this room!")
            return

        self.rooms[room] = {
            "name": ROOMS[room]["name"],
            "level": 1,
            "facilities": ROOMS[room]["facilities"],
        }
        print(f"{C.GRE}✨ {ROOMS[room]['name']} added to your house!")
        return

    def add_recipe(self, room, recipe):
        if room not in self.rooms:
            print(f"{C.RED}[x] Invalid room!")
            return

        # self.recipes[recipe] = RECIPES[recipe]
        print(f"{C.GRE}✨ {recipe['name']} added to your recipes!")

    def upgrade_room(self, room):
        if room not in self.rooms:
            print(f"{C.RED}[x] Invalid room!")
            return False

        cost = (
            ROOMS[room]["cost"] * 1.5
            if self.rooms[room]["level"] == 1
            else ROOMS[room]["cost"] * self.rooms[room]["level"]
        )
        if self.owner.coins < cost:
            print(f"{C.RED}[x] You don't have enough coins!")
            sleep(1)
            return False

        self.owner.coins -= cost

        self.rooms[room]["level"] += 1
        progress_bar((self.rooms[room]["level"] * 5), delay=0.15, length=50)
        print(
            f"{C.GRE}\n✨ {room.capitalize()}  leveled up to level {self.rooms[room]['level']}!"
        )
        return True

    # Crafting functions
    def brew_potion(self, recipe_name):
        if recipe_name not in self.recipes["potions"]:
            print(f"{C.RED}[x] Receita não encontrada!")
            return False

        recipe = self.recipes["potions"][recipe_name]
        # Verificar ingredientes
        for ingredient in recipe["ingredients"]:
            if not any(
                item["name"] == ingredient for item in self.owner.inventory["items"]
            ):
                print(f"{C.RED}[x] Você não tem {ingredient}!")
                return False

        # Remover ingredientes
        for ingredient in recipe["ingredients"]:
            for item in self.owner.inventory["items"]:
                if item["name"] == ingredient:
                    self.owner.inventory["items"].remove(item)
                    break

        # Adicionar poção
        self.owner.add_item(recipe["result"], "potions")
        print(f"{C.GRE}✨ Você preparou {recipe_name}!")
        return True

    def craft_item(self, recipe_name):
        if not self.facilities["workbench"]:
            print(f"{C.RED}[x] Você precisa de uma bancada para criar itens!")
            return False

        if recipe_name not in self.recipes["crafting"]:
            print(f"{C.RED}[x] Receita não encontrada!")
            return False

        recipe = self.recipes["crafting"][recipe_name]
        # Verificar ingredientes
        for ingredient in recipe["ingredients"]:
            if not any(
                item["name"] == ingredient for item in self.owner.inventory["items"]
            ):
                print(f"{C.RED}[x] Você não tem {ingredient}!")
                return False

        # Remover ingredientes
        for ingredient in recipe["ingredients"]:
            for item in self.owner.inventory["items"]:
                if item["name"] == ingredient:
                    self.owner.inventory["items"].remove(item)
                    break

        # Adicionar item
        self.owner.add_item(recipe["result"], recipe["result"]["type"])
        print(f"{C.GRE}✨ Você criou {recipe_name}!")
        return True

    # House functions
    def sleep(self, hours):
        if not self.facilities["bed"]:
            print(f"{C.RED}[x] Você precisa de uma cama para dormir!")
            return False

        # Bônus de recuperação baseado no nível do quarto
        recovery_multiplier = 1 + (self.rooms["bedroom"] * 0.2)
        hp_recovery = int(10 * hours * recovery_multiplier)
        mp_recovery = int(5 * hours * recovery_multiplier)

        self.owner.heal(hp_recovery)
        self.owner.restore_mp(mp_recovery)
        self.owner.pass_time(hours)

        print(
            f"{C.GRE}💤 Você dormiu por {hours} horas e recuperou {hp_recovery} HP e {mp_recovery} MP!"
        )
        return True

    def garden_harvest(self):
        if not self.facilities["herb_garden"]:
            print(f"{C.RED}[x] Você precisa de um jardim para colher ervas!")
            return False

        # Chance de colher baseada no nível do jardim
        harvest_chance = 20 + (self.rooms["garden"] * 10)
        if chance() > (100 - harvest_chance):
            herbs = ["Erva Medicinal", "Cristal Azul", "Minério de Ferro", "Couro"]
            herb = choice(herbs)
            self.owner.add_item({"name": herb, "type": "items"}, "items")
            print(f"{C.GRE}🌱 Você colheu {herb} do seu jardim!")
            return True
        else:
            print(f"{C.YEL}🌱 Nada está pronto para colher...")
            return False

    def show_status(self):
        clear_screen()
        title_text("Your House")
        print(f"\n{C.CYA}Rooms:")
        for room, level in self.rooms.items():
            print(f"{C.WHI}  {room.title()}: {C.BLA}Lv. {level}{C.RESET}")
        input(PRESS_ENTER)

    def to_dict(self):
        return {
            "level": self.level,
            "rooms": self.rooms,
            "facilities": self.facilities,
            "recipes": self.recipes,
        }

    def has_room(self, room):
        return True if room in self.rooms else False

    @classmethod
    def from_dict(cls, data, owner):
        house = cls(owner)
        house.level = data["level"]
        house.rooms = data["rooms"]
        house.recipes = data["recipes"]
        return house


class Room:
    def __init__(self, name, cost, description, id):
        self.name = name
        self.cost = cost
        self.desc = description
        self.id = id

    def __str__(self):
        return f"{C.BLA}{self.name}"
