# 🐉 Dungeon Awakening RPG

Um RPG de texto por turnos com progressão de personagem, combates em dungeon e sistema de save/load em JSON. Inspirado por títulos como *Solo Leveling* e *Omniscient Reader’s Viewpoint*, esse projeto é focado em aprendizado de Python orientado a objetos e foi feito com a ajuda do ChatGPT com ideias e dúvidas.

---

## 🎮 Funcionalidades

- 🧙 Criação de personagem com evolução de atributos e classes  
- ⚔️ Combate baseado em turnos contra inimigos  
- 💼 Inventário e equipamentos  
- 🗃️ Sistema de salvamento e carregamento de progresso (3 slots)  
- 🛠️ Sistema modular de arquivos para facilitar a expansão do jogo  

---

## 📁 Estrutura do Projeto

```
DungeonRPG/
│
├── data/
│   └── data.json
│
├── src/
│   ├── player.py         # Classe Player e funcionalidades
│   ├── enemy.py          # Classe Enemy
│   ├── fight.py          # Combate entre jogador e inimigo
│   └── utils.py          # Funções utilitárias e SaveManager
│
├── saves/                # Diretório de saves automáticos
│
├── main.py               # Menu principal e loop do jogo
├── README.md
└── requirements.txt      # Bibliotecas necessárias
```

---

## 🚀 Como Rodar

1. **Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/DungeonAwakening.git
cd DungeonAwakening
```

2. **Crie um ambiente virtual (recomendado):**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Inicie o jogo:**

```bash
python src/main.py
```

---

## 🧪 Tecnologias

- Python 3.10+
- [`Colorama`](https://pypi.org/project/colorama/) para estilização no terminal

---

## ✅ Próximas melhorias (to-do)

- [ ] Sistema de loja com rotação de estoque  
- [ ] Crafting: fundir 3 itens iguais para criar um de raridade maior  
- [ ] Dungeons com múltiplos andares  
- [ ] Multiplicidade de inimigos e balanceamento de combate  
- [ ] Salvamento automático ao final de cada luta  
- [ ] Sistema de habilidades ativas e passivas  

---

## 🤝 Contribuição

Pull requests são bem-vindas! Sinta-se à vontade para forkar e propor novas ideias. 💡

---

## 📜 Licença

Este projeto é livre para fins educacionais e pessoais. Sinta-se livre para usar como base para seus próprios jogos!

---

> Feito por Felipe Cardoso
