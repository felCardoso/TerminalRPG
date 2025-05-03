from src.utils.item import Potion, Weapon, Armor, Item, Accessory, Ingredient

INGREDIENT = {  # Ingredient ID: Ingredient Object
    0: Ingredient(name="Water", rarity="common", price=5),  # Common Base
    # D - Common Ingredients
    1: Ingredient(name="Sunroot", rarity="common", price=5),  # HP
    2: Ingredient(name="Moonbloom", rarity="common", price=5),  # MP
    3: Ingredient(name="Embermoss", rarity="common", price=5),  # STR
    4: Ingredient(name="Frostleaf", rarity="common", price=5),  # DEF
    5: Ingredient(name="Ghostfern", rarity="common", price=5),  # AGI
    # C - Uncommon Ingredients
    6: Ingredient(name="Glowcap", rarity="uncommon", price=10),  # HP
    7: Ingredient(name="Crystal Shard", rarity="uncommon", price=10),  # MP
    8: Ingredient(name="Iron Herb", rarity="uncommon", price=10),  # STR
    9: Ingredient(name="Blue Herb", rarity="uncommon", price=10),  # DEF
    10: Ingredient(name="Green Herb", rarity="uncommon", price=10),  # AGI
    # B - Rare Ingredients
    11: Ingredient(name="Golden Crystal", rarity="rare", price=20),  # HP
    12: Ingredient(name="Mana Herb", rarity="rare", price=20),  # MP
    13: Ingredient(name="Vital Herb", rarity="rare", price=20),  # STR
    14: Ingredient(name="Lucky Herb", rarity="rare", price=20),  # DEF
    15: Ingredient(name="Swift Herb", rarity="rare", price=20),  # AGI
    # A - Epic Ingredients
    16: Ingredient(name="Diamond Shard", rarity="epic", price=50),  # HP
    17: Ingredient(name="Fire Herb", rarity="epic", price=50),  # MP
    18: Ingredient(name="Ice Herb", rarity="epic", price=50),  # STR
    19: Ingredient(name="Poison Herb", rarity="epic", price=50),  # DEF
    20: Ingredient(name="Lightning Herb", rarity="epic", price=50),  # AGI
    # S - Legendary Ingredients
    21: Ingredient(name="Phoenix Feather", rarity="legendary", price=100),  # HP
    22: Ingredient(name="Storm Crystal", rarity="legendary", price=100),  # MP
    23: Ingredient(name="Moon Crystal", rarity="legendary", price=100),  # STR
    24: Ingredient(name="Celestial Crystal", rarity="legendary", price=100),  # DEF
    25: Ingredient(name="Ethereal Crystal", rarity="legendary", price=100),  # AGI
    100: Ingredient(name="Pure Water", rarity="epic", price=75),  # Epic Base
}

ITEM = {  # Item ID: Item Object
    # Potions
    "P1": Potion(  # D - Minor Health Potion +25 HP
        name="Minor Health Potion",
        rarity="common",
        price=10,
        effect="hp",
        mod=25,
        recipe=True,
        ing=[0, 1],
    ),
    "P2": Potion(  # D - Minor Mana Potion +30 MP
        name="Minor Mana Potion",
        rarity="common",
        price=25,
        effect="mp",
        mod=30,
        recipe=True,
        ing=[0, 2],
    ),
    "P3": Potion(  # D - Basic Strength Potion +5 STR
        name="Basic Strength Potion",
        rarity="common",
        price=35,
        effect="str",
        mod=5,
        recipe=True,
        ing=[0, 3],
    ),
    "P4": Potion(  # D - Basic Resistance Potion +5 DEF
        name="Basic Resistance Potion",
        rarity="common",
        price=35,
        effect="def",
        mod=5,
        recipe=True,
        ing=[0, 4],
    ),
    "P5": Potion(  # D - Basic Agility Potion +5 AGI
        name="Basic Agility Potion",
        rarity="rare",
        price=35,
        effect="agi",
        mod=5,
        recipe=True,
        ing=[0, 5],
    ),
    "P6": Potion(  # C - Healing Potion +40 HP
        name="Healing Potion",
        rarity="uncommon",
        price=50,
        effect="hp",
        mod=40,
        recipe=True,
        ing=[0, 6],
    ),
    "P7": Potion(  # C - Mana Potion +50 MP
        name="Mana Potion",
        rarity="uncommon",
        price=50,
        effect="mp",
        mod=50,
        recipe=True,
        ing=[0, 7],
    ),
    "P8": Potion(  # C - Strength Potion +10 STR
        name="Strength Potion",
        rarity="uncommon",
        price=100,
        effect="str",
        mod=10,
        recipe=True,
        ing=[0, 8],
    ),
    "P9": Potion(  # C - Resistance Potion +10 DEF
        name="Resistance Potion",
        rarity="uncommon",
        price=100,
        effect="def",
        mod=10,
        recipe=True,
        ing=[0, 9],
    ),
    "P10": Potion(  # C - Agility Potion +10 AGI
        name="Agility Potion",
        rarity="uncommon",
        price=100,
        effect="agi",
        mod=10,
        recipe=True,
        ing=[0, 10],
    ),
    "P11": Potion(  # B - Greater Health Potion +80 HP
        name="Greater Health Potion",
        rarity="rare",
        price=150,
        effect="hp",
        mod=80,
        recipe=True,
        ing=[0, 11],
    ),
    "P12": Potion(  # B - Greater Mana Potion +100 MP
        name="Greater Mana Potion",
        rarity="rare",
        price=150,
        effect="hp",
        mod=80,
        recipe=True,
        ing=[0, 12],
    ),
    "P13": Potion(  # B - Greater Strength Potion +15 STR
        name="Great Strength Potion",
        rarity="rare",
        price=200,
        effect="str",
        mod=15,
        recipe=True,
        ing=[0, 13],
    ),
    "P14": Potion(  # B - Greater Resistance Potion +20 DEF
        name="Potion of Invincibility",
        rarity="rare",
        price=220,
        effect="def",
        mod=20,
        recipe=False,
        ing=[0, 14],
    ),
    "P15": Potion(  # B - Greater Agility Potion +20 AGI
        name="Greater Agility Potion",
        rarity="rare",
        price=220,
        effect="spd",
        mod=20,
        recipe=True,
        ing=[0, 15],
    ),
    "P16": Potion(  # A - Life Elixir +150
        name="Life Elixir",
        rarity="epic",
        price=250,
        effect="hp",
        mod=150,
        recipe=True,
        ing=[100, 16],
    ),
    "P17": Potion(  # A - Magic Elixir +200
        name="Magic Elixir",
        rarity="epic",
        price=250,
        effect="mp",
        mod=150,
        recipe=True,
        ing=[100, 17],
    ),
    "P18": Potion(  # A - Berserker's Brew +25 STR
        name="Potion of Poison Resistance",
        rarity="epic",
        price=300,
        effect="str",
        mod=25,
        recipe=True,
        ing=[100, 18],
    ),
    "P19": Potion(  # A - Iron Skin +25 DEF
        name="Potion of Poison Resistance",
        rarity="epic",
        price=300,
        effect="def",
        mod=25,
        recipe=True,
        ing=[100, 19],
    ),
    "P20": Potion(  # A - Speed Tonic +25 AGI
        name="Speed Tonic",
        rarity="epic",
        price=400,
        effect="agi",
        mod=25,
        recipe=True,
        ing=[100, 20],
    ),
    "P21": Potion(  # S - Full Restore Potion +full HP + full MP
        name="Full Restore Potion",
        rarity="legendary",
        price=800,
        effect="fr",
        mod=0,
        recipe=False,
    ),
    "P22": Potion(  # S - TODO
        name="Potion",
        rarity="legendary",
        price=500,
        effect="",
        mod=0,
        recipe=False,
    ),
    "P23": Potion(  # S - Minotaur's Frenesi +50 STR
        name="Minotaur's Frenesi",
        rarity="legendary",
        price=850,
        effect="str",
        mod=50,
        recipe=False,
    ),
    "P24": Potion(  # S - Obsidian Skin +40 DEF
        name="Obsidian Skin",
        rarity="legendary",
        price=850,
        effect="def",
        mod=40,
        recipe=False,
    ),
    "P25": Potion(  # S - Lightning o'Bottle +40 AGI
        name="Lightning o'Bottle",
        rarity="legendary",
        price=850,
        effect="agi",
        mod=40,
        recipe=False,
    ),
    # Weapons
    "W1": Weapon(  # [D] Wooden Sword - 5 DMG
        name="Wooden Sword",
        rarity="common",
        price=20,
        damage=5,
        w_type="sword",
        recipe=True,
        ing=[102, 50],
    ),
    "W2": Weapon(  # [D]
        name="Copper Sword",
        w_type="sword",
        damage=7,
        price=25,
        rarity="common",
        recipe=True,
        ing=[102, 52],
    ),
    "W3": Weapon(  # [D]
        name="Simple Dagger",
        w_type="dagger",
        damage=4,
        price=15,
        rarity="common",
        recipe=True,
        ing=[],
    ),
    "W4": Weapon(  # [D]
        name="Copper Dagger",
        w_type="dagger",
        damage=6,
        price=30,
        rarity="common",
        recipe=True,
        ing=[],
    ),
    "W5": Weapon(  # [D]
        name="Wooden Axe",
        w_type="axe",
        damage=7,
        price=25,
        rarity="common",
        recipe=True,
        ing=[],
    ),
    "W6": Weapon(  # [D]
        name="Iron Axe",
        w_type="axe",
        damage=9,
        price=40,
        rarity="common",
        recipe=True,
        ing=[],
    ),
    "W7": Weapon(  # [D]
        name="Short Bow",
        w_type="bow",
        damage=5,
        price=20,
        rarity="common",
        recipe=True,
        ing=["Wood", "Thread"],
    ),
    "W8": Weapon(  # [D]
        name="Hunting Bow",
        w_type="bow",
        damage=7,
        price=35,
        rarity="common",
        recipe=True,
        ing=["Wood", "Iron Nail"],
    ),
    "W9": Weapon(  # [D]
        name="Wooden Spear",
        w_type="spear",
        damage=6,
        price=30,
        rarity="common",
        recipe=True,
        ing=["Wood", "Iron Nail"],
    ),
    "W10": Weapon(  # [D]
        name="Copper Spear",
        w_type="spear",
        damage=8,
        price=50,
        rarity="common",
        recipe=True,
        ing=["Iron Ingot", "Wood"],
    ),
    "W11": Weapon(  # [C]
        name="Steel Sword",
        w_type="sword",
        damage=12,
        price=80,
        rarity="uncommon",
        recipe=True,
        ing=["Steel Ingot", "Leather Grip"],
    ),
    "W12": Weapon(  # [C]
        name="Sharp Blade",
        w_type="sword",
        damage=14,
        price=100,
        rarity="uncommon",
        recipe=True,
        ing=["Steel Ingot", "Wood"],
    ),
    "W13": Weapon(  # [C]
        name="Steel Dagger",
        w_type="dagger",
        damage=10,
        price=60,
        rarity="uncommon",
        recipe=True,
        ing=["Steel Ingot", "Leather Grip"],
    ),
    "W14": Weapon(  # [C]
        name="Forest Dagger",
        w_type="dagger",
        damage=12,
        price=80,
        rarity="uncommon",
        recipe=True,
        ing=["Poison Crystal", "Steel Ingot"],
    ),
    "W15": Weapon(  # [C]
        name="Battle Axe",
        w_type="axe",
        damage=15,
        price=100,
        rarity="uncommon",
        recipe=True,
        ing=["Steel Ingot", "Wood"],
    ),
    "W16": Weapon(  # [C]
        name="Double-Edged Axe",
        w_type="axe",
        damage=18,
        price=120,
        rarity="uncommon",
        recipe=True,
        ing=["Steel Ingot", "Leather Grip"],
    ),
    "W17": Weapon(  # [C]
        name="Recurve Bow",
        w_type="bow",
        damage=12,
        price=90,
        rarity="uncommon",
        recipe=True,
        ing=["Wood", "Thread"],
    ),
    "W18": Weapon(  # [C]
        name="Long Bow",
        w_type="bow",
        damage=14,
        price=110,
        rarity="uncommon",
        recipe=True,
        ing=["Wood", "Steel Ingot"],
    ),
    "W19": Weapon(  # [C]
        name="Steel Spear",
        w_type="spear",
        damage=13,
        price=100,
        rarity="uncommon",
        recipe=True,
        ing=["Steel Ingot", "Wood"],
    ),
    "W20": Weapon(  # [C]
        name="Piercing Spear",
        w_type="spear",
        damage=16,
        price=120,
        rarity="uncommon",
        recipe=True,
        ing=["Steel Ingot", "Leather Grip"],
    ),
    "W21": Weapon(  # [B]
        name="Ice Sword",
        w_type="sword",
        damage=30,
        price=750,
        rarity="rare",
        recipe=True,
        ing=["Ice Crystal", "Steel Ingot", "Leather Grip"],
    ),
    "W22": Weapon(  # [B]
        name="Flame Sword",
        w_type="sword",
        damage=35,
        price=900,
        rarity="rare",
        recipe=True,
        ing=["Fire Crystal", "Steel Ingot", "Leather Grip"],
    ),
    "W23": Weapon(  # [B]
        name="Ice Dagger",
        w_type="dagger",
        damage=25,
        price=600,
        rarity="rare",
        recipe=True,
        ing=["Dark Crystal", "Steel Ingot"],
    ),
    "W24": Weapon(  # [B]
        name="Venom Dagger",
        w_type="dagger",
        damage=28,
        price=700,
        rarity="rare",
        recipe=True,
        ing=["Poison Crystal", "Steel Ingot"],
    ),
    "W25": Weapon(  # [B]
        name="Thunder Axe",
        w_type="axe",
        damage=35,
        price=800,
        rarity="rare",
        recipe=True,
        ing=["Lightning Crystal", "Steel Ingot", "Wood"],
    ),
    "W26": Weapon(  # [B]
        name="Earthshaker Axe",
        w_type="axe",
        damage=40,
        price=950,
        rarity="rare",
        recipe=True,
        ing=["Earth Crystal", "Steel Ingot", "Wood"],
    ),
    "W27": Weapon(  # [B]
        name="Shadow Bow",
        w_type="bow",
        damage=25,
        price=600,
        rarity="rare",
        recipe=True,
        ing=["Dark Crystal", "Wood", "Thread"],
    ),
    "W28": Weapon(  # [B]
        name="Phoenix Bow",
        w_type="bow",
        damage=30,
        price=750,
        rarity="rare",
        recipe=True,
        ing=["Phoenix Feather", "Wood", "Thread"],
    ),
    "W29": Weapon(  # [B]
        name="Crystal Spear",
        w_type="spear",
        damage=28,
        price=700,
        rarity="rare",
        recipe=True,
        ing=["Crystal Shard", "Steel Ingot"],
    ),
    "W30": Weapon(  # [B]
        name="Lightning Spear",
        w_type="spear",
        damage=32,
        price=850,
        rarity="rare",
        recipe=True,
        ing=["Lightning Crystal", "Steel Ingot"],
    ),
    "W31": Weapon(  # [A]
        name="Dark Sword",
        w_type="sword",
        damage=65,
        price=5000,
        rarity="epic",
        recipe=True,
        ing=["Dark Crystal", "Steel Ingot", "Leather Grip"],
    ),
    "W32": Weapon(  # [A]
        name="Inferno Sword",
        w_type="sword",
        damage=70,
        price=5500,
        rarity="epic",
        recipe=True,
        ing=["Inferno Crystal", "Steel Ingot", "Leather Grip"],
    ),
    "W33": Weapon(  # [A]
        name="Frost Dagger",
        w_type="dagger",
        damage=50,
        price=4000,
        rarity="epic",
        recipe=True,
        ing=["Ice Crystal", "Steel Ingot"],
    ),
    "W34": Weapon(  # [A]
        name="Storm Dagger",
        w_type="dagger",
        damage=55,
        price=4500,
        rarity="epic",
        recipe=True,
        ing=["Storm Crystal", "Steel Ingot"],
    ),
    "W35": Weapon(  # [A]
        name="Frost Hammer",
        w_type="axe",
        damage=55,
        price=2500,
        rarity="epic",
        recipe=True,
        ing=["Ice Crystal", "Steel Ingot", "Leather Grip"],
    ),
    "W36": Weapon(  # [A]
        name="Inferno Axe",
        w_type="axe",
        damage=60,
        price=3000,
        rarity="epic",
        recipe=True,
        ing=["Inferno Crystal", "Steel Ingot", "Wood"],
    ),
    "W37": Weapon(  # [A]
        name="Crystal Bow",
        w_type="bow",
        damage=50,
        price=2000,
        rarity="epic",
        recipe=True,
        ing=["Crystal Shard", "Wood", "Magic Thread"],
    ),
    "W38": Weapon(  # [A]
        name="Lunar Bow",
        w_type="bow",
        damage=55,
        price=2500,
        rarity="epic",
        recipe=True,
        ing=["Moon Crystal", "Wood", "Thread"],
    ),
    "W39": Weapon(  # [A]
        name="Silver Spear",
        w_type="spear",
        damage=45,
        price=1800,
        rarity="epic",
        recipe=True,
        ing=["Gold Ingot", "Wood"],
    ),
    "W40": Weapon(  # [A]
        name="Celestial Spear",
        w_type="spear",
        damage=50,
        price=2200,
        rarity="epic",
        recipe=True,
        ing=["Celestial Crystal", "Gold Ingot", "Wood"],
    ),
    "W41": Weapon(  # [S]
        name="Storm Blade",
        w_type="sword",
        damage=80,
        price=5000,
        rarity="legendary",
    ),
    "W42": Weapon(  # [S]
        name="Ethereal Dagger",
        w_type="dagger",
        damage=75,
        price=6000,
        rarity="legendary",
    ),
    "W43": Weapon(  # [S]
        name="Earthbreaker Axe",
        w_type="axe",
        damage=85,
        price=7000,
        rarity="legendary",
    ),
    "W44": Weapon(  # [S]
        name="Ether Bow",
        w_type="bow",
        damage=90,
        price=8000,
        rarity="legendary",
    ),
    "W45": Weapon(  # [S]
        name="Lunar Spear",
        w_type="spear",
        damage=95,
        price=9000,
        rarity="legendary",
    ),
    # Armor
    "A1": Armor(  # [D]
        name="Leather Armor",
        defense=5,
        price=40,
        rarity="common",
        recipe=True,
        ing=["Leather", "Thread"],
    ),
    "A2": Armor(  # [D]
        name="Steel Armor",
        defense=10,
        price=80,
        rarity="common",
        recipe=True,
        ing=["Steel Ingot", "Thread"],
    ),
    "A3": Armor(  # [C]
        name="Chainmail Armor",
        defense=15,
        price=120,
        rarity="uncommon",
        recipe=True,
        ing=["Iron Ingot", "Thread"],
    ),
    "A4": Armor(  # [C]
        name="Ice Armor",
        defense=20,
        price=160,
        rarity="uncommon",
        recipe=True,
        ing=["Ice Crystal", "Steel Ingot", "Thread"],
    ),
    "A5": Armor(  # [B]
        name="Golden Armor",
        defense=50,
        price=1000,
        rarity="rare",
        recipe=True,
        ing=["Gold Ingot", "Thread"],
    ),
    "A6": Armor(  # [B]
        name="Dragon Scale Armor",
        defense=60,
        price=1500,
        rarity="rare",
        recipe=True,
        ing=["Dragon Scale", "Steel Ingot", "Thread"],
    ),
    "A7": Armor(  # [A]
        name="Inferno Armor",
        defense=80,
        price=2500,
        rarity="epic",
        recipe=True,
        ing=["Inferno Crystal", "Steel Ingot", "Thread"],
    ),
    "A8": Armor(  # [A]
        name="Frost Armor",
        defense=90,
        price=3000,
        rarity="epic",
        recipe=True,
        ing=["Frost Crystal", "Steel Ingot", "Thread"],
    ),
    "A9": Armor(  # [S]
        name="Phoenix Feather Armor",
        defense=110,
        price=4000,
        rarity="legendary",
        recipe=True,
        ing=["Phoenix Feather", "Thread"],
    ),
    "A10": Armor(  # [S]
        name="Celestial Armor",
        defense=130,
        price=5000,
        rarity="legendary",
        recipe=True,
        ing=["Celestial Crystal", "Gold Ingot", "Thread"],
    ),
    # Items
    "I1": Item(
        name="Bomb",
        type="item",
        price=30,
        rarity="common",
    ),
    "I2": Item(
        name="Big Bomb",
        type="item",
        price=50,
        rarity="common",
    ),
    "I3": Item(
        name="Giant Bomb",
        type="item",
        price=100,
        rarity="uncommon",
    ),
    "I4": Item(
        name="Holy Bomb",
        type="item",
        price=200,
        rarity="rare",
    ),
    "I5": Item(
        name="Dark Bomb",
        type="item",
        price=400,
        rarity="epic",
    ),
    "I6": Item(
        name="Napalm",
        type="item",
        price=800,
        rarity="legendary",
    ),
    # Accessories
    "C1": Accessory(
        name="Ring of Strength",
        effect="str",
        mod=5,
        price=100,
        rarity="common",
    ),
    "C2": Accessory(
        name="Ring of Agility",
        effect="agi",
        mod=5,
        price=100,
        rarity="common",
    ),
    "C3": Accessory(
        name="Ring of Intelligence",
        effect="int",
        mod=10,
        price=100,
        rarity="common",
    ),
    "C4": Accessory(
        name="Ring of Defense",
        effect="dfc",
        mod=10,
        price=100,
        rarity="rare",
    ),
    "C5": Accessory(
        name="Rabbit Foot",
        effect="lck",
        mod=10,
        price=100,
        rarity="epic",
    ),
    "C6": Accessory(
        name="Necklace of Recovery",
        effect="reg",
        mod=10,
        price=100,
        rarity="legendary",
    ),
}

from src.entities.enemy import Enemy, Boss

ENEMY = {  # Enemy ID: Enemy Object
    # Dark Cave - Basic monsters and undead
    1: Enemy("Goblin", 20, 3, 10, 5, 0),
    2: Enemy("Skeleton", 25, 4, 15, 10, 0),
    3: Enemy("Zombie", 30, 5, 20, 15, 2),
    4: Enemy("Giant Bat", 15, 4, 12, 8, 0, 10),
    5: Enemy("Poisonous Spider", 18, 5, 15, 10, 1, 5),
    # Forbidden Forest - Nature creatures and humanoids
    6: Enemy("Wild Wolf", 36, 5, 18, 9, 0),
    7: Enemy("Orc", 45, 7, 27, 18, 0),
    8: Enemy("Giant Spider", 54, 9, 36, 27, 4),
    9: Enemy("Ent", 63, 11, 45, 36, 9),
    10: Enemy("Evil Fairy", 54, 14, 45, 36, 0, 18),
    # Frozen Mountain - Ice creatures and elementals
    11: Enemy("Snow Wolf", 65, 9, 32, 16, 0),
    12: Enemy("Ice Golem", 81, 13, 49, 29, 7),
    13: Enemy("Dark Fairy", 97, 16, 65, 49, 0, 32),
    14: Enemy("Yeti", 113, 20, 81, 65, 14),
    15: Enemy("Ice Elemental", 81, 25, 81, 65, 9, 9),
    # Ancient Temple - Mystical creatures and guardians
    16: Enemy("Mummy", 117, 16, 58, 29, 18, 9),
    17: Enemy("Phantom Cat", 146, 45, 90, 58, 18, 144),
    18: Enemy("Golden Skeleton", 175, 54, 117, 90, 36, 9),
    19: Enemy("Temple Guardian", 204, 45, 126, 108, 27, 18),
    20: Enemy("Cursed Pharaoh", 233, 54, 144, 126, 36, 9),
    # Abandoned Castle - Dark creatures and fallen nobles
    21: Enemy("Dark Knight", 210, 72, 180, 144, 54, 18),
    22: Enemy("Vampire", 252, 81, 216, 180, 36, 36),
    23: Enemy("Banshee", 168, 90, 198, 162, 27, 45),
    24: Enemy("Lich", 315, 99, 234, 198, 45, 27),
}

BOSS = {  # Boss ID: Boss Object
    1: Boss("Dark Troll", 50, 10, 50, 20, 5),
    2: Boss("High Elf", 90, 18, 90, 36, 9),
    3: Boss("Big Foot", 162, 32, 162, 65, 16),
    4: Boss("Anubis", 292, 63, 270, 180, 45),
    5: Boss("Fallen King", 540, 144, 540, 360, 72),
}

from src.locations.dungeon import Dungeon

DUNGEON = {  # Dungeon ID: Dungeon Object
    1: Dungeon("Caverna Sombria", 1),
    2: Dungeon("Floresta Proibida", 2),
    3: Dungeon("Montanha Congelada", 3),
    4: Dungeon("Templo Antigo", 4),
    5: Dungeon("Castelo Abandonado", 5),
}

DUNGEON_ENEMIES = {  # Dungeon ID: Enemy List
    1: [ENEMY[1], ENEMY[2], ENEMY[3], ENEMY[4]],
    2: [ENEMY[5], ENEMY[6], ENEMY[7], ENEMY[8]],
    3: [ENEMY[9], ENEMY[10], ENEMY[11], ENEMY[12]],
    4: [ENEMY[13], ENEMY[14], ENEMY[15], ENEMY[16]],
    5: [ENEMY[17], ENEMY[18], ENEMY[19], ENEMY[20]],
}

DUNGEON_ITEMS = {  # Dungeon ID: Item List
    1: [ITEM["P1"], ITEM["P2"], ITEM["W2"], ITEM["A1"]],
    2: [],
    3: [],
    4: [],
    5: [],
}

# House
ROOMS = {  # Room Name: Room Dict
    "bedroom": {
        "name": "Bedroom",
        "description": "A place to rest and recover energy",
        "cost": 100,
    },
    "brewery": {
        "name": "Brewery",
        "description": "A place to brew magical potions",
        "cost": 200,
    },
    "workshop": {
        "name": "Workshop",
        "description": "A place to craft weapons and armor",
        "cost": 200,
    },
    "garden": {
        "name": "Garden",
        "description": "A place to grow magical herbs and materials",
        "cost": 200,
    },
    "laboratory": {
        "name": "Laboratory",
        "description": "A place to study and research new recipes and facilities",
        "cost": 500,
    },
}


from src.locations.world import City, NPCCharacter, Shop

NPC = {  # NPC ID: NPCCharacter Object
    0: NPCCharacter(
        name="Eldon",
        desc="A friendly villager who offers guidance to new adventurers.",
        func=None,
        dial=[
            "Welcome to our humble town, traveler!",
            "If you need any help, feel free to ask me.",
            "Good luck on your journey!",
        ],
        locked=False,
    ),
    1: NPCCharacter(
        name="Marlo",
        desc="A wise old man with a simple shop.",
        func="Shopkeeper",
        dial=[
            "Hello, there! I'm Marlo, the shopkeeper.",
            "Would you like to see what I have for sale?",
        ],
    ),
    2: NPCCharacter(
        name="Selene",
        desc="A mysterious lady with a deep knowledge about mana, magic and potions.",
        func="Alchemist",
        dial=[
            "Greetings, traveler! I am Selene the alchemist.",
            "I can teach you some secrets about potions and magic...",
            "Would you like to learn some secrets of the world with me?",
        ],
    ),
    3: NPCCharacter(
        name="Garrick",
        desc="A blacksmith with a passion for crafting weapons.",
        func="Blacksmith",
        dial=[
            "Ah, a fellow admirer of fine craftsmanship!",
            "Let me show you some of my finest creations.",
        ],
    ),
    4: NPCCharacter(
        name="Liora",
        desc="A healer who tends to the wounded and weary.",
        func="Healer",
        dial=[
            "Welcome, traveler. Do you need healing or guidance?",
            "May the light guide your path.",
        ],
    ),
    5: NPCCharacter(
        name="Thorne",
        desc="A grizzled mercenary with tales of adventure.",
        func=None,
        dial=[
            "I've seen things you wouldn't believe.",
            "If you need advice on surviving out there, just ask.",
        ],
    ),
    6: NPCCharacter(
        name="Evelyn",
        desc="A librarian with a vast knowledge of ancient lore.",
        func="Librarian",
        dial=[
            "Books are the windows to the past and the future.",
            "What knowledge do you seek, traveler?",
        ],
    ),
    7: NPCCharacter(
        name="Darius",
        desc="A retired knight who trains young adventurers.",
        func="Trainer",
        dial=[
            "Discipline and courage are the keys to victory.",
            "Let me show you some techniques to improve your skills.",
        ],
    ),
    8: NPCCharacter(
        name="Fiona",
        desc="A cheerful baker known for her delicious pastries.",
        func="Baker",
        dial=[
            "Hello there! Care for a freshly baked treat?",
            "My pastries are the best in town!",
        ],
    ),
    9: NPCCharacter(
        name="Kael",
        desc="A wandering bard who sings tales of heroism.",
        func="Bard",
        dial=[
            "Greetings, traveler! Shall I sing you a song of old?",
            "Music is the soul's greatest companion.",
        ],
    ),
    10: NPCCharacter(
        name="Sylas",
        desc="A shady merchant dealing in rare artifacts.",
        func="Merchant",
        dial=[
            "Looking for something... unique? I might have what you need.",
            "Just don't ask too many questions about where it came from.",
        ],
    ),
    11: NPCCharacter(
        name="Isolde",
        desc="A herbalist who gathers rare plants for potions.",
        func="Herbalist",
        dial=[
            "Nature holds the cure to many ailments.",
            "Would you like to see my collection of herbs?",
        ],
    ),
    12: NPCCharacter(
        name="Ronan",
        desc="A fisherman who knows the secrets of the sea.",
        func="Fisherman",
        dial=[
            "The sea is a harsh mistress, but she provides for those who respect her.",
            "Care to hear a tale of the deep?",
        ],
    ),
    13: NPCCharacter(
        name="Astrid",
        desc="A jeweler who crafts exquisite accessories.",
        func="Jeweler",
        dial=[
            "Every gem has a story to tell.",
            "Let me show you some of my finest pieces.",
        ],
    ),
    14: NPCCharacter(
        name="Victor",
        desc="A grumpy innkeeper who runs the local tavern.",
        func="Innkeeper",
        dial=[
            "What do you want? A room or a drink?",
            "Just don't cause any trouble in my tavern.",
        ],
    ),
    15: NPCCharacter(
        name="Mira",
        desc="A fortune teller who sees glimpses of the future.",
        func="Fortune Teller",
        dial=[
            "The threads of fate are ever-changing.",
            "Would you like me to read your fortune?",
        ],
    ),
    16: NPCCharacter(
        name="Cedric",
        desc="A hunter who knows the forests like the back of his hand.",
        func="Hunter",
        dial=[
            "The wilderness is both beautiful and dangerous.",
            "If you're heading into the woods, I can give you some tips.",
        ],
    ),
    17: NPCCharacter(
        name="Elara",
        desc="A seamstress who creates magical garments.",
        func="Seamstress",
        dial=[
            "Clothing is more than just fabric; it's an expression of self.",
            "Would you like me to craft something special for you?",
        ],
    ),
    18: NPCCharacter(
        name="Magnus",
        desc="A retired mage who studies ancient spells.",
        func="Mage",
        dial=[
            "Magic is a tool, a weapon, and a mystery.",
            "Would you like to learn a spell or two?",
        ],
    ),
    19: NPCCharacter(
        name="Talia",
        desc="A cartographer who maps uncharted territories.",
        func="Cartographer",
        dial=[
            "The world is vast and full of wonders.",
            "Would you like to see my latest maps?",
        ],
    ),
    20: NPCCharacter(
        name="Orin",
        desc="A miner who digs deep for precious ores.",
        func="Miner",
        dial=[
            "The earth holds treasures beyond imagination.",
            "If you need raw materials, I'm your guy.",
        ],
    ),
}

CITY = {  # City ID: City Object
    0: City(
        name="Newhaven Village",
        level=0,
        shops=[
            Shop(
                name="Beginner's Supplies",
                items=["P1", "P2", "W1", "W3", "W5", "W7", "A1"],
            )
        ],
        dungeons=[1],
        npcs=[
            NPC[0],
        ],
    ),
    1: City(
        name="Arborstead",
        level=1,
        shops=[
            Shop(
                name="Marlo's Bazaar",
                items=["P1", "P2", "W2", "W4", "W6", "A2"],
            )
        ],
        dungeons=[
            DUNGEON[1],
        ],
        npcs=[
            NPC[1],
            NPC[2],
        ],
    ),
    2: City(
        name="Stormhold",
        level=2,
        shops=[
            Shop(
                name="Stormhold Armory",
                items=[
                    ITEM["W4"],
                    ITEM["W5"],
                    ITEM["A3"],
                    ITEM["A4"],
                    ITEM["I4"],
                ],
            )
        ],
        dungeons=[
            DUNGEON[2],
        ],
        npcs=[
            NPC[1],
            NPC[2],
        ],
    ),
    3: City(
        name="Eldergrove",
        level=3,
        shops=[
            Shop(
                name="Eldergrove Enchantments",
                items=[
                    ITEM["P3"],
                    ITEM["P4"],
                    ITEM["I5"],
                    ITEM["I6"],
                ],
            )
        ],
        dungeons=[
            DUNGEON[3],
        ],
        npcs=[
            NPC[2],
        ],
    ),
    4: City(
        name="Ironclad Bastion",
        level=4,
        shops=[
            Shop(
                name="Ironclad Forge",
                items=[
                    ITEM["W6"],
                    ITEM["A5"],
                ],
            )
        ],
        dungeons=[
            DUNGEON[4],
        ],
        npcs=[
            NPC[1],
            NPC[2],
        ],
    ),
    5: City(
        name="Mystvale",
        level=5,
        shops=[
            Shop(
                name="Mystvale Curios",
                items=[
                    ITEM["P5"],
                    ITEM["P6"],
                ],
            )
        ],
        dungeons=[
            DUNGEON[5],
        ],
        npcs=[
            NPC[2],
        ],
    ),
}
