# DiscordDiceBot

A Discord bot that allows users to roll dice using custom expressions like \1d20+4\, supporting multiple rolls and initiative tracking for tabletop RPGs.

## Features

- Dice rolling with support for expressions like \2d6+1d4+3\
- Highlight for critical rolls (natural 1 and max face)
- Multiple rolls with \#\ notation (e.g., \3#1d20+2\)
- Initiative tracker with tie-breaking by natural 20, modifier, then total
- Simple and clean Discord bot commands with error handling

## Commands

- \!r 1d20+4\: Roll a dice expression.
- \!r 3#1d6+2\: Roll the same expression multiple times.
- \!initiative\: Start a new initiative round.
- \!add <name> <roll>\: Add a player to the initiative.
- \!list\: List current initiative order.
- \!remove <name>\: Remove a player from initiative.

## Setup

1. Create a Discord bot and copy the token.
2. Replace your token in \DiscordDiceBot.py\.
3. Run the bot with Python 3.10+ and dependencies installed.

## Requirements

- Python 3.10+
- \discord.py\ library

## License

MIT
