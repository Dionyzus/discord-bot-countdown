import discord
import asyncio
import os
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
    
    boss = ''
    respawn_window = 0
    if message.content.startswith(COMMAND_KEY):
        boss, respawn_window = get_respawn_window(message)
        original_message = await message.channel.send(create_message(boss, RS_STARTS_IN, respawn_window))

        await countdown(original_message, respawn_window, boss)

def get_respawn_window(boss_name):
    boss_name = boss_name.content[BOSS_NAME_INDEX:]
    boss_exists = False
    respawn_window = ''

    for key in BOSSES:
        if boss_name in BOSSES[key]:
            boss_exists = True
            respawn_window = key
            break
    
    if (boss_exists == False):
        return BOSS_INPUT_ERROR

    return boss_name, respawn_window

@client.event
async def countdown(message, respawn_window, boss):
    unit = respawn_window[UNIT_INDEX]
    timer = int(respawn_window[:TIME_INDEX])

    timer = convert_timer_to_seconds(timer, unit)

    while True:
        if timer > SECONDS_IN_HOUR:
            timer = await handle_hours_countdown(message, timer, SECONDS_IN_HOUR, boss)
        elif timer > SECONDS_IN_MINUTE:
            timer = await handle_minutes_countdown(message, timer, SECONDS_IN_MINUTE, boss)
        else:
            countdown_done = await handle_seconds_countdown(message, timer, TEN_SECONDS, boss)
            if countdown_done == True:
                return

def convert_timer_to_seconds(timer, unit):
    if unit == SECONDS:
        return timer
    if unit == MINUTES:
        return timer * SECONDS_IN_MINUTE

    return timer * SECONDS_IN_HOUR

async def handle_hours_countdown(message, timer, sleepTime, boss):
    if timer - sleepTime < 0:
        handle_minutes_countdown(message, timer, SECONDS_IN_MINUTE, boss)

    return await update_timer(message, timer, sleepTime, boss, HOURS, SECONDS_IN_HOUR)

async def handle_minutes_countdown(message, timer, sleepTime, boss):
    if timer - sleepTime < 0:
        handle_seconds_countdown(message, timer, 10, boss)

    return await update_timer(message, timer, sleepTime, boss, MINUTES, SECONDS_IN_MINUTE)

async def handle_seconds_countdown(message, timer, sleepTime, boss):
    while True:
        if timer - sleepTime < 0:
            sleepTime = timer

        await asyncio.sleep(sleepTime)
        timer-=sleepTime

        if timer <= 0:
            await message.delete()
            await message.channel.send(create_message(boss, RS_STARTED))
            return True

        await message.edit(content=create_message(boss, RS_STARTS_IN, str(timer), SECONDS))

async def update_timer(message, timer, sleepTime, boss, unit, divisor):
    await asyncio.sleep(sleepTime)
    timer-=sleepTime

    display_timer = timer // divisor

    await message.edit(content=create_message(boss, RS_STARTS_IN, str(display_timer), unit))

    return timer

def create_message(*args):
    return ' '.join(args)

client.run(os.environ.get('TOKEN'))
#client.run(SECRET_TOKEN)
