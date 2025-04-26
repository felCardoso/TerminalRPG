# Dungeon RPG - Terminal

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
- 🏠 Sistema de criação de casa e ugrades
- 🗃️ Sistema de salvamento e carregamento de progresso (3 slots)
- 🛠️ Sistema modular de arquivos para facilitar a expansão do jogo

---

## 📁 Estrutura do Projeto

```
DungeonRPG/
│
├── saves/                # Diretório de saves automáticos
│
├── src/
│   ├── enemy.py          # Classe Enemy e Dungeon e Subclasse Boss
│   ├── fight.py          # Combate entre jogador e inimigo
│   ├── house.py          # Classe House e funções da casa
│   ├── player.py         # Classe Player e funcionalidades
│   └── utils.py          # Funções utilitárias, SaveManager e Constantes
│
├── game.py               # Menus e loop principal do jogo
├── README.md
└── requirements.txt      # Bibliotecas necessárias
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
- [ ] 

---

## 🤝 Contribuição

Pull requests são bem-vindas! Sinta-se à vontade para forkar e propor novas ideias. 💡

---

## 📜 Licença

Este projeto é livre para fins educacionais e pessoais. Sinta-se livre para usar como base para seus próprios jogos!

---

> Feito por Felipe Cardoso
