class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.att = {"FOR": 5, "AGI": 5, "VIT": 5, "INT": 5}  # Atributos
        self.lvl = 1  # Nível
        self.xp = 0  # Experiência
        self.coins = 0  # Moedas
        self.hp = self.get_max_hp()  # Vida
        self.mp = self.get_max_mp()  # Mana
        self.title = None  # Título
        self.inv = []  # Inventário
        self.equip = []  # Equipamentos

    def add_xp(self, qnt: int) -> None:
        self.xp += qnt
        if self.xp >= self.get_max_xp():
            self.xp -= self.get_max_xp()
            self.lvl += 1
            print(f"{self.name} subiu para o nível {self.lvl}!")
            self.hp = self.get_max_hp()

    def get_max_hp(self) -> int:
        return self.att["VIT"] * 10

    def get_max_mp(self) -> int:
        return self.att["INT"] * 10

    def get_max_xp(self) -> int:
        return 100 + (self.lvl * 10)

    def add_coins(self, qnt: int) -> None:
        self.coins += qnt

    def add_att(self, att: str, qnt: int) -> None:
        if att in self.att:
            self.att[att] += qnt
        else:
            print(f'Você não possui o atributo "{att}".')

    def __str__(self) -> str:
        card = f"""{self.name}{self.title}
Lv.{self.lvl} [{self.xp}/100] - {self.coins}c
HP: {self.hp}/{self.get_max_hp()} - MP: {self.mp}/{self.get_max_mp()}
FOR: {self.att["FOR"]} - AGI: {self.att["AGI"]} - VIT: {self.att["VIT"]} - INT: {self.att["INT"]}
"""
        return card
