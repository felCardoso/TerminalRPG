# Dungeon RPG (Terminal Game em Python)

Um RPG de texto por turnos com progressão de personagem, combates em dungeon e sistema de save/load em JSON. Esse projeto é focado em aprendizagem de Python orientado a objetos e foi feito com a ajuda do ChatGPT com ideias, dúvidas e este README :).

---

## 🎮 Funcionalidades

- 🧙 Criação de personagem com evolução de atributos
- ⚔️ Combate baseado em turnos contra inimigos
- 🔥 Habilidades de combate
- 🧌 Dungeons, bosses, inimigos e itens para encontrar
- ⏳ Sistema de passagem de tempo e deslocamento para as dungeons
- 💼 Inventário e equipamentos
- 🪙 Sistema de moedas e loja
- 🏠 Sistema de criação de casa e upgrades
- 🗃️ Sistema de salvamento e carregamento de progresso (3 slots)
- 🛠️ Sistema modular de arquivos para facilitar a expansão do jogo

---

## 📁 Estrutura do Projeto

```
TerminalRPG/
│
├── saves/                # Saved Games
│
├── src/
│   ├── combat/           # Combat Logic
│   │   └── combat.py
│   │
│   ├── entities/
│   │   ├── enemy.py      # Enemy / Boss(Enemy)
│   │   └── player.py     # Player / House / Room
│   │
│   ├── locations/
│   │   ├── dungeon.py    # Dungeon
│   │   └── world.py      # City / Guild / Shop / NPCs
│   │
│   ├── utils/
│   │   ├── codex.py      # Codex (Items, Enemies, Dungeons, Cities, NPCs, Shops, ...)
│   │   ├── core.py       # DungeonManager, SaveManager, Colors, Constants and General Functions
│   │   ├── item.py       # Item / Potion(Item) / Weapon(Item) / Armor(Item) / Accessory(Item)
│   │   └── menu.py       # Menus (BaseMenu, CityMenu, AdventureMenu, ShopMenu, ...)
│
├── game.py               # Main game loop
├── README.md
└── requirements.txt      # Colorama install
```

---

## 🚀 Como Executar o jogo

1. **Clone o repositório:**

```bash
git clone https://github.com/felCardoso/TerminalRPG.git
cd TerminalRPG
```

2. **Crie um ambiente virtual (recomendado):**

```bash
python -m venv rpg-venv
rpg-venv\Scripts\activate     # Windows
source rpg-venv/bin/activate  # Linux/Mac
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Inicie o jogo:**

```bash
python game.py
```

---

## 🧪 Tecnologias

- Python 3.10+
- [`Colorama`](https://pypi.org/project/colorama/) para estilização no terminal

---

## ✅ Próximas melhorias (to-do)

- [ ] Crafting
- [ ] Balanceamento de Combate e XP
- [ ] Menu de Configurações
- [ ] Salvamento automático ao final de cada luta (Habilitável)
- [ ] Sistema de habilidades ativas e passivas
- [ ] Melhorias no sistema de Housing
- [ ] Exemplo de execução do jogo no README / Badges (Linguagem, Licença e Status de Build) para tornar o README mais visual

---

## 🤝 Contribuição

Pull requests são bem-vindas! Sinta-se à vontade para forkar e propor novas ideias. 💡

---

## 📜 Licença

Este projeto é livre para fins educacionais e pessoais. Sinta-se livre para usar como base para seus próprios jogos!

---

> Feito por Felipe Cardoso
