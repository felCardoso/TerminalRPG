from src.utils import roll_check
from random import randint


class Enemy:
    def __init__(self, name, hp, attack, xp_reward, coin_reward, defense=0, agility=0):
        self.name = name
        self.attack = attack  # Base attack value
        self.defense = defense  # Base defense value
        self.agility = agility  # Base agility value
        self.hp = roll_check(hp, 2)
        self.xp_reward = roll_check(xp_reward, 5)
        self.coin_reward = roll_check(coin_reward, 5)
        self.is_boss = False
        self.item_reward = None

    def set_item(self, items):
        if roll_check(sides=100) > 90:
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
        self.xp_reward = roll_check(xp_reward * 5, 10)  # Bosses give more XP
        self.coin_reward = roll_check(coin_reward * 5, 10)  # Bosses give more coins
        self.item_reward = []  # Bosses can drop multiple items
        self.is_boss = True  # Mark as a boss enemy

    def set_item(self, items):
        if roll_check(sides=100) >= 30:
            item = items[randint(0, len(items) - 1)]
            if item not in self.item_reward:
                self.item_reward.append(item)
            else:
                item = items[randint(0, len(items) - 1)]
                self.item_reward.append(item)
        elif roll_check(sides=100) > 50:
            # Bosses can drop multiple items
            for _ in range(2):
                item = items[randint(0, len(items) - 1)]
                if item not in self.item_reward:
                    self.item_reward.append(item)
                else:
                    item = items[randint(0, len(items) - 1)]
                    self.item_reward.append(item)
        elif roll_check(sides=100) > 70:
            for _ in range(3):
                item = items[randint(0, len(items) - 1)]
                if item not in self.item_reward:
                    self.item_reward.append(item)
                else:
                    item = items[randint(0, len(items) - 1)]
                    self.item_reward.append(item)

    def show_status(self):
        print(
            f"{self.name} (BOSS) | HP: {self.hp} | ATK: {self.attack} | DEF: {self.defense}"
        )


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
        if self.boss:
            self.boss = None

    # Boolean methods to check if the dungeon is empty or has a boss
    def has_boss(self) -> bool:
        return self.boss is not None

    def is_empty(self) -> bool:
        return len(self.enemies) == 0

    # Method to get the first enemy in the list
    def get_enemy(self, index=0):
        if index == 0 and self.enemies:
            return self.enemies[randint(0, len(self.enemies) - 1)]
        elif index < len(self.enemies):
            return self.enemies[index]
        elif index >= len(self.enemies):
            return None


DUNGEON_LEVELS = {
    1: Dungeon("Caverna Sombria", 1),
    2: Dungeon("Floresta Proibida", 2),
    3: Dungeon("Montanha Congelada", 3),
    4: Dungeon("Templo Antigo", 4),
    5: Dungeon("Castelo Abandonado", 5),
}

# Name, HP, ATK, XP, COINS, DEFENSE, AGILITY
DUNGEON_ENEMIES = {
    1: [  # Caverna Sombria - Monstros básicos e mortos-vivos
        Enemy("Goblin", 20, 3, 10, 5, 0),
        Enemy("Esqueleto", 25, 4, 15, 10, 0),
        Enemy("Zumbi", 30, 5, 20, 15, 2),
        Enemy("Morcego Gigante", 15, 4, 12, 8, 0, 10),
        Enemy("Aranha Venenosa", 18, 5, 15, 10, 1, 5),
        Boss("Troll Sombrio", 50, 10, 50, 20, 5),
    ],
    2: [  # Floresta Proibida - Criaturas da natureza e humanoides
        Enemy("Lobo Selvagem", 36, 5, 18, 9, 0),
        Enemy("Orc", 45, 7, 27, 18, 0),
        Enemy("Aranha Gigante", 54, 9, 36, 27, 4),
        Enemy("Ent", 63, 11, 45, 36, 9),
        Enemy("Fada Maligna", 54, 14, 45, 36, 0, 18),
        Boss("High Elf", 90, 18, 90, 36, 9),
    ],
    3: [  # Montanha Congelada - Criaturas do gelo e elementais
        Enemy("Lobo da Neve", 65, 9, 32, 16, 0),
        Enemy("Golem de Gelo", 81, 13, 49, 29, 7),
        Enemy("Fada Sombria", 97, 16, 65, 49, 0, 32),
        Enemy("Yeti", 113, 20, 81, 65, 14),
        Enemy("Elemental de Gelo", 81, 25, 81, 65, 9, 9),
        Boss("Dragão de Gelo", 162, 32, 162, 65, 16),
    ],
    4: [  # Templo Antigo - Criaturas místicas e guardiões
        Enemy("Múmia", 117, 16, 58, 29, 18, 9),
        Enemy("Gato Fantasma", 146, 45, 90, 58, 18, 144),
        Enemy("Esqueleto Dourado", 175, 54, 117, 90, 36, 9),
        Enemy("Guardião do Templo", 204, 45, 126, 108, 27, 18),
        Enemy("Faraó Amaldiçoado", 233, 54, 144, 126, 36, 9),
        Boss("Anúbis", 292, 63, 270, 180, 45),
    ],
    5: [  # Castelo Abandonado - Criaturas sombrias e nobres caídos
        Enemy("Cavaleiro Negro", 210, 72, 180, 144, 54, 18),
        Enemy("Vampiro", 252, 81, 216, 180, 36, 36),
        Enemy("Banshee", 168, 90, 198, 162, 27, 45),
        Enemy("Lich", 315, 99, 234, 198, 45, 27),
        Boss("Rei Caído", 540, 144, 540, 360, 72),
    ],
}

# Itens por dungeon e suas chances de drop
DUNGEON_ITEMS = {
    1: [  # Caverna Sombria - Itens básicos
        {
            "name": "Poção de Vida",
            "type": "potions",
            "effect": {"heal": 50},
            "price": 20,
            "chance": 30,
        },
        {
            "name": "Poção de Mana",
            "type": "potions",
            "effect": {"mp": 30},
            "price": 25,
            "chance": 20,
        },
        {
            "name": "Bomba",
            "type": "items",
            "effect": {"dmg": 20},
            "price": 30,
            "chance": 15,
        },
        {
            "name": "Espada de Ferro",
            "type": "weapons",
            "effect": {"dmg": 10},
            "price": 50,
            "chance": 10,
            "rarity": "comum",
        },
        {
            "name": "Armadura de Couro",
            "type": "armors",
            "effect": {"dfc": 5},
            "price": 40,
            "chance": 10,
            "rarity": "comum",
        },
    ],
    2: [  # Floresta Proibida - Itens naturais
        {
            "name": "Poção de Vida Grande",
            "type": "potions",
            "effect": {"heal": 100},
            "price": 40,
            "chance": 25,
        },
        {
            "name": "Poção de Mana Grande",
            "type": "potions",
            "effect": {"mp": 60},
            "price": 45,
            "chance": 20,
        },
        {
            "name": "Bomba Explosiva",
            "type": "items",
            "effect": {"dmg": 40},
            "price": 50,
            "chance": 15,
        },
        {
            "name": "Espada de Aço",
            "type": "weapons",
            "effect": {"dmg": 20},
            "price": 100,
            "chance": 8,
            "rarity": "comum",
        },
        {
            "name": "Armadura de Aço",
            "type": "armors",
            "effect": {"dfc": 10},
            "price": 80,
            "chance": 8,
            "rarity": "comum",
        },
        {
            "name": "Arco Élfico",
            "type": "weapons",
            "effect": {"dmg": 25},
            "price": 150,
            "chance": 5,
            "rarity": "raro",
        },
    ],
    3: [  # Montanha Congelada - Itens congelados
        {
            "name": "Poção de Vida Suprema",
            "type": "potions",
            "effect": {"heal": 200},
            "price": 80,
            "chance": 20,
        },
        {
            "name": "Poção de Mana Suprema",
            "type": "potions",
            "effect": {"mp": 120},
            "price": 85,
            "chance": 15,
        },
        {
            "name": "Bomba Atômica",
            "type": "items",
            "effect": {"dmg": 80},
            "price": 100,
            "chance": 10,
        },
        {
            "name": "Espada de Gelo",
            "type": "weapons",
            "effect": {"dmg": 35},
            "price": 200,
            "chance": 6,
            "rarity": "comum",
        },
        {
            "name": "Armadura de Gelo",
            "type": "armors",
            "effect": {"dfc": 20},
            "price": 160,
            "chance": 6,
            "rarity": "comum",
        },
        {
            "name": "Cajado do Inverno",
            "type": "weapons",
            "effect": {"dmg": 40, "mp": 50},
            "price": 300,
            "chance": 3,
            "rarity": "raro",
        },
    ],
    4: [  # Templo Antigo - Itens místicos
        {
            "name": "Poção de Vida Divina",
            "type": "potions",
            "effect": {"heal": 400},
            "price": 160,
            "chance": 15,
        },
        {
            "name": "Poção de Mana Divina",
            "type": "potions",
            "effect": {"mp": 240},
            "price": 170,
            "chance": 10,
        },
        {
            "name": "Bomba Sagrada",
            "type": "items",
            "effect": {"dmg": 160},
            "price": 200,
            "chance": 8,
        },
        {
            "name": "Espada Sagrada",
            "type": "weapons",
            "effect": {"dmg": 50},
            "price": 400,
            "chance": 4,
            "rarity": "comum",
        },
        {
            "name": "Armadura Sagrada",
            "type": "armors",
            "effect": {"dfc": 30},
            "price": 320,
            "chance": 4,
            "rarity": "comum",
        },
        {
            "name": "Cajado do Faraó",
            "type": "weapons",
            "effect": {"dmg": 60, "mp": 100},
            "price": 600,
            "chance": 2,
            "rarity": "raro",
        },
    ],
    5: [  # Castelo Abandonado - Itens sombrios
        {
            "name": "Poção de Vida Sombria",
            "type": "potions",
            "effect": {"heal": 800},
            "price": 320,
            "chance": 10,
        },
        {
            "name": "Poção de Mana Sombria",
            "type": "potions",
            "effect": {"mp": 480},
            "price": 340,
            "chance": 8,
        },
        {
            "name": "Bomba Sombria",
            "type": "items",
            "effect": {"dmg": 320},
            "price": 400,
            "chance": 5,
        },
        {
            "name": "Espada Sombria",
            "type": "weapons",
            "effect": {"dmg": 70},
            "price": 800,
            "chance": 3,
            "rarity": "comum",
        },
        {
            "name": "Armadura Sombria",
            "type": "armors",
            "effect": {"dfc": 40},
            "price": 640,
            "chance": 3,
            "rarity": "comum",
        },
        {
            "name": "Cajado do Rei Caído",
            "type": "weapons",
            "effect": {"dmg": 80, "mp": 200},
            "price": 1200,
            "chance": 1,
            "rarity": "raro",
        },
    ],
}

# Drops lendários dos chefes
BOSS_LEGENDARY_ITEMS = {
    1: [  # Troll Sombrio
        {
            "name": "Martelo do Troll",
            "type": "weapons",
            "effect": {"dmg": 30, "stun": 20},
            "price": 1000,
            "chance": 5,
            "rarity": "lendário",
        },
        {
            "name": "Pele do Troll",
            "type": "armors",
            "effect": {"dfc": 15, "hp": 50},
            "price": 800,
            "chance": 5,
            "rarity": "lendário",
        },
    ],
    2: [  # High Elf
        {
            "name": "Arco Élfico Sagrado",
            "type": "weapons",
            "effect": {"dmg": 40, "agi": 20},
            "price": 2000,
            "chance": 5,
            "rarity": "lendário",
        },
        {
            "name": "Armadura Élfica",
            "type": "armors",
            "effect": {"dfc": 20, "mp": 100},
            "price": 1600,
            "chance": 5,
            "rarity": "lendário",
        },
    ],
    3: [  # Dragão de Gelo
        {
            "name": "Espada de Gelo Eterna",
            "type": "weapons",
            "effect": {"dmg": 60, "freeze": 30},
            "price": 4000,
            "chance": 5,
            "rarity": "lendário",
        },
        {
            "name": "Escamas do Dragão",
            "type": "armors",
            "effect": {"dfc": 30, "hp": 200},
            "price": 3200,
            "chance": 5,
            "rarity": "lendário",
        },
    ],
    4: [  # Anúbis
        {
            "name": "Cajado de Anúbis",
            "type": "weapons",
            "effect": {"dmg": 80, "mp": 300, "curse": 40},
            "price": 8000,
            "chance": 5,
            "rarity": "lendário",
        },
        {
            "name": "Máscara de Anúbis",
            "type": "armors",
            "effect": {"dfc": 40, "mp": 400},
            "price": 6400,
            "chance": 5,
            "rarity": "lendário",
        },
    ],
    5: [  # Rei Caído
        {
            "name": "Espada do Rei Caído",
            "type": "weapons",
            "effect": {"dmg": 100, "dark": 50},
            "price": 16000,
            "chance": 5,
            "rarity": "lendário",
        },
        {
            "name": "Coroa do Rei Caído",
            "type": "armors",
            "effect": {"dfc": 50, "hp": 500, "mp": 500},
            "price": 12800,
            "chance": 5,
            "rarity": "lendário",
        },
    ],
}

# Chance base de encontrar um item ao explorar
BASE_ITEM_CHANCE = 20  # 20% de chance base

# Chance de encontrar itens raros
RARE_ITEM_CHANCE = 10  # 10% de chance de encontrar item raro

# Chance de encontrar itens épicos
EPIC_ITEM_CHANCE = 5  # 5% de chance de encontrar item épico

# Chance de encontrar itens lendários
LEGENDARY_ITEM_CHANCE = 1  # 1% de chance de encontrar item lendário
