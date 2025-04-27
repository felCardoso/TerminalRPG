from src.utils import ABILITIES, C, clear_screen, type_text, title_text, option_text
from time import sleep


class Player:
    def __init__(self, name):
        self.name = name  # Player name
        self.level = 1  # Player level
        self.xp = 0  # Player experience points

        self.days = 0  # Count of days in game
        self.hours = 0  # Count of hours in game

        self.local = "Starting Town"  # Actual location

        self.coins = 100  # Balance
        self.attributes = {"STR": 5, "AGI": 5, "VIT": 5, "INT": 5}  # Attributes

        self.hp_max = self.attributes["VIT"] * 10  # Max HP
        self.hp = self.hp_max  # Health Points
        self.mp_max = self.attributes["INT"] * 10  # Max MP
        self.mp = self.mp_max  # Mana Points
        self.df = 0  # Defence

        self.inventory = {  # Player inventory
            "items": [],
            "weapons": [],
            "armors": [],
            "potions": [],
        }

        self.equipment = {  # Player equipped items
            "weapon": None,
            "armor": None,
            "accessories": [None, None],
        }
        self.abilities = {}  # Player habilities

    # Combat methods
    def take_damage(self, damage):
        df = 0
        if self.equipment["armor"] is not None:
            df = self.equipment["armor"]["effect"]["dfc"]
        if self.equipment["accessories"][0] is not None:
            if "dfc" in self.equipment["accessories"][0]["effect"]:
                df += self.equipment["accessories"][0]["effect"]["dfc"]
        if self.equipment["accessories"][1] is not None:
            if "dfc" in self.equipment["accessories"][1]["effect"]:
                df += self.equipment["accessories"][1]["effect"]["dfc"]

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
            print(f"{C.BLUL}⏳ Sleeping... {C.RESET}", end="\r")
            sleep(1)
        input(f"{C.BLUL}[i] Pressione Enter para continuar")

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

    def add_item(self, item, category):
        if category not in self.inventory:
            print(f"{C.RED}[x] Invalid category.")
            return
        if category == "weapons":
            self.inventory["weapons"].append(item)
        elif category == "armors":
            self.inventory["armors"].append(item)
        elif category == "potions":
            self.inventory["potions"].append(item)
        elif category == "items":
            self.inventory["items"].append(item)

    def add_ability(self, ability):
        if ability not in self.abilities:
            self.abilities[ability] = ABILITIES[ability]
            self.abilities[ability]["lvl"] = 1
            self.abilities[ability]["xp"] = 0
            self.abilities[ability]["xp_max"] = 100
            self.abilities[ability]["lvl_max"] = 10
            print(f"{self.name} learned {ability}!")
        else:
            self.abilities[ability]["xp"] += 50
            print(f"{self.name} ganhou 50xp em {ability}.")

    # List methods
    def list_abilities(self):
        i = 0
        for ability in self.abilities.items():
            if "dmg" in ability:
                print(
                    f"{C.BLUL}  {ability} - Dano: {ability['dmg']} | {ability['cost']} MP"
                )
            elif "heal" in ability:
                print(
                    f"{C.BLUL}  {ability} - Cura: {ability['heal']} | {ability['cost']} MP"
                )
            else:
                print(
                    f"{C.BLUL}  {ability} - {ability['xp']}/{ability['xp_max']} | {ability['cost']} MP"
                )
            i += 1
        if i == 0:
            print(f"{C.RED}  Nenhuma habilidade aprendida.")
        print(f"{C.RESET}")

    def show_inventory(self, use=False):
        clear_screen()
        title_text("Inventory")
        print(f"{C.BLA}  Balance: {C.GRE}{self.coins}c\n")

        self.list_potions()  # Exibir poções
        self.list_items()  # Exibir itens
        self.list_weapons()  # Exibir armas
        self.list_armor()  # Exibir armaduras

        print(f"{C.WHI}------------------")

        if use:

            opt = input(
                f"\n{C.BLA}Would you like to use an item? (y/n):\n{C.WHI}> {C.BLA}"
            )
            clear_screen()
            if (
                opt.lower() == "y"
                or opt.lower() == "yes"
                or opt.lower() == "s"
                or opt == "1"
            ):
                title_text("Inventory")
                print()
                option_text(1, "Potions")
                option_text(2, "Items")
                option_text(3, "Weapons")
                option_text(4, "Armor")
                category = int(input(f"\n{C.BLA}Choose a category:\n{C.WHI}> {C.BLA}"))

                if category == 0:
                    return
                elif category == 1:
                    self.list_potions()
                    item_index = int(
                        input(
                            f"\n{C.BLA}Choose a potion by its number:\n{C.WHI}> {C.BLA}"
                        )
                    )
                    try:
                        item_index = int(item_index) - 1
                        if 0 <= item_index < len(self.inventory["potions"]):
                            selected_item = self.inventory["potions"][item_index]
                            self.use_item(selected_item, player=self)
                        else:
                            print(f"{C.RED}[x] Invalid potion number.")
                    except ValueError:
                        print(f"{C.RED}[x] Invalid input.")
                elif category == 2:
                    self.list_items()
                    item_index = int(
                        input(
                            f"\n{C.BLA}Choose an item by its number:\n{C.WHI}> {C.BLA}"
                        )
                    )
                    try:
                        item_index = int(item_index) - 1
                        if 0 <= item_index < len(self.inventory["items"]):
                            selected_item = self.inventory["items"][item_index]
                            self.use_item(selected_item, player=self)
                        else:
                            print(f"{C.RED}[x] Invalid item number.")
                    except ValueError:
                        print(f"{C.RED}[x] Invalid input.")
                elif category == 3:
                    self.list_weapons()
                    item_index = int(
                        input(
                            f"\n{C.BLA}Choose a weapon by its number:\n{C.WHI}> {C.BLA}"
                        )
                    )
                    try:
                        item_index = int(item_index) - 1
                        if 0 <= item_index < len(self.inventory["weapons"]):
                            selected_item = self.inventory["weapons"][item_index]
                            self.equip_weapon(selected_item)
                        else:
                            print(f"{C.RED}[x] Invalid weapon number.")
                    except ValueError:
                        print(f"{C.RED}[x] Invalid input.")
                elif category == 4:
                    self.list_armor()
                    item_index = int(
                        input(
                            f"\n{C.BLA}Choose an armor by its number:\n{C.WHI}> {C.BLA}"
                        )
                    )
                    try:
                        item_index = int(item_index) - 1
                        if 0 <= item_index < len(self.inventory["armors"]):
                            selected_item = self.inventory["armors"][item_index]
                            self.equip_armor(selected_item)
                        else:
                            print(f"{C.RED}[x] Invalid armor number.")
                    except ValueError:
                        print(f"{C.RED}[x] Invalid input.")
                elif category == 5:
                    self.list_accessories()
                    item_index = int(
                        input(
                            f"\n{C.BLA}Choose an accessory by its number:\n{C.WHI}> {C.BLA}"
                        )
                    )
                    try:
                        item_index = int(item_index) - 1
                        if 0 <= item_index < len(self.inventory["accessories"]):
                            selected_item = self.inventory["accessories"][item_index]
                            self.equip_accessory(selected_item)
                        else:
                            print(f"{C.RED}[x] Invalid accessory number.")
                    except ValueError:
                        print(f"{C.RED}[x] Invalid input.")
                else:
                    print(f"{C.RED}[x] Invalid category!")
            elif opt.lower() == "n" or opt.lower() == "no":
                print(f"{C.GRE}Exiting inventory...")
                sleep(1)
                return
            else:
                print(f"{C.RED}[x] Invalid option!")
        print(f"{C.RESET}")

    def list_potions(self):
        print(f"{C.WHI}  Potions:")
        potion_counts = {}
        if not self.inventory["potions"]:
            print(f"{C.RESET}{C.FAD}    Empty{C.RESET}")
        for potion in self.inventory["potions"]:
            potion_counts[potion["name"]] = potion_counts.get(potion["name"], 0) + 1
        for name, count in potion_counts.items():
            print(f"    {name} x{count}")

    def list_items(self):
        print(f"{C.GRE}  Items:")
        item_counts = {}
        if not self.inventory["items"]:
            print(f"{C.RESET}{C.FAD}    Empty{C.RESET}")
        for item in self.inventory["items"]:
            item_counts[item["name"]] = item_counts.get(item["name"], 0) + 1
        for name, count in item_counts.items():
            print(f"    {name} x{count}")

    def list_weapons(self):
        print(f"{C.MAG}  Weapons:")
        weapon_counts = {}
        if not self.inventory["weapons"]:
            print(f"{C.RESET}{C.FAD}    Empty{C.RESET}")
        for weapon in self.inventory["weapons"]:
            weapon_counts[weapon["name"]] = weapon_counts.get(weapon["name"], 0) + 1
        for name, count in weapon_counts.items():
            print(f"    {name} x{count}")

    def list_armor(self):
        print(f"{C.CYA}  Armors:")
        armor_counts = {}
        if not self.inventory["armors"]:
            print(f"{C.RESET}{C.FAD}    Empty{C.RESET}")
        for armor in self.inventory["armors"]:
            armor_counts[armor["name"]] = armor_counts.get(armor["name"], 0) + 1
        for name, count in armor_counts.items():
            print(f"    {name} x{count}")

    def list_accessories(self):
        print(f"{C.BLUL}  Accessories:")
        accessory_counts = {}
        if not self.inventory["accessories"]:
            print(f"{C.RESET}{C.FAD}    Empty{C.RESET}")
        for accessory in self.inventory["accessories"]:
            accessory_counts[accessory["name"]] = (
                accessory_counts.get(accessory["name"], 0) + 1
            )
        for name, count in accessory_counts.items():
            print(f"    {name} x{count}")

    # Equip methods
    def equip_weapon(self, weapon):
        if weapon in self.inventory["weapons"]:
            self.unequip_weapon()
            self.equipment["weapon"] = weapon
            self.inventory["weapons"].remove(weapon)
            print(f"{self.name} equipou {weapon}.")
        else:
            print(f"{C.RED}[x] Arma não encontrada na mochila.")

    def equip_armor(self, armor):
        if armor in self.inventory["armors"]:
            self.unequip_armor()
            self.equipment["armor"] = armor
            self.inventory["armors"].remove(armor)
            print(f"{self.name} equipou {armor}.")
        else:
            print(f"{C.RED}[x] Armadura não encontrada na mochila.")

    def equip_accessory(self, accessory):
        if accessory in self.inventory["accessories"]:
            for i in range(2):
                if self.equipment["accessories"][i] is None:
                    self.equipment["accessories"][i] = accessory
                    self.inventory["accessories"].remove(accessory)
                    print(f"{self.name} equipou {accessory}.")
                    return
            print(f"{C.RED}[x] Não há espaço para mais acessórios.")
        else:
            print(f"{C.RED}[x] Acessório não encontrado na mochila.")

    # Unequip methods
    def unequip_weapon(self):
        if self.equipment["weapon"] is not None:
            self.inventory["weapons"].append(self.equipment["weapon"])
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
        if accessory in self.equipment["accessories"]:
            self.inventory["accessories"].append(accessory)
            print(f"{self.name} removeu {accessory}.")
            for i in range(2):
                if self.equipment["accessories"][i] == accessory:
                    self.equipment["accessories"][i] = None
                    return
        # else:
        #     print(f"{Colors.RED}[x] Acessório não encontrado na mochila.")

    # Use methods
    def use_item(self, item, enemy=None, player=None):
        if item in self.inventory["potions"]:
            if "heal" in item["effect"]:
                self.heal(item["effect"]["heal"])
                print(
                    f"{self.name} usou {item['name']} e curou {item['effect']['heal']} HP!"
                )
            elif "mp" in item["effect"]:
                self.restore_mp(item["effect"]["mp"])
                print(
                    f"{self.name} usou {item['name']} e restaurou {item['effect']['mp']} MP!"
                )
            self.inventory["potions"].remove(item)
        elif item in self.inventory["items"]:
            if "dmg" in item["effect"] and enemy:
                enemy.take_damage(item["effect"]["dmg"])
                print(
                    f"{self.name} usou {item['name']} e causou {item['effect']['dmg']} de dano em {enemy.name}!"
                )
            elif "heal" in item["effect"] and player:
                player.heal(item["effect"]["heal"])
                print(
                    f"{self.name} usou {item['name']} e curou {item['effect']['heal']} HP!"
                )
            self.inventory["items"].remove(item)

    # Dict method
    def to_dict(self):
        data = self.__dict__.copy()
        if hasattr(self, "house") and not isinstance(self.house, dict):
            data["house"] = self.house.to_dict()
        return data

    # Boolean check methods
    def is_alive(self):
        return self.hp > 0

    def has_weapon(self) -> bool:
        return self.equipment["weapon"] is not None

    def has_armor(self) -> bool:
        return self.equipment["armor"] is not None

    def has_accessory(self) -> bool:
        return (
            self.equipment["accessories"][0] is not None
            or self.equipment["accessories"][1] is not None
        )

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
            from src.house import House

            player.house = House.from_dict(data["house"], player)
        player.__dict__.update(data)
        return player

    def __str__(self):
        clear_screen()
        title_text("Player Status")

        # Formatar equipamento
        weapon = (
            f"{self.equipment['weapon']['name']} (Dano: {self.equipment['weapon']['effect']['dmg']})"
            if self.equipment["weapon"]
            else "None"
        )
        armor = (
            f"{self.equipment['armor']['name']} [Defesa: {self.equipment['armor']['effect']['dfc']}]"
            if self.equipment["armor"]
            else "None"
        )
        accessories = []
        for accessory in self.equipment["accessories"]:
            if accessory:
                accessories.append(
                    f"{accessory['name']} (Efeito: {', '.join([f'{k}: {v}' for k, v in accessory['effect'].items()])})"
                )
            else:
                accessories.append("None")

        return (
            f"{C.CYA}👤 Name: {self.name} {C.RESET}| {C.RED}HP: [{self.hp}/{self.hp_max}]\n"
            f"{C.YEL}⭐ Level: {self.level} {C.RESET}| {C.YEL}EXP: {self.xp}/{self.level * 100}\n"
            f"{C.GRE}💰 Money: {self.coins}c\n"
            f"{C.BLU}📊 Attributes:\n"
            f"  STR: {self.attributes['STR']}  AGI: {self.attributes['AGI']}  "
            f"VIT: {self.attributes['VIT']}  INT: {self.attributes['INT']}\n"
            f"{C.WHI}🛡 Equipped:\n"
            f"  Weapon: {weapon}\n"
            f"  Armor: {armor}\n"
            f"  Accessories:\n"
            f"    1. {accessories[0]}\n"
            f"    2. {accessories[1]}\n"
            f"{C.RESET}"
        )
