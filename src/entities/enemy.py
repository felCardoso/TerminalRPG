# from src.utils.codex import ITEM
from src.utils.core import chance
from random import randint


class Enemy:
    def __init__(self, name, hp, atk, xp_rwd, coi_rwd, dfs=0, agi=0):
        self.name = name
        self.attack = atk  # Base attack value
        self.defense = dfs  # Base defense value
        self.agility = agi
        self.hp = chance(hp, int(hp * 0.35))
        self.xp_reward = chance(xp_rwd, int(xp_rwd * 0.5))
        self.coin_reward = chance(coi_rwd, int(coi_rwd * 0.5))
        self.is_boss = False
        self.item_reward = []

    def set_item(self, items):
        if chance(sides=100) > 90:
            self.item_reward = items[randint(0, len(items) - 1)]
        else:
            self.item_reward = None

    def take_damage(self, damage):
        dmg = max(damage - self.defense, 0)
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return dmg

    def is_alive(self) -> bool:
        return self.hp > 0


class Boss(Enemy):
    def __init__(self, name, hp, attack: int, xp_reward, coin_reward, defense=0):
        super().__init__(name, hp, attack, xp_reward, coin_reward, defense)
        self.is_boss = True  # Mark as a boss enemy

    def set_item(self, items):
        pass

    def show_status(self):
        print(
            f"{self.name} (BOSS) | HP: {self.hp} | ATK: {self.attack} | DEF: {self.defense}"
        )
