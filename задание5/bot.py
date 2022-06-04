import discord
from discord import Client
from discord.ext import commands
from api_requests import ApiRequests

config = {
    'token': 'OTgyNjY1NTU2OTYyNDcxOTk4.G326Lt.IkpEBP5A5WFp8dqUp8_nWxD7z0cFXm16bNVbvE',
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
