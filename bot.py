import re
import discord
from discord.ext import commands
import pickle
from item import Item
from random import randint
#import asyncio

inventory = []
prefix = '!'
bot = commands.Bot(command_prefix=prefix)
inv_file = 'inv.bot'

def dm_check(ctx):
    return True if 'dungeon master' in ctx.message.author.role.name.lower() else False


@bot.command(pass_context=True)
async def prefix(ctx, pre):
    """changes the prefix of the bot."""
    if dm_check():
        prefix = pre
    else:
        await bot.say('You can not set the prefix of the bot.')

@bot.command(pass_context=True)
async def additem(ctx, title, desc, sell, buy, amt):
    """addes item to the inventory"""
    if dm_check():
        pickle.load(inv_file) # loads from file
        inventory.append(Item(title, desc, sell, buy, amt))
        pickle.dump(inventory, inv_file) # dumps datat in file
        await bot.say('added {0} to the inventory.'.format(title))
    else:
        await bot.say('You can not add an item to the inventory.')

@bot.command(pass_context=True)
async def rmitem(ctx, title, amt):
    """removes item(s) from the inventory."""
    if dm_check():
        pickle.load(inv_file)
        for x in range(len(inventory)):
            if title == inventory[x].title:
                for y in range(amt):
                    inventory[x].amount -= 1
                    if inventory[x].amount < 1:
                        del inventory[x]
                        break
        pickle.dump(inventory, inv_file)
        await bot.say('Removed {0} {1}(s) from the inventory.'.format(amt, title))
    else:
        await bot.say('You can not remove an item to the inventory.')
            

@bot.command(pass_context=True)
async def lsinv(ctx):
    """lists the inventory."""
    string = ''
    for item in inventory:
        string += '''title: {0.title} desc: {0.description}
            sell: {0.sell} buy: {0.buy} amount: {0.amount}\n'''.format(item)
    await bot.say(string)

@bot.command(pass_context=True)
async def roll(ctx, *args):
    """roll a dice of designated sides."""
    sides = 20
    numDice = 1
    mod_msg = ""
    mods = []
    adv = ""
    rolls = []
    adv_msg = ""
    force_crit = 0

    for arg in args:
        if re.match(r"^(([1-9]*)d[^i])", arg):
            if arg.startswith('d'):
                sides = int(arg[1:])
            else:
                i = arg.index('d')
                numDice = int(arg[0:i])
                sides = int(arg[i + 1:])
        elif '+' in arg or '-' in arg:
            mods.append(str(arg))
        elif 'adv' in arg or 'dis' in arg:
            adv = arg
        elif arg == 'force crit':
            force_crit = 1
        elif arg == 'force fail':
            force_crit = -1
        else:
            print('Invalid argument discarded')

    for _ in range(numDice):
        roll = 0
        if adv == "":
            roll = randint(1,sides)
        elif adv == "adv" or adv == "advantage":
            roll = rollWithAdv(sides)
            adv_msg = " with advantage"
        elif adv == "dis" or adv == "disadvantage":
            roll = rollWithAdv(sides, dis=True)
            adv_msg = " with disadvantage"
        else:
            await bot.say('Invalid argument! Try "adv" or "dis"')

        if force_crit > 0:
            roll = sides
        elif force_crit < 0:
            roll = 1
        rolls.append(roll)

    if numDice == 1:
        result = rolls[0]
        for mod in mods:
            result += int(mod)
    else:
        result = 0
        for roll in rolls:
            result += roll
        for mod in mods:
            result += int(mod)

    min_total = "total"

    if result < 1:
        result = 1
        min_total = "minimum"

    if len(mods) == 0:
        mod_msg = "no modifiers"
    elif len(mods) == 1:
        mod_msg = mods[0]
    else:
        mod_msg = printableArray(mods)

    if numDice > 1:
        await bot.say(f'{ctx.message.author.mention} rolled {numDice} d{sides}s and got {printableArray(rolls)}{adv_msg} with {mod_msg} for a {min_total} of **{result}**.')
    elif rolls[0] == sides and sides == 20:
        await bot.say(f'{ctx.message.author.mention} **crit{adv_msg}** on a d{sides} with {mod_msg} for a {min_total} of **{result}**!')
    elif rolls[0] == 1 and sides == 20:
        await bot.say(f'{ctx.message.author.mention} rolled a **nat 1{adv_msg}** on a d{sides} with {mod_msg} for a {min_total} of **{result}**.')
    else:
        await bot.say(f'{ctx.message.author.mention} rolled {rolls[0]}{adv_msg} on a d{sides} with {mod_msg} for a {min_total} of **{result}**.')
   
def rollWithAdv(sides, dis=False):
    result = 0
    rollOne = randint(1,sides)
    rollTwo = randint(1,sides)

    if not dis:
        result = rollOne if rollOne > rollTwo else rollTwo
    if dis:
        result = rollOne if rollOne < rollTwo else rollTwo

    return result
        
def printableArray(arr):
    result = ""

    for i in range(len(arr)):
        if i < (len(arr) - 2):
            result += f'{arr[i]}'
            result += ', '
        elif i == (len(arr) - 2):
            result += f'{arr[i]}'
        else:
            result += f' and {arr[i]}'

    return result

try:
    file = open('secret.bot', 'r')
    token = file.readline()
    file.close()
    client = discord.Client()
    bot.run(token)
except Exception as error:
    print('Something went wrong ¯\_(ツ)_/¯')
    print(error)
    print(error.args)
finally:
    print('End of Bot.')

