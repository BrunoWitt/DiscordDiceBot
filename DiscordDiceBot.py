import discord
from discord.ext import commands
import random
import re

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Rolls dice according to the given expression and returns the total and individual rolls
def roll(dice_expression: str) -> tuple[int, list[str]]:
    """
    Parses and rolls dice based on an expression like '2d6+1d4+3'.
    Returns the total result and a list of formatted individual rolls/modifiers.
    Raises ValueError if dice quantity or faces are less than 1.
    """
    total_result = 0
    rolls = []
    # Split the expression into parts separated by '+' or '-'
    parts = re.findall(r'[+-]?\s*\d*d?\d+', dice_expression)

    for part in parts:
        part = part.replace(' ', '')
        part_no_sign = part.lstrip('+-')
        sign = -1 if part.startswith('-') else 1

        if 'd' in part_no_sign:
            qty_str, faces_str = part_no_sign.split('d')
            qty = int(qty_str) if qty_str else 1
            faces = int(faces_str)

            if qty < 1 or faces < 1:
                raise ValueError("Dice quantity and faces must be greater than 0.")

            for _ in range(qty):
                value = random.randint(1, faces)
                total_result += value * sign

                # Highlight max or min rolls
                if value == faces or value == 1:
                    formatted = f"**{sign * value}**"
                else:
                    formatted = f"{sign * value}"
                rolls.append(formatted)
        else:
            # Modifier or flat number
            value = int(part_no_sign)
            rolls.append(f"{sign * value:+d}")
            total_result += value * sign

    return total_result, rolls

def roll_initiative(expression: str) -> tuple[int, int, int]:
    """
    Rolls initiative from an expression like '1d20+4'.
    Returns a tuple of (total, d20_roll_value, modifier_sum).
    Detects natural 20 if roll is exactly 20 on a single d20.
    """
    parts = re.findall(r'[+-]?\s*\d*d?\d+', expression)
    total = 0
    d20_value = None
    modifier = 0

    for part in parts:
        part = part.replace(' ', '')
        part_no_sign = part.lstrip('+-')
        sign = -1 if part.startswith('-') else 1

        if 'd' in part_no_sign:
            qty_str, faces_str = part_no_sign.split('d')
            qty = int(qty_str) if qty_str else 1
            faces = int(faces_str)
            for _ in range(qty):
                value = random.randint(1, faces)
                total += value * sign
                # Detect natural 20 on a single d20 roll
                if faces == 20 and qty == 1:
                    d20_value = value
        else:
            value = int(part_no_sign)
            total += value * sign
            modifier += value * sign

    return total, d20_value or 0, modifier

async def add_player(ctx: commands.Context, name: str, dice_expression: str) -> None:
    """
    Adds a player to the initiative list with rolled initiative values.
    Sorts the list by:
        1) Natural 20 priority
        2) Higher modifier
        3) Higher total initiative
    """
    total, d20, mod = roll_initiative(dice_expression)
    initiative.append((name, total, d20, mod))
    initiative.sort(key=lambda x: (
        x[2] != 20,   # False < True, so natural 20 first
        -x[3],        # Higher modifier next
        -x[1]         # Then higher total initiative
    ))
    await ctx.send(f"{name} joined with an initiative of {total}.", reference=ctx.message)

async def list_initiative(ctx: commands.Context) -> None:
    """
    Sends a message listing all players currently in the initiative order.
    """
    if not initiative:
        await ctx.send("The initiative list is empty.")
        return
    list_text = "\n".join(f"{i+1}. {name} ({total})" for i, (name, total, _, _) in enumerate(initiative))
    await ctx.send(f"**Initiative Order:**\n{list_text}")

async def remove_player(ctx: commands.Context, name: str) -> None:
    """
    Removes a player from the initiative list by name.
    """
    global initiative
    for player in initiative:
        if player[0].lower() == name.lower():
            initiative.remove(player)
            await ctx.send(f"{name} was removed from initiative.")
            return
    await ctx.send(f"Player '{name}' not found in initiative.")

@bot.event
async def on_ready() -> None:
    """
    Event handler for when the bot has connected to Discord.
    """
    print("Dice is ready to roll!")

@bot.command()
async def r(ctx: commands.Context, dice: str) -> None:
    """
    Rolls dice based on the given expression.
    Supports multiple rolls with '#' separator (e.g., '3#1d20+2').
    Replies with the result and detailed individual rolls.
    """
    try:
        if '#' in dice:
            times_str, expression = dice.split('#')
            times = int(times_str)
            message = []
            for _ in range(times):
                result, rolls = roll(expression)
                message.append(f"{result} <- [{', '.join(rolls)}] {expression}\n")
            await ctx.send("".join(message), reference=ctx.message)
        else:
            result, rolls = roll(dice)
            await ctx.send(f"{result} <- [{', '.join(rolls)}] {dice}\n", reference=ctx.message)
    except Exception as e:
        await ctx.send(f"Error rolling dice: {e}", reference=ctx.message)

@bot.command()
async def initiative(ctx: commands.Context) -> None:
    """
    Starts a new initiative round, clearing any existing players.
    """
    global initiative
    initiative = []
    await ctx.send("Initiative started! Use !add <name> <dice> to add players.")

@bot.command()
async def add(ctx: commands.Context, name: str, dice: str) -> None:
    """
    Adds a player to the initiative using their name and dice expression.
    """
    try:
        await add_player(ctx, name, dice)
    except Exception as e:
        await ctx.send(f"Error adding player: {e}", reference=ctx.message)

@bot.command()
async def list(ctx: commands.Context) -> None:
    """
    Lists all players in the current initiative order.
    """
    await list_initiative(ctx)

@bot.command()
async def remove(ctx: commands.Context, name: str) -> None:
    """
    Removes a player from initiative by name.
    """
    await remove_player(ctx, name)

bot.run("Your Token Here")  # Replace with your bot token
# Make sure to keep your token secure and not share it publicly.
