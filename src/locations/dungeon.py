from src.utils.core import chance


class Dungeon:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.enemies = []
        self.boss = None
        self.items = []
        self.traps = []
        self.events = []
        self.difficulty = 1

    # Add methods to manage enemies
    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def add_boss(self, boss):
        self.boss = boss

    # Remove methods to manage enemies
    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def remove_boss(self):
        """Remove o boss da masmorra"""
        self.boss = None

    # Boolean methods to check if the dungeon is empty or has a boss
    def has_boss(self) -> bool:
        return self.boss is not None

    def is_empty(self) -> bool:
        return len(self.enemies) == 0

    # Method to get the first enemy in the list
    def get_enemy(self, index=0):
        from random import randint

        if index == 0 and self.enemies:
            return self.enemies[randint(0, len(self.enemies) - 1)]
        elif index < len(self.enemies):
            return self.enemies[index]
        elif index >= len(self.enemies):
            if self.enemies == []:
                return
