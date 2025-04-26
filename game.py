from src.player import Player
from src.enemy import (
    Enemy,
    Boss,
    DUNGEON_LEVELS,
    DUNGEON_ENEMIES,
    DUNGEON_ITEMS,
    BASE_ITEM_CHANCE,
    RARE_ITEM_CHANCE,
    EPIC_ITEM_CHANCE,
    LEGENDARY_ITEM_CHANCE,
)
from src.utils import Colors, SaveManager, clear_screen, type_text, roll_check, gen_shop
from src.fight import Fight
from time import sleep
from src.house import House

sm = SaveManager()


def main_menu():
    while True:
        clear_screen()
        print(f"{Colors.MAG}🎮 DUNGEON AWAKENING RPG\n")
        print(f"{Colors.WHI}[1] Novo Jogo")
        print("[2] Continuar")
        print("[3] Sair")
        i = input("\nEscolha uma opção:\n> ")

        if i == "1":
            clear_screen()
            slot = sm.select_slot(new=True)
            if slot:
                new_game(slot)
        elif i == "2":
            clear_screen()
            slot = sm.select_slot(new=False)
            if slot:
                continue_game(slot)
        elif i == "3":
            clear_screen()
            type_text("Até logo, caçador!", color=Colors.RED)
            sleep(1.5)
            print(f"{Colors.RESET}", end="")
            clear_screen()
            break
        else:
            clear_screen()
            print(f"{Colors.RED}[x] Escolha inválida!")
            sleep(1)
            input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")


def new_game(slot_file):
    clear_screen()
    name = input("Digite o nome do seu personagem:\n> ")
    player = Player(name)
    sm.save(player, slot_file)
    start_adventure(player, slot_file)


def continue_game(slot_file):
    try:
        data = sm.load(slot_file)
        player = Player.from_dict(data)
        start_adventure(player, slot_file)
    except FileNotFoundError:
        print(f"{Colors.RED}[x] Arquivo de save não encontrado!\n")
        sleep(1)
        input(f"{Colors.LBLU}[i] Pressione Enter para voltar ao menu principal.")
        main_menu()


def start_adventure(player, slot_file):
    while True:
        clear_screen()
        print(f"{player.name} entra na dungeon...\n")
        print("O que você deseja fazer?")
        print(f"{Colors.LBLU}1. Dungeons")
        print(f"2. Ver status do personagem")
        print(f"3. Loja")
        print(f"4. Inventário")
        print(f"5. Minha Casa")
        print(f"6. Salvar e sair")
        choice = input("> ")

        if choice == "1":
            explore_dungeon(player)
        elif choice == "2":
            clear_screen()
            print(player)
            input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")
        elif choice == "3":
            shop_menu(player)
        elif choice == "4":
            player.show_inventory(True)
        elif choice == "5":
            house_menu(player)
        elif choice == "6":
            clear_screen()
            sm.save(player, slot_file)
            print("Saindo para o menu principal...")
            sleep(1)
            break
        else:
            clear_screen()
            print(f"{Colors.RED}[x] Escolha inválida!")


def shop_menu(player):
    clear_screen()
    # Gerar itens aleatórios para a loja
    shop_items = gen_shop()

    while True:
        print(f"{Colors.MAG}🏪 Bem-vindo à Loja!")
        print(f"{Colors.GRE}Moedas disponíveis: {player.coins}")
        print(f"{Colors.WHI}Itens disponíveis para compra:")

        # Agrupar itens por categoria
        items_by_category = {}
        for item in shop_items:
            if item["type"] not in items_by_category:
                items_by_category[item["type"]] = []
            items_by_category[item["type"]].append(item)

        # Exibir itens por categoria
        item_count = 1
        for category, items in items_by_category.items():
            print(f"\n{Colors.CYA}{category.upper()}:")
            for item in items:
                rarity_color = Colors.WHI
                if item.get("rarity") == "raro":
                    rarity_color = Colors.MAG
                elif item.get("rarity") == "épico":
                    rarity_color = Colors.RED
                print(
                    f"[{item_count}] {rarity_color}{item['name']} - {item['price']} moedas"
                )
                item_count += 1

        print(f"\n{Colors.LBLU}[0] Sair da loja")
        choice = input("\nEscolha um item para comprar (número):\n> ")

        if choice == "0" or choice == "":
            clear_screen()
            print(f"{Colors.GRE}Obrigado por visitar a loja!")
            sleep(1.5)
            break

        try:
            choice = int(choice) - 1
            if 0 <= choice < len(shop_items):
                item = shop_items[choice]
                if player.coins >= item["price"]:
                    player.coins -= item["price"]
                    player.add_item(item, item["type"])
                    print(f"{Colors.GRE}Você comprou {item['name']}!")
                    if item.get("rarity") == "raro":
                        print(f"{Colors.MAG}✨ É um item raro!")
                    elif item.get("rarity") == "épico":
                        print(f"{Colors.RED}🔥 É um item épico!")
                else:
                    print(f"{Colors.RED}[x] Você não tem moedas suficientes!")
            else:
                print(f"{Colors.RED}[x] Escolha inválida!")
        except ValueError:
            print(f"{Colors.RED}[x] Entrada inválida!")

        input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")
        clear_screen()


def explore_dungeon(player):
    clear_screen()
    print(f"{Colors.MAG}🌌 Escolha uma Dungeon para explorar:")
    for level, dungeon in DUNGEON_LEVELS.items():
        print(
            f"{level}. {dungeon.name} (Nível {dungeon.level}) - {dungeon.level * 2} dias de viagem"
        )
    print("0. Voltar")
    choice = input("> ")

    try:
        choice = int(choice)
        if choice == 0:
            return
        if choice in DUNGEON_LEVELS:
            dungeon = DUNGEON_LEVELS[choice]
            travel_time = int(dungeon.level * 48)  # 2 dias por nível
            clear_screen()
            print(
                f"{Colors.LBLU}🛤️ Você começou sua jornada para {Colors.CYA}{dungeon.name}{Colors.LBLU}. Isso levará {int(travel_time / 24)} dias."
            )
            player.pass_time(travel_time)

            # Criar barra de progresso
            bar_length = 50
            for i in range(travel_time):
                progress = (i + 1) / travel_time
                filled_length = int(bar_length * progress)
                bar = f"{Colors.LBLU}[{'▮' * filled_length}{' ' * (bar_length - filled_length)}] {int(progress * 100)}%"
                print(f"\r{bar}", end="")
                sleep(0.15)
            print(f"\n{Colors.GRE}Você chegou na {dungeon.name}!")
            start_dungeon(player, dungeon)
        else:
            print(f"{Colors.RED}[x] Dungeon inválida!")
    except ValueError:
        print(f"{Colors.RED}[x] Entrada inválida!")
    input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")


def start_dungeon(player, dungeon):
    clear_screen()
    print(f"{Colors.MAG}🌌 Entrando na {dungeon.name}...")
    sleep(1)

    # Criar novos inimigos para a dungeon baseado no nível
    dungeon.enemies = []
    for enemy in DUNGEON_ENEMIES[dungeon.level]:
        if isinstance(enemy, Boss):
            dungeon.boss = Boss(
                enemy.name,
                enemy.hp,
                enemy.attack,
                enemy.xp_reward,
                enemy.coin_reward,
                enemy.defense,
            )
            # Adicionar drops lendários ao chefe
            chance = roll_check(mod=0, sides=100)
            if chance <= LEGENDARY_ITEM_CHANCE:
                # Filtrar itens lendários
                legendary_items = [
                    item
                    for item in DUNGEON_ITEMS[dungeon.level]
                    if item.get("rarity") == "lendário"
                ]
                if legendary_items:
                    dungeon.boss.set_item(legendary_items)
            elif chance <= EPIC_ITEM_CHANCE:
                # Filtrar itens épicos
                epic_items = [
                    item
                    for item in DUNGEON_ITEMS[dungeon.level]
                    if item.get("rarity") == "épico"
                ]
                if epic_items:
                    dungeon.boss.set_item(epic_items)
            elif chance <= RARE_ITEM_CHANCE:
                # Filtrar itens raros
                rare_items = [
                    item
                    for item in DUNGEON_ITEMS[dungeon.level]
                    if item.get("rarity") == "raro"
                ]
                if rare_items:
                    dungeon.boss.set_item(rare_items)
            elif chance <= BASE_ITEM_CHANCE:
                # Filtrar itens comuns
                common_items = [
                    item
                    for item in DUNGEON_ITEMS[dungeon.level]
                    if item.get("rarity") == "comum"
                ]
                if common_items:
                    dungeon.boss.set_item(common_items)
        else:
            dungeon.enemies.append(
                Enemy(
                    enemy.name,
                    enemy.hp,
                    enemy.attack,
                    enemy.xp_reward,
                    enemy.coin_reward,
                    enemy.defense,
                    enemy.agility,
                )
            )

    # Verificar se a dungeon está vazia
    if not dungeon.enemies and not dungeon.has_boss():
        print(f"{Colors.YEL}⚠️ Esta dungeon está vazia!")
        sleep(1)
        return

    while True:
        clear_screen()
        print(f"{Colors.MAG}===== {dungeon.name} =====")
        print(f"{Colors.WHI}O que você deseja fazer?")
        print(f"{Colors.LBLU}1. Explorar mais")
        print(f"2. Ver status")
        print(f"3. Usar item")
        print(f"4. Voltar")
        choice = input("> ")

        if choice == "1":
            # Chance de encontrar inimigo ou chefe
            roll = roll_check()
            if roll > 15:
                if dungeon.has_boss() and roll > 18:
                    print(f"{Colors.RED}⚠️ Você encontrou o chefe da dungeon!")
                    sleep(1)
                    fight = Fight()
                    fight.start(player, dungeon.boss)
                    if not player.is_alive():
                        return
                    if not dungeon.boss.is_alive():
                        print(
                            f"{Colors.MAG}🎉 Você derrotou o chefe da {dungeon.name}!"
                        )
                        # Verificar drops lendários
                        if dungeon.boss.item_reward:
                            for item in dungeon.boss.item_reward:
                                print(
                                    f"{Colors.MAG}✨ Você encontrou um item lendário: {item['name']}!"
                                )
                                player.add_item(item, item["type"])
                        sleep(1)
                        dungeon.remove_boss()
                else:
                    enemy = dungeon.get_enemy()
                    if enemy:
                        fight = Fight()
                        fight.start(player, enemy)
                        if not player.is_alive():
                            return
            else:
                # Chance de encontrar item
                if roll_check(sides=100) > (100 - BASE_ITEM_CHANCE):
                    # Chance de encontrar item raro
                    if roll_check(sides=100) > (100 - RARE_ITEM_CHANCE):
                        items = [
                            item
                            for item in DUNGEON_ITEMS[dungeon.level]
                            if item.get("rarity") == "raro"
                        ]
                    else:
                        items = [
                            item
                            for item in DUNGEON_ITEMS[dungeon.level]
                            if item.get("rarity") != "raro"
                        ]

                    # Calcular chance total de drop
                    total_chance = sum(item["chance"] for item in items)
                    roll = roll_check(mod=0, sides=total_chance)

                    # Encontrar o item baseado na chance
                    current_chance = 0
                    for item in items:
                        current_chance += item["chance"]
                        if roll <= current_chance:
                            print(
                                f"{Colors.GRE}🎁 Você encontrou um item: {item['name']}!"
                            )
                            if item.get("rarity") == "raro":
                                print(f"{Colors.MAG}✨ É um item raro!")
                            player.add_item(item, item["type"])
                            break
                    sleep(1)
                else:
                    print(f"{Colors.GRE}Você explorou a área e não encontrou nada...")
                    sleep(1)

        elif choice == "2":
            clear_screen()
            print(player)
            input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")

        elif choice == "3":
            player.show_inventory(use=True)

        elif choice == "4":
            clear_screen()
            print(f"{Colors.GRE}Voltando para a cidade...")
            sleep(1)
            return

        else:
            print(f"{Colors.RED}[x] Escolha inválida!")
            sleep(1)


def house_menu(player):
    if not hasattr(player, "house"):
        player.house = House(player)

    while True:
        clear_screen()
        print(f"{Colors.MAG}🏠 Minha Casa")
        print(f"{Colors.WHI}O que você deseja fazer?")
        print(f"{Colors.LBLU}1. Ver status da casa")
        print(f"2. Melhorar salas")
        print(f"3. Preparar poções")
        print(f"4. Criar itens")
        print(f"5. Dormir")
        print(f"6. Colher do jardim")
        print(f"7. Voltar")
        choice = input("> ")

        if choice == "1":
            player.house.show_status()
        elif choice == "2":
            clear_screen()
            print(f"{Colors.MAG}Melhorar Salas")
            print(f"{Colors.WHI}Qual sala você deseja melhorar?")
            for room, level in player.house.rooms.items():
                cost = player.house.upgrade_costs[room] * level
                print(f"{Colors.LBLU}{room.title()}: Nível {level} - {cost} moedas")
            room = input("\nDigite o nome da sala (ou Enter para voltar):\n> ").lower()
            if room:
                player.house.upgrade_room(room)
                input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")
        elif choice == "3":
            clear_screen()
            print(f"{Colors.MAG}Preparar Poções")
            print(f"{Colors.WHI}Qual poção você deseja preparar?")
            for recipe in player.house.recipes["potions"]:
                ingredients = ", ".join(
                    player.house.recipes["potions"][recipe]["ingredients"]
                )
                print(f"{Colors.LBLU}{recipe}: {ingredients}")
            recipe = input("\nDigite o nome da poção (ou Enter para voltar):\n> ")
            if recipe:
                player.house.brew_potion(recipe)
                input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")
        elif choice == "4":
            clear_screen()
            print(f"{Colors.MAG}Criar Itens")
            print(f"{Colors.WHI}Qual item você deseja criar?")
            for recipe in player.house.recipes["crafting"]:
                ingredients = ", ".join(
                    player.house.recipes["crafting"][recipe]["ingredients"]
                )
                print(f"{Colors.LBLU}{recipe}: {ingredients}")
            recipe = input("\nDigite o nome do item (ou Enter para voltar):\n> ")
            if recipe:
                player.house.craft_item(recipe)
                input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")
        elif choice == "5":
            clear_screen()
            print(f"{Colors.MAG}Dormir")
            hours = input(f"{Colors.WHI}Quantas horas você deseja dormir?\n> ")
            try:
                hours = int(hours)
                if hours > 0:
                    player.house.sleep(hours)
                else:
                    print(f"{Colors.RED}[x] Horas inválidas!")
            except ValueError:
                print(f"{Colors.RED}[x] Entrada inválida!")
            input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")
        elif choice == "6":
            player.house.garden_harvest()
            input(f"{Colors.LBLU}[i] Pressione Enter para continuar.")
        elif choice == "7":
            return
        else:
            print(f"{Colors.RED}[x] Escolha inválida!")
            sleep(1)


if __name__ == "__main__":
    main_menu()
