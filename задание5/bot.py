import discord
from discord import Client
from discord.ext import commands
from api_requests import ApiRequests

config = {
    'token': 'ВАШ ТОКЕН',
    'prefix': '!'
}

bot = commands.Bot(command_prefix=config['prefix'])


@bot.command()
async def get_task(ctx, *args):
    api_requests = ApiRequests(usernames=args)
    task = api_requests.get_task()

    text = f'Могут попробовать задачку {task["name"]}\n' \
           f'URL --> https://codeforces.com/problemset/problem/{task["id"]}/{task["index"]}'

    await ctx.send(text)


bot.run(config['token'])
