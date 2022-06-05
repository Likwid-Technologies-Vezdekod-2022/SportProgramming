import csv
import datetime

import asyncio
import time

import discord
from discord import Client
from discord.ext import commands

DAYS_OF_WEEK = {'понедельник': 1, 'вторник': 2, 'среда': 3, 'четверг': 4, 'пятница': 5,
                'суббота': 6, 'воскресенье': 7}

groups = {
    'Group1': {'days_range': 'понедельник - четверг', 'time_range': '20:00 - 22:00',
               'members': 'cirmiuwu#1039,Bankai#6237'},
    'Group2': {'days_range': 'вторник - пятница', 'time_range': '20:00 - 22:00', 'members': 'cirmiuwu#1039'},
    'Group3': {'days_range': 'суббота - понедельник', 'time_range': '16:00 - 18:00',
               'members': 'Bankai#6237,Ktirskikh#8472'}

}

users = {
    'cirmiuwu#1039': {'enter_count': 0},
    'Bankai#6237': {'enter_count': 0},
    'Blackvenon223#5707': {'enter_count': 0},

}

config = {
    'token': 'ВАШ ТОКЕН',
    'prefix': 'prefix'
}

bot = commands.Bot(command_prefix=config['prefix'])


def format_time_range(time_range: str):
    start_hour, end_hour = time_range.strip().split('-')
    start_hour = datetime.time(int(start_hour.split(':')[0]), int(start_hour.split(':')[1]))
    end_hour = datetime.time(int(end_hour.split(':')[0]), int(end_hour.split(':')[1]))

    return start_hour, end_hour


def check_time_range(time_range: str):
    time_range = format_time_range(time_range)
    today = datetime.time()

    if time_range[0] <= time_range[1]:
        return time_range[0] <= today <= time_range[1]
    else:
        return time_range[0] <= today or today <= time_range[1]


def format_days_range(days_range: str):
    start_day, end_day = days_range.strip().split('-')
    start_day = DAYS_OF_WEEK[start_day.strip()]
    end_day = DAYS_OF_WEEK[end_day.strip()]
    return start_day, end_day


def check_days_range(days_range) -> bool:
    days_range = format_days_range(days_range)

    today = datetime.datetime.today().weekday()

    if days_range[1] < days_range[0]:
        if days_range[1] <= today <= days_range[0]:
            return True
        return False
    if days_range[0] <= today <= days_range[1]:
        return True
    return False


def save_log(user_name: str):
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(f'{user_name} -> Посетил занятие')


def check_enter_time(group_name: str, user_name: str):
    end_hour = int(groups[group_name]['time_range'].split('-')[1].strip().split(':')[0])

    if check_days_range(days_range=groups[group_name]['days_range']):
        if check_time_range(groups[group_name]['time_range']):
            users[user_name]['enter_count'] += 1
            while datetime.time() < datetime.time(end_hour):
                time.sleep(1)
                print('Ожидаем конца занятия')
            save_log(user_name)


async def check_enter(user: discord.User, channel: discord.VoiceChannel):
    group = groups[channel.name]
    group_members = group['members'].split(',')
    user_name = f'{user.name}#{user.discriminator}'

    if user_name in group_members:
        check_enter_time(group_name=channel.name, user_name=user_name)


@bot.event
async def on_voice_state_update(member: discord.User, before, after):
    if before.channel is None and after.channel is not None:
        await check_enter(user=member, channel=after.channel)


bot.run(config['token'])
