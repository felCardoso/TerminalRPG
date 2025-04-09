import random
import json
from src.utils import Colors, roll_check, clear_screen, type_text


class Fight:
    def __init__(self):
        with open("data/damage_config.json", "r") as f:
            self.damage_config = json.load(f)

        self.attack_categories = {
            "1": "sword",
            "2": "magic",
            "3": "bow",
            "4": "summon",
            "5": "shield",
        }

    def start(self, player, enemy):
        type_text(f"A {enemy.name} appeared!", color=Colors.LRED, delay=0.05)

        turn = 1
        while enemy.is_alive() and player.is_alive():
            print(f"\n{Colors.MAG}===== Turn {turn} =====")
            self.display_status(player, enemy)
            self.player_turn(player, enemy)
            if enemy.is_alive():
                self.enemy_turn(player, enemy)
            turn += 1

        if not player.is_alive():
            print(f"{Colors.RED}💀 You were defeated!")
        else:
            print(f"{Colors.GRE}🏆 Victory! You defeated the {enemy.name}.")
            player.gain_exp(enemy.exp_reward)
            player.gain_money(enemy.gold_reward)
            player.check_class()

    def display_status(self, player, enemy):
        print(f"{Colors.RED}\n🧟 {enemy.name}: {enemy.hp} HP")
        print(f"{Colors.CYA}🧝 {player.name}: {player.attributes['VIT']} HP")
        print(f"{Colors.WHI}\nChoose your action category:")
        print("[1] Sword | [2] Magic | [3] Bow | [4] Summon | [5] Shield")

    def player_turn(self, player, enemy):
        action, mod, base_damage = self.choose_attack(player)
        if not action:
            return
        self.player_attack(player, enemy, action, mod, base_damage)

    def enemy_turn(self, player, enemy):
        dodge_roll = roll_check(player.attributes["AGI"])
        if dodge_roll < 10:
            enemy_damage = enemy.attack + random.randint(1, 4)
            player.attributes["VIT"] -= enemy_damage
            print(f"{Colors.RED}⚔ {enemy.name} hit you! You took {enemy_damage} damage.")
        else:
            print(f"{Colors.BLU}🚡 You dodged the attack!")

    def choose_attack(self, player):
        category_choice = input("> ")
        category = self.attack_categories.get(category_choice)

        if not category:
            print(f"{Colors.RED}[x] Invalid category.")
            return None, None, None

        options = self.get_attacks_by_category(category)
        if not options:
            print(f"{Colors.RED}[x] No attacks found.")
            return None, None, None

        print("\nChoose your attack:")
        for i, atk in enumerate(options, 1):
            desc = self.damage_config[atk].get("description", "")
            print(f"[{i}] {atk} - {desc}")

        atk_choice = input("> ")
        try:
            attack_name = options[int(atk_choice) - 1]
        except (IndexError, ValueError):
            print(f"{Colors.RED}[x] Invalid attack.")
            return None, None, None

        mod = self.get_modifier_for_attack(player, attack_name)
        base_damage = self.damage_config[attack_name]["base_damage"]
        return attack_name, mod, base_damage

    def get_attacks_by_category(self, category):
        return [atk for atk in self.damage_config if atk.startswith(category)]

    def get_modifier_for_attack(self, player, attack_name):
        if "sword" in attack_name or "shield" in attack_name:
            return player.attributes["STR"]
        elif "magic" in attack_name or "fire" in attack_name or "ice" in attack_name:
            return player.attributes["INT"]
        elif "bow" in attack_name or "crossbow" in attack_name:
            return player.attributes["AGI"]
        elif "summon" in attack_name or "spirit" in attack_name:
            return player.attributes["INT"]
        return 1

    def player_attack(self, player, enemy, action, mod, base_damage):
        player.use_action(action)
        attack_roll = roll_check(mod)

        if attack_roll >= 12:
            damage = random.randint(1, base_damage) + mod
            enemy.take_damage(damage)
            print(f"{Colors.GRE}💥 Hit! You dealt {damage} damage.")
        else:
            print(f"{Colors.YEL}❌ Missed the attack!")
