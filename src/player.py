from colorama import Fore, Style
from src.utils import Colors
import os


class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0

        self.class_type = None
        self.skills = []
        self.money = 100
        self.attributes = {"STR": 5, "AGI": 5, "VIT": 5, "INT": 5}

        self.hp_max = self.attributes["VIT"] * 10
        self.hp = self.hp_max
        self.mp_max = self.attributes["INT"] * 10
        self.mp = self.mp_max

        self.inventory = {
            "items": [],
            "weapons": [],
            "armors": [],
            "potions": [],
        }

        self.equipment = {
            "weapon": None,
            "armor": None,
            "accessories": [None, None],
        }
        self.affinity = {
            "sword": 0,
            "shield": 0,
            "magic": 0,
            "summon": 0,
            "bow": 0,
        }

    def use_action(self, action):
        if action in self.affinity:
            self.affinity[action] += 1
            print(f"{self.name} used {action}! Affinity increased.")
        else:
            print("Invalid action.")

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} gained {amount} EXP.")
        while self.exp >= self.level * 100:
            self.exp -= self.level * 100
            self.level += 1
            self.attributes["STR"] += 1
            self.attributes["AGI"] += 1
            self.attributes["VIT"] += 2
            self.attributes["INT"] += 1
            print(f"⭐ {self.name} leveled up to level {self.level}!")

    def gain_money(self, amount):
        self.money += amount
        print(f"{self.name} gained {amount} G. Total: {self.money} G.")

    def check_class(self):
        most_used = max(self.affinity, key=self.affinity.get)
        value = self.affinity[most_used]
        if value < 5:
            print("No combat style defined yet.")
            return
        class_map = {
            "sword": "Swordsman",
            "shield": "Tank",
            "magic": "Mage",
            "summon": "Summoner",
            "bow": "Archer",
        }
        self.class_type = class_map.get(most_used, None)
        print(f"🎉 Class awakened: {self.class_type}!")

    def to_dict(self):
        return self.__dict__

    def is_alive(self):
        return self.hp > 0

    @classmethod
    def from_dict(cls, data):
        player = cls(data["name"])
        player.__dict__.update(data)
        return player

    def __str__(self):
        os.system("cls" if os.name == "nt" else "clear")
        return (
            f"{Colors.CYA}👤 Name: {self.name}\n"
            f"{Colors.YEL}⭐ Level: {self.level} | EXP: {self.exp}/{self.level * 100}\n"
            f"{Colors.MAG}🏹 Class: {self.class_type}\n"
            f"{Colors.GRE}💰 Money: {self.money} G\n"
            f"{Colors.BLU}📊 Attributes:\n"
            f"  STR: {self.attributes['STR']}  AGI: {self.attributes['AGI']}  "
            f"VIT: {self.attributes['VIT']}  INT: {self.attributes['INT']}\n"
            f"{Colors.WHI}🛡 Equipped:\n"
            f"  Weapon: {self.equipment['weapon']}\n"
            f"  Armor: {self.equipment['armor']}\n"
            f"  Accessories: {self.equipment['accessories']}\n"
            f"{Colors.RESET}"
        )
