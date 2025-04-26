from src.utils import Colors, roll_check, clear_screen, type_text
from random import randint
from time import sleep


class Fight:
    def __init__(self):
        pass
        self.flee = False

    def start(self, player, enemy):
        clear_screen()
        type_text(f"A {enemy.name} appeared!", color=Colors.LRED)
        sleep(1)

        if enemy.is_boss:
            type_text(f"⚔️ Boss Fight: {enemy.name}!", color=Colors.MAG)
            sleep(1)
            type_text("Prepare yourself!", color=Colors.RED)
            sleep(1)
        turn = 1
        while enemy.is_alive() and player.is_alive() and not self.flee:
            self.player_turn(player, enemy, turn)
            if self.flee:
                break
            if enemy.is_alive():
                self.enemy_turn(player, enemy)
            turn += 1
            player.pass_time(0.2)

        if not player.is_alive():
            clear_screen()
            type_text(f"💀 You were defeated by the {enemy.name}!", color=Colors.RED)
            sleep(1)
            input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")
        else:
            clear_screen()
            print(f"{Colors.GRE}🏆 Victory! You defeated the {enemy.name}.")
            player.add_xp(enemy.xp_reward)
            player.add_coin(enemy.coin_reward)
            if enemy.item_reward:
                if isinstance(enemy.item_reward, list):
                    for item in enemy.item_reward:
                        player.add_item(item)
                else:
                    player.add_item(enemy.item_reward)
            if enemy.is_boss:
                type_text(f"🎉 You defeated the boss {enemy.name}!", color=Colors.MAG)
                sleep(1)
                type_text("You can now continue your adventure!", color=Colors.GRE)
            sleep(1)
            input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")

    def status(self, player, enemy):
        print(f"{Colors.RED}\n🧟 {enemy.name}: {enemy.hp} HP")
        print(f"{Colors.CYA}🧝 {player.name}: {player.hp} HP")
        type_text("Choose your action:", color=Colors.WHI)
        print("[1] Attack | [2] Ability | [3] Item | [4] Run")

    def player_turn(self, player, enemy, turn):
        clear_screen()
        print(f"{Colors.MAG}===== Turn {turn} =====")
        self.status(player, enemy)
        action = input("> ")
        if action == "1":
            self.player_attack(player, enemy)
        elif action == "2":
            player.list_abilities()
            ability = input("Choose your ability:\n> ")
            player.use_ability(num=ability, enemy=enemy)
        elif action == "3":
            player.show_inventory()
            item_index = input("Choose an item or potion by its number:\n> ")
            try:
                item_index = int(item_index) - 1
                all_items = (
                    player.inventory["potions"] + player.inventory["items"]
                )  # Combine potions and items
                if 0 <= item_index < len(all_items):
                    selected_item = all_items[item_index]
                    if "heal" in selected_item["effect"]:  # If it's a healing potion
                        player.heal(selected_item["effect"]["heal"])
                        print(
                            f"{Colors.GRE}You used {selected_item['name']} and healed {selected_item['effect']['heal']} HP!"
                        )
                    elif "dmg" in selected_item["effect"]:  # If it's a damaging item
                        enemy.take_damage(selected_item["effect"]["dmg"])
                        print(
                            f"{Colors.RED}You used {selected_item['name']} and dealt {selected_item['effect']['dmg']} damage to {enemy.name}!"
                        )
                    (
                        player.inventory["potions"].remove(selected_item)
                        if selected_item in player.inventory["potions"]
                        else player.inventory["items"].remove(selected_item)
                    )
                else:
                    print(f"{Colors.RED}[x] Invalid item selection!")
            except (ValueError, IndexError):
                print(f"{Colors.RED}[x] Invalid input!")
            sleep(1)
        elif action == "4":
            chance = roll_check(mod=player.attributes["AGI"], sides=5)
            if chance >= (enemy.agility * 2):
                print(f"{Colors.GRE}🏃 You successfully ran away!")
                self.flee = True
                sleep(1)
                return
            else:
                print(f"{Colors.RED}❌ Failed to run away!")
                sleep(1)
                self.enemy_turn(player, enemy)
        else:
            print(f"{Colors.RED}[x] Invalid action!")
            self.player_turn(player, enemy, turn)

    def enemy_turn(self, player, enemy):
        dodge_roll = roll_check(mod=player.attributes["AGI"], sides=5)
        if dodge_roll < 15:
            enemy_damage = randint(enemy.attack - 2, enemy.attack + 2)
            dmg = player.take_damage(enemy_damage)
            print(f"{Colors.RED}⚔ {enemy.name} hit you! You took {dmg} damage.")
            sleep(1)
        else:
            print(f"{Colors.BLU}🚡 You dodged the attack!")
            sleep(1)

    def player_attack(self, player, enemy):
        base_dmg = roll_check(mod=player.attributes["STR"], sides=6)
        if player.has_weapon():
            weapon_dmg = player.equipment["weapon"]["effect"]["dmg"]
            base_dmg += weapon_dmg
        dmg = enemy.take_damage(base_dmg)
        print(f"{Colors.GRE}⚔ You hit the {enemy.name} for {dmg} damage!")
        sleep(1)
