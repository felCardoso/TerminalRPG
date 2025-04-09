class Enemy:
    def __init__(self, name, hp, attack, exp_reward, gold_reward, defense=0):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        dmg = max(damage - self.defense, 0)
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        print(f"{self.name} took {dmg} damage!")

    def show_status(self):
        print(f"{self.name} | HP: {self.hp} | ATK: {self.attack} | DEF: {self.defense}")
