# from src.utils.codex import ITEM
from src.utils.core import chance
from random import randint


class Enemy:
    def __init__(self, name, hp, atk, xp_rwd, coi_rwd, dfs=0, agi=0):
        self.name = name
        self.attack = atk  # Base attack value
        self.defense = dfs  # Base defense value
        self.agility = agi
        self.hp = hp
        self.xp_reward = chance(xp_rwd, int(xp_rwd * 0.5))
        self.coin_reward = chance(coi_rwd, int(coi_rwd * 0.5))
        self.item_reward = []
        self.is_boss = False
        self.is_miniboss = False

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


def gen_enemy(race, level=None, miniboss=False):  # ATK / DEF / AGI / HP / XP_R / CO_R
    from src.utils.codex import ENEMY_PREFIX, ENEMY_NAME

    def gen_stats(total_points):
        stats = [0] * 4
        for _ in range(total_points):
            stats[randint(0, 3)] += 5
        return stats

    def gen_miniboss():  # 10 to 15
        x = chance(10, 5)
        if x <= 10:
            x = 10
        elif x >= 15:
            x = 15
        enemy_name = f"{ENEMY_PREFIX[x]} {ENEMY_NAME[race][randint(1,10)]}"
        enemy_stats = gen_stats(int((level * 10 * 1.5) * (x / 10)))
        enemy = Enemy(
            name=enemy_name,
            hp=enemy_stats[0],
            atk=enemy_stats[1],
            dfs=enemy_stats[2],
            agi=enemy_stats[3],
            xp_rwd=int((sum(enemy_stats) * 1.5) * (x / 7.5)),
            coi_rwd=int((sum(enemy_stats) * 1.5) * (x / 7.5)),
        )
        enemy.is_miniboss = True
        return enemy

    if miniboss:
        return gen_miniboss()
    if not level:
        x = chance()
        if x <= 10:
            gen_miniboss(chance(10, 5))
        else:
            i = chance(sides=10)
