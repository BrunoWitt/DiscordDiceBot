# DiscordDiceBot
A Discord bot built to manage RPG-style initiative rolls with advanced sorting logic. Supports rolling dice expressions, multiple rolls, and managing turn order with priority given to natural 20 rolls, modifiers, and total scores.

# Dice rolls bot

A Discord bot built to manage RPG-style initiative rolls with advanced sorting logic.  
Supports rolling dice expressions, multiple rolls, and managing turn order with priority given to natural 20 rolls, modifiers, and total scores.

---

## Features

- Roll dice expressions (e.g., `1d20+4`, `2d6+3`)  
- Support for multiple rolls at once (e.g., `3#1d20+2`)  
- Custom initiative management with commands to add, list, and remove players  
- Initiative order prioritizes:  
  1. Natural 20 on d20 rolls  
  2. Higher modifiers  
  3. Higher total roll  
- Clear and detailed roll results in chat messages

---

## Commands

| Command                  | Description                          | Example                |
|--------------------------|------------------------------------|------------------------|
| `!r <dice>`              | Roll dice expression                | `!r 1d20+4`            |
| `!r <times>#<dice>`      | Roll multiple times                 | `!r 3#1d20+2`          |
| `!initiative`            | Start a new initiative round       | `!initiative`          |
| `!add <name> <dice>`     | Add player to initiative            | `!add Bruno 1d20+3`    |
| `!list`                  | Show current initiative order      | `!list`                |
| `!remove <name>`         | Remove player from initiative       | `!remove Bruno`        |

---

## Requirements

- Python 3.10 or higher  
- [discord.py](https://discordpy.readthedocs.io/en/stable/) library  
- Internet connection for Discord API access

---

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/odio-initiative-bot.git
   cd odio-initiative-bot
