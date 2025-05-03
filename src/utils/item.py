from src.utils.core import C, chance

RARITY_C = {
    "common": f"{C.WHI}",
    "uncommon": f"{C.GRE}",
    "rare": f"{C.BLU}",
    "epic": f"{C.MAG}{C.FAD}",
    "legendary": f"{C.RED}{C.BOL}",
}

TYPE_C = {
    "hp": f"{C.RED}",
    "mp": f"{C.CYA}",
    "df": f"{C.GRE}",
    "agi": f"{C.BLU}",
    "str": f"{C.YEL}",
}


def get_rarity(rarity, dict):  # Return a list of items by rarity
    items = []
    for item in dict:
        if item.rarity == rarity:
            items.append(item)
    return items[chance(mod=0, sides=len(items))]


class Item:
    def __init__(self, name, type, rarity, price, recipe=False, ing=None):
        self.name = name
        self.type = type
        self.rarity = rarity
        self.price = price
        self.recipe = recipe
        self.ing = ing

    def __str__(self):
        return f"{C.WHI}[{C.BLA}{self.type.capitalize()}{C.WHI}] {RARITY_C[self.rarity]}{self.name}{C.RESET}"

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "rarity": self.rarity,
            "price": self.price,
        }

    def opt(self):
        if self.type == "potion":
            return f"{RARITY_C[self.rarity]}{self.name} {C.WHI}({TYPE_C[self.effect]}{self.mod} {self.effect.upper()}{C.WHI}){C.RESET}"
        elif self.type == "weapon":
            return f"{RARITY_C[self.rarity]}{self.name} {C.WHI}({C.BLA}{self.damage} DMG{C.WHI}){C.RESET}"
        elif self.type == "armor":
            return f"{RARITY_C[self.rarity]}{self.name} {C.WHI}({C.BLA}{self.defense} DEF{C.WHI}){C.RESET}"
        elif self.type == "accessory":
            return f"{RARITY_C[self.rarity]}{self.name} {C.WHI}({C.BLA}{self.mod} {self.effect.upper()}{C.WHI}){C.RESET}"


class Potion(Item):
    def __init__(self, name, rarity, price, effect, mod, recipe=False, ing=None):
        super().__init__(name, "potion", rarity, price, recipe, ing)
        self.effect = effect  # Potion type ("hp" / "mp" / "agi" / "str")
        self.mod = mod  # Effect amount (int)

    def __str__(self):
        TYPE_C = {
            "hp": f"{C.RED}",
            "mp": f"{C.CYA}",
            "df": f"{C.GRE}",
            "agi": f"{C.BLU}",
            "str": f"{C.YEL}",
        }
        return f"{super().__str__()} {C.WHI}({TYPE_C[self.effect]}+{self.mod}{C.WHI}){C.RESET}"

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "effect": self.effect,
                "mod": self.mod,
            }
        )
        return data


class Weapon(Item):
    def __init__(self, name, rarity, price, damage, w_type, recipe=False, ing=None):
        super().__init__(name, "weapon", rarity, price, recipe, ing)
        self.w_type = w_type
        self.damage = damage

    def __str__(self):
        return f"{super().__str__()} {C.WHI}(+{C.BLA}{self.damage}{C.WHI})"

    def to_dict(self):
        data = super().to_dict()
        data["w_type"] = self.w_type
        data["damage"] = self.damage
        return data


class Armor(Item):
    def __init__(self, name, rarity, price, defense, recipe=False, ing=None):
        super().__init__(name, "armor", rarity, price, recipe, ing)
        self.defense = defense

    def __str__(self):
        return f"{super().__str__()} {C.WHI}(+{C.GRE}{self.defense}{C.WHI}){C.RESET}"

    def to_dict(self):
        data = super().to_dict()
        data["defense"] = self.defense
        return data


class Accessory(Item):
    def __init__(self, name, rarity, price, effect, mod, recipe=False, ing=None):
        super().__init__(name, "accessory", rarity, price, recipe, ing)
        self.effect = effect
        self.mod = mod

    def __str__(self):
        effect_color = {
            "vit": f"{C.RED}",
            "agi": f"{C.BLU}",
            "str": f"{C.YEL}",
            "int": f"{C.CYA}",
            "df": f"{C.GRE}",
        }
        return f"{super().__str__()} {C.WHI}(+{effect_color[self.effect]}{self.mod} {self.effect.upper()}{C.WHI}){C.RESET}"

    def to_dict(self):
        data = super().to_dict()
        data["effect"] = self.effect
        data["mod"] = self.mod
        return data


class Ingredient:
    def __init__(self, name, rarity, price):
        self.name = name
        self.rarity = rarity
        self.price = price

    def __str__(self):
        return f"{C.WHI}[{C.BLA}I{C.WHI}] {RARITY_C[self.rarity]}{self.name}"

    def to_dict(self):
        return {
            "name": self.name,
            "rarity": self.rarity,
            "price": self.price,
        }
