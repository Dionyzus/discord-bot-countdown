import discord
import asyncio
import os
import time
from datetime import datetime
from constants import *
from dotenv import load_dotenv

load_dotenv('.env')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    actual_respawn_window = ''
    hours_difference = 0
    time_difference = 0

    if message.content.startswith(COMMAND_KEY):
        command = message.content.split(' ')
        if len(command) == CMD_TIME_INPUT_LENGTH:
            boss_name = get_boss_name(command[ARRAY_BOSS_NAME])
            respawn_window = get_respawn_window(boss_name)

            time_difference = handle_time_input(message, command)
            actual_respawn_window = offset_respawn_window(respawn_window, time_difference)

            original_message = await send_initial_message(message, actual_respawn_window, boss_name)
        else:
            boss_name = get_boss_name(message.content)
            respawn_window = get_respawn_window(boss_name)
            actual_respawn_window = create_actual_timer(respawn_window)

            original_message = await send_initial_message(message, actual_respawn_window, boss_name)
        try:
            await countdown(original_message, boss_name, actual_respawn_window)
        except ValueError:
            await message.channel.send(create_message(boss_name, BOSS_INPUT_ERROR))
            return

async def send_initial_message(message, actual_respawn_window, boss_name):
    hours, minutes = convert_hour_minutes(actual_respawn_window)
    return await message.channel.send(create_message(boss_name, RS_STARTS_IN, str(hours) + HOURS, str(minutes) + MINUTES))

def create_actual_timer(respawn_window):
    unit = respawn_window[UNIT_INDEX]
    timer = int(respawn_window[:TIME_INDEX])

    return convert_timer_to_seconds(timer, unit)

def offset_respawn_window(respawn_window, offset):
    unit = respawn_window[UNIT_INDEX]
    timer = int(respawn_window[:TIME_INDEX])

    timer_in_seconds = convert_timer_to_seconds(timer, unit)
    offset_in_seconds = offset * SECONDS_IN_MINUTE

    return timer_in_seconds - offset_in_seconds

def handle_time_input(message, command):
    killed_time = command[ARRAY_KILLED_TIME]
    current_time = command[ARRAY_CURRENT_TIME]

    dt_killed_time = datetime.strptime(killed_time, HOURS_MINUTES_FORMAT)
    dt_current_time = datetime.strptime(current_time, HOURS_MINUTES_FORMAT)

    hours_difference = (dt_current_time.hour - dt_killed_time.hour) - 1
    minutes_difference =  (MINUTES_IN_HOUR - dt_killed_time.minute) + dt_current_time.minute

    return (hours_difference * MINUTES_IN_HOUR) + minutes_difference

def get_boss_name(command):
    return command[BOSS_NAME_INDEX:]

def get_respawn_window(boss_name):
    boss_exists = False
    respawn_window = ''

    for key in BOSSES:
        if boss_name in BOSSES[key]:
            boss_exists = True
            respawn_window = key
            break
    
    if (boss_exists == False):
        return boss_name

    return respawn_window

@client.event
async def countdown(message, boss, timer):
    while True:
        if timer is None:
            return
        if timer > SECONDS_IN_HOUR:
            timer = await handle_hours_countdown(message, timer, SECONDS_IN_HOUR, boss)
        elif timer > SECONDS_IN_MINUTE:
            timer = await handle_minutes_countdown(message, timer, SECONDS_IN_MINUTE, boss)
        else:
            countdown_done = await handle_seconds_countdown(message, timer, TEN_SECONDS, boss)
            if countdown_done == True or countdown_done is None:
                return

def convert_timer_to_seconds(timer, unit):
    if unit == SECONDS:
        return timer
    if unit == MINUTES:
        return timer * SECONDS_IN_MINUTE

    return timer * SECONDS_IN_HOUR

async def handle_hours_countdown(message, timer, sleepTime, boss):
    if timer - sleepTime < 0:
        await handle_minutes_countdown(message, timer, SECONDS_IN_MINUTE, boss)

    return await update_timer(message, timer, sleepTime, boss)

async def handle_minutes_countdown(message, timer, sleepTime, boss):
    if timer - sleepTime < 0:
        await handle_seconds_countdown(message, timer, 10, boss)

    return await update_timer(message, timer, sleepTime, boss)

async def handle_seconds_countdown(message, timer, sleepTime, boss):
    while True:
        if timer - sleepTime < 0:
            sleepTime = timer

        await asyncio.sleep(sleepTime)
        timer-=sleepTime

        if timer <= 0:
            await delete_and_send_new(message, create_message(boss, RS_STARTED))

        await edit_message(message, create_message(boss, RS_STARTS_IN, str(timer), SECONDS))

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

def convert_hour_minutes(seconds):
    more_than_hour = False
    if seconds > SECONDS_IN_HOUR:
        more_than_hour = True

    seconds = seconds % (HOURS_IN_DAY * SECONDS_IN_HOUR)
    hours = seconds // SECONDS_IN_HOUR
    seconds %= SECONDS_IN_HOUR
    minutes = seconds // SECONDS_IN_MINUTE
    seconds %= SECONDS_IN_MINUTE

    if hours == 0 and more_than_hour:
        return HOURS_IN_DAY, minutes

    return hours, minutes

def create_message(*args):
    return ' '.join(args)

client.run(os.environ.get('TOKEN'))
#client.run(SECRET_TOKEN)
