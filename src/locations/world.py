from src.utils.core import C, type_text, title_text, clear_screen
from src.utils.codex import ITEM, DUNGEON

# ₵ Money


class City:
    def __init__(self, name, level, shops=None, dungeons=None, npcs=None):
        self.name = name
        self.level = level
        self.shops = shops if shops else []
        self.dungeons = dungeons if dungeons else []
        self.npcs = npcs if npcs else []
        self.update()

    def update(self):
        for npc in self.npcs:
            npc.city = self

    def guild_create(self, name, player):
        self.guild = Guild(name, player)

    def shop(self, i=0):
        shop = self.shops[i]
        clear_screen()
        while True:
            shop.display()


class Guild:  # TODO
    def __init__(self, name, player):
        self.name = name
        self.player = player
        self.rank = "D"
        self.reputation = 0
        self.gold = 0

    def __str__(self):
        rank_color = {
            "S": f"{C.RED}{C.BOL}",
            "A": f"{C.CYA}{C.FAD}",
            "B": f"{C.YEL}{C.FAD}",
            "C": f"{C.BLA}",
            "D": f"{C.WHI}",
        }
        return f"{C.WHI}[{C.BLA}{self.name}{C.WHI}] Rank {rank_color[self.rank]}{self.rank}{C.RESET}"

    def check_rank(self):
        if self.reputation <= 5 and self.player.attributes["STR"] >= 10:
            self.rank = "E"
        elif self.reputation <= 20 and self.player.attributes["STR"] >= 15:
            self.rank = "D"
        elif self.reputation <= 50 and self.player.attributes["STR"] >= 25:
            self.rank = "C"
        elif self.reputation <= 100 and self.player.attributes["STR"] >= 40:
            self.rank = "A"
        elif self.player:
            self.rank = "S"

    def quests(self):
        pass

    def add_gold(self):
        pass

    def take_gold(self):
        pass


class NPCCharacter:
    def __init__(self, name, desc, func=None, dial=None, locked=True):
        self.name = name
        self.description = desc
        self.func = func
        self.dialogue = dial if dial else []
        self.locked = locked

        self.city = None

    def talk(self):
        print(f"{C.YELLOW}{self.name}{C.ENDC}: {self.description}")
        for line in self.dialogue:
            type_text(line)
            print()

    def unlock(self):
        self.unlocked = True
        print(f"{C.GREEN}You have unlocked {self.name}!{C.ENDC}")
        type_text(f"{self.name} is now available for interaction.")
        print()
        self.talk()

    def interact(self):
        if not self.locked:
            if self.function == "Shopkeeper":
                self.city.shop(self.name)


class Shop:
    def __init__(self, name, items=None):
        self.name = name
        self.items = items if items else []

    def buy(self, player, item_id):
        item = ITEM[item_id]
        if player.coins >= item.price:
            player.coins -= item.price
            player.add_item(item_id)
            return True
        else:
            return False
