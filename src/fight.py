from src.utils import C, roll_check, clear_screen, type_text, PRESS_ENTER
from random import randint, choice
from time import sleep, time


class Fight:
    def __init__(self):
        pass
        self.flee = False

    def start(self, player, enemy):
        clear_screen()
        type_text(choice(RANDOM_ENCOUNTERS), color=C.REDL)
        sleep(1.5)

        if enemy.is_boss:
            type_text(choice(BOSS_ENCOUNTERS), color=C.RED)
            type_text("Prepare yourself!", color=C.RED)
            sleep(1.5)

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
            type_text(f"💀 You were defeated by the {enemy.name}!", color=C.RED)
            sleep(1)
            input(f"{C.BLUL}[i] Pressione Enter para continuar.")
        else:
            if self.flee:
                return
            else:
                clear_screen()
                if enemy.is_boss:
                    type_text(f"You defeated the boss {enemy.name}!", color=C.MAG)
                    sleep(1)
                else:
                    print(f"{C.GRE}🏆 Victory! You defeated the {enemy.name}.")
                    sleep(1)
                player.add_xp(enemy.xp_reward)
                player.add_coin(enemy.coin_reward)
                if enemy.item_reward:
                    if isinstance(enemy.item_reward, list):
                        for item in enemy.item_reward:
                            player.add_item(item)
                    else:
                        player.add_item(enemy.item_reward)

                    type_text("You can now continue your adventure!", color=C.GRE)
                sleep(1)
                print()
                input(PRESS_ENTER)

    def status(self, player, enemy):
        print(f"{C.RED}\n🧟 {enemy.name}: {enemy.hp} HP")
        print(f"{C.CYA}🧝 {player.name}: {player.hp} HP")
        type_text("Choose your action:", color=C.WHI)
        print(
            f"{C.WHI}[{C.BLA}1{C.WHI}] Attack {C.BLA}| {C.WHI}[{C.WHI}2{C.WHI}] Ability {C.BLA}| {C.WHI}[{C.WHI}3{C.WHI}] Item {C.BLA}| {C.WHI}[{C.WHI}4{C.WHI}] Run"
        )

    def player_turn(self, player, enemy, turn):
        clear_screen()
        print(f"{C.MAG}===== Turn {turn} =====")
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
                            f"{C.GRE}You used {selected_item['name']} and healed {selected_item['effect']['heal']} HP!"
                        )
                    elif "dmg" in selected_item["effect"]:  # If it's a damaging item
                        enemy.take_damage(selected_item["effect"]["dmg"])
                        print(
                            f"{C.RED}You used {selected_item['name']} and dealt {selected_item['effect']['dmg']} damage to {enemy.name}!"
                        )
                    (
                        player.inventory["potions"].remove(selected_item)
                        if selected_item in player.inventory["potions"]
                        else player.inventory["items"].remove(selected_item)
                    )
                else:
                    print(f"{C.RED}[x] Invalid item selection!")
            except (ValueError, IndexError):
                print(f"{C.RED}[x] Invalid input!")
            sleep(1)
        elif action == "4":
            chance = roll_check(sides=100)
            if chance >= min(player.attributes["AGI"] * 5, 80):
                print(f"{C.GRE}🏃 You successfully ran away!")
                self.flee = True
                sleep(1)
                return
            else:
                print(f"{C.RED}❌ Failed to run away!")
                sleep(1)
                return
        else:
            print(f"{C.RED}[x] Invalid action!")
            self.player_turn(player, enemy, turn)

    def enemy_turn(self, player, enemy):
        # Chance de 30% de ter que fazer um teste de reflexo
        if roll_check(sides=100) <= min(player.attributes["AGI"], 70):
            if self.reflex_check():
                print(f"{C.GRE}You dodged {enemy.name}'s attack!")
                sleep(1)
                return
            else:
                print(f"{C.RED}You didn't dodge in time!")
                sleep(1)
        enemy_damage = randint(enemy.attack - 2, enemy.attack + 2)
        dmg = player.take_damage(enemy_damage)
        print(f"{C.RED}⚔ {enemy.name} hit you! You took {dmg} damage.")
        sleep(1)

    def player_attack(self, player, enemy):
        base_dmg = roll_check(mod=player.attributes["STR"], sides=6)
        if player.has_weapon():
            weapon_dmg = player.equipment["weapon"]["effect"]["dmg"]
            base_dmg += weapon_dmg
        dmg = enemy.take_damage(base_dmg)
        print(f"{C.GRE}⚔ You hit the {enemy.name} for {dmg} damage!")
        sleep(1)

    def reflex_check(self):  # Quick-time event (Player Reflex)
        x = choice(["a", "b", "c", "x", "y", "z", "l"])
        clear_screen()
        print(f"{C.RED}[!] Type [{x.upper()}] to dodge!")
        start_time = time()
        response = input().lower()
        end_time = time()

        reaction_time = end_time - start_time
        if response == x.lower() and reaction_time < 2.5:  # React time
            return True
        return False


RANDOM_ENCOUNTERS = [
    "A shadowy figure emerges from the darkness, its eyes glowing with malice...",
    "The ground trembles as a fearsome creature steps into view...",
    "From the mist, a sinister presence reveals itself...",
    "A blood-curdling roar echoes through the area as your enemy appears...",
    "The air grows cold as a menacing foe materializes before you...",
    "Your path is blocked by a formidable opponent...",
    "A sudden movement catches your eye - danger approaches!",
    "The silence is broken by the sound of approaching footsteps...",
    "A pair of glowing eyes pierce through the darkness...",
    "The scent of danger fills the air as your enemy reveals itself...",
    "A chilling presence makes itself known...",
    "The shadows themselves seem to take form as your adversary appears...",
    "Your instincts scream danger as a new threat emerges...",
    "The very ground seems to reject the presence of this foe...",
    "A sinister laugh echoes as your enemy steps into the light...",
]

BOSS_ENCOUNTERS = [
    "The very air trembles as the legendary boss reveals its true form...",
    "A deafening roar shakes the foundations as the mighty boss emerges...",
    "The final guardian of this realm stands before you, radiating power...",
    "The ground cracks beneath the weight of the ultimate adversary...",
    "A wave of pure terror washes over you as the boss enters the battlefield...",
]
