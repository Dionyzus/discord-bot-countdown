import discord
import asyncio

from constants import *
from time_util import *

async def send_initial_message(message, actual_respawn_window, boss_name):
    hours, minutes = convert_hour_minutes(actual_respawn_window)
    return await message.channel.send(create_message(boss_name, RS_STARTS_IN, str(hours) + HOURS, str(minutes) + MINUTES))

async def update_timer(message, timer, sleepTime, boss):
    await asyncio.sleep(sleepTime)
    timer-=sleepTime

    hours, minutes = convert_hour_minutes(timer)
    await edit_message(message, create_message(create_message(boss, RS_STARTS_IN, str(hours) + HOURS, str(minutes) + MINUTES)))

    return timer

async def edit_message(message, message_content):
    try:
        await message.edit(content=message_content)
    except discord.errors.NotFound:
        return

async def delete_and_send_new(message, new_message):
    try:
        await message.delete()
        await message.channel.send(new_message)
        return True
    except (discord.errors.NotFound, discord.errors.HTTPException): 
        return

def create_message(*args):
    return ' '.join(args)