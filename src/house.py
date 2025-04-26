from src.utils import Colors, clear_screen, type_text, roll_check
from time import sleep
import random


class House:
    def __init__(self, owner):
        self.owner = owner
        self.level = 1
        self.rooms = {"bedroom": 1, "kitchen": 0, "workshop": 0, "garden": 0}
        self.facilities = {
            "bed": True,
            "stove": True,
            "workbench": True,
            "herb_garden": True,
        }
        self.upgrade_costs = {
            "bedroom": 500,
            "kitchen": 500,
            "workshop": 500,
            "garden": 500,
        }
        self.recipes = {
            "potions": {
                "Poção de Vida": {
                    "ingredients": ["Erva Medicinal", "Água Pura"],
                    "result": {
                        "name": "Poção de Vida",
                        "type": "potions",
                        "effect": {"heal": 50},
                        "price": 20,
                    },
                },
                "Poção de Mana": {
                    "ingredients": ["Cristal Azul", "Água Pura"],
                    "result": {
                        "name": "Poção de Mana",
                        "type": "potions",
                        "effect": {"mp": 30},
                        "price": 25,
                    },
                },
            },
            "crafting": {
                "Espada de Ferro": {
                    "ingredients": ["Minério de Ferro", "Madeira"],
                    "result": {
                        "name": "Espada de Ferro",
                        "type": "weapons",
                        "effect": {"dmg": 10},
                        "price": 50,
                    },
                },
                "Armadura de Couro": {
                    "ingredients": ["Couro", "Fio"],
                    "result": {
                        "name": "Armadura de Couro",
                        "type": "armors",
                        "effect": {"dfc": 5},
                        "price": 40,
                    },
                },
            },
        }

    def upgrade_room(self, room):
        if room not in self.rooms:
            print(f"{Colors.RED}[x] Sala inválida!")
            return False

        cost = self.upgrade_costs[room] * self.rooms[room]
        if self.owner.coins < cost:
            print(f"{Colors.RED}[x] Você não tem moedas suficientes!")
            return False

        self.owner.coins -= cost
        self.rooms[room] += 1
        print(
            f"{Colors.GRE}✨ Você melhorou sua {room} para o nível {self.rooms[room]}!"
        )
        return True

    def brew_potion(self, recipe_name):
        if not self.facilities["stove"]:
            print(f"{Colors.RED}[x] Você precisa de um fogão para preparar poções!")
            return False

        if recipe_name not in self.recipes["potions"]:
            print(f"{Colors.RED}[x] Receita não encontrada!")
            return False

        recipe = self.recipes["potions"][recipe_name]
        # Verificar ingredientes
        for ingredient in recipe["ingredients"]:
            if not any(
                item["name"] == ingredient for item in self.owner.inventory["items"]
            ):
                print(f"{Colors.RED}[x] Você não tem {ingredient}!")
                return False

        # Remover ingredientes
        for ingredient in recipe["ingredients"]:
            for item in self.owner.inventory["items"]:
                if item["name"] == ingredient:
                    self.owner.inventory["items"].remove(item)
                    break

        # Adicionar poção
        self.owner.add_item(recipe["result"], "potions")
        print(f"{Colors.GRE}✨ Você preparou {recipe_name}!")
        return True

    def craft_item(self, recipe_name):
        if not self.facilities["workbench"]:
            print(f"{Colors.RED}[x] Você precisa de uma bancada para criar itens!")
            return False

        if recipe_name not in self.recipes["crafting"]:
            print(f"{Colors.RED}[x] Receita não encontrada!")
            return False

        recipe = self.recipes["crafting"][recipe_name]
        # Verificar ingredientes
        for ingredient in recipe["ingredients"]:
            if not any(
                item["name"] == ingredient for item in self.owner.inventory["items"]
            ):
                print(f"{Colors.RED}[x] Você não tem {ingredient}!")
                return False

        # Remover ingredientes
        for ingredient in recipe["ingredients"]:
            for item in self.owner.inventory["items"]:
                if item["name"] == ingredient:
                    self.owner.inventory["items"].remove(item)
                    break

        # Adicionar item
        self.owner.add_item(recipe["result"], recipe["result"]["type"])
        print(f"{Colors.GRE}✨ Você criou {recipe_name}!")
        return True

    def sleep(self, hours):
        if not self.facilities["bed"]:
            print(f"{Colors.RED}[x] Você precisa de uma cama para dormir!")
            return False

        # Bônus de recuperação baseado no nível do quarto
        recovery_multiplier = 1 + (self.rooms["bedroom"] * 0.2)
        hp_recovery = int(10 * hours * recovery_multiplier)
        mp_recovery = int(5 * hours * recovery_multiplier)

        self.owner.heal(hp_recovery)
        self.owner.restore_mp(mp_recovery)
        self.owner.pass_time(hours)

        print(
            f"{Colors.GRE}💤 Você dormiu por {hours} horas e recuperou {hp_recovery} HP e {mp_recovery} MP!"
        )
        return True

    def garden_harvest(self):
        if not self.facilities["herb_garden"]:
            print(f"{Colors.RED}[x] Você precisa de um jardim para colher ervas!")
            return False

        # Chance de colher baseada no nível do jardim
        harvest_chance = 20 + (self.rooms["garden"] * 10)
        if roll_check() > (100 - harvest_chance):
            herbs = ["Erva Medicinal", "Cristal Azul", "Minério de Ferro", "Couro"]
            herb = random.choice(herbs)
            self.owner.add_item({"name": herb, "type": "items"}, "items")
            print(f"{Colors.GRE}🌱 Você colheu {herb} do seu jardim!")
            return True
        else:
            print(f"{Colors.YEL}🌱 Nada está pronto para colher...")
            return False

    def show_status(self):
        clear_screen()
        print(f"{Colors.MAG}===== Sua Casa =====")
        print(f"{Colors.WHI}Nível: {self.level}")
        print(f"\n{Colors.CYA}Salas:")
        for room, level in self.rooms.items():
            print(f"  {room.title()}: Nível {level}")
        print(f"\n{Colors.GRE}Facilidades:")
        for facility, available in self.facilities.items():
            status = "✅" if available else "❌"
            print(f"  {facility.title()}: {status}")
        input(f"\n{Colors.LBLU}[i] Pressione Enter para continuar.")

    def to_dict(self):
        return {"level": self.level, "rooms": self.rooms, "facilities": self.facilities}

    @classmethod
    def from_dict(cls, data, owner):
        house = cls(owner)
        house.level = data["level"]
        house.rooms = data["rooms"]
        house.facilities = data["facilities"]
        return house
