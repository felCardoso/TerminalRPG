from src.utils import (
    C,
    clear_screen,
    type_text,
    title_text,
    roll_check,
    progress_bar,
    PRESS_ENTER,
)
from time import sleep
import random


class House:
    def __init__(self, owner):
        self.owner = owner
        self.level = 1
        self.rooms = {}
        self.recipes = {
            "potions": {},
            "crafting": {},
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

    def add_facility(self, room, facility):
        if room not in self.rooms:
            print(f"{C.RED}[x] Invalid room!")
            return

        self.rooms[room]["facilities"].append(facility)
        print(
            f"{C.GRE}✨ {FACILITIES[facility]['name']} added to {ROOMS[room]['name']}!"
        )

    def add_recipe(self, room, recipe):
        if room not in self.rooms:
            print(f"{C.RED}[x] Invalid room!")
            return

        self.recipes[recipe] = RECIPES[recipe]
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
        if not self.facilities["stove"]:
            print(
                f"{C.RED}[x] You need a {C.WHI}{FACILITIES[2]['name']}{C.RED} to brew potions!"
            )
            return False

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
        if roll_check() > (100 - harvest_chance):
            herbs = ["Erva Medicinal", "Cristal Azul", "Minério de Ferro", "Couro"]
            herb = random.choice(herbs)
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
        print(f"\n{C.GRE}Facilities:")
        for facility, available in self.facilities.items():
            status = "✅" if available else "❌"
            print(f"{C.WHI}  {facility.title()}: {status}")
        input(PRESS_ENTER)

    def to_dict(self):
        return {
            "level": self.level,
            "rooms": self.rooms,
            "facilities": self.facilities,
            "recipes": self.recipes,
        }

    def has_facility(self, room, facility):
        return True if facility in self.rooms[room]["facilities"] else False

    def has_room(self, room):
        return True if room in self.rooms else False

    @classmethod
    def from_dict(cls, data, owner):
        house = cls(owner)
        house.level = data["level"]
        house.rooms = data["rooms"]
        house.facilities = data["facilities"]
        house.recipes = data["recipes"]
        return house


ROOMS = {
    "bedroom": {
        "name": "Bedroom",
        "description": "A place to rest and recover energy",
        "facilities": [1],
        "cost": 100,
    },
    "brewery": {
        "name": "Brewery",
        "description": "A place to brew magical potions",
        "facilities": [2],
        "cost": 200,
    },
    "workshop": {
        "name": "Workshop",
        "description": "A place to craft weapons and armor",
        "facilities": [3],
        "cost": 200,
    },
    "garden": {
        "name": "Garden",
        "description": "A place to grow magical herbs and materials",
        "facilities": [4],
        "cost": 200,
    },
    "laboratory": {
        "name": "Laboratory",
        "description": "A place to study and research new recipes and facilities",
        "facilities": [5],
        "cost": 500,
    },
}

FACILITIES = {
    1: {"name": "Bed", "room": "bedroom", "cost": 100},
    2: {"name": "Brewing Station", "room": "brewery", "cost": 200},
    3: {"name": "Workbench", "room": "workshop", "cost": 200},
    4: {"name": "Garden", "room": "garden", "cost": 200},
    5: {"name": "Research Table", "room": "laboratory", "cost": 500},
}

RECIPES = {
    "potions": {
        1: {
            "ingredients": ["Medicinal Herb", "Pure Water"],
            "result": {
                "name": "Health Potion",
                "type": "potions",
                "effect": {"heal": 50},
                "price": 20,
            },
        },
        2: {
            "ingredients": ["Blue Crystal", "Pure Water"],
            "result": {
                "name": "Mana Potion",
                "type": "potions",
                "effect": {"mp": 30},
                "price": 25,
            },
        },
    },
    "crafting": {
        "Iron Sword": {
            "ingredients": ["Refined Iron", "Wood"],
            "result": {
                "name": "Iron Sword",
                "type": "weapons",
                "effect": {"dmg": 10},
                "price": 50,
            },
        },
        "Leather Armor": {
            "ingredients": ["Leather", "Thread"],
            "result": {
                "name": "Leather Armor",
                "type": "armors",
                "effect": {"dfc": 5},
                "price": 40,
            },
        },
    },
}
