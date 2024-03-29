import discord
import asyncio
import os

from constants import *
from respawn_window_helper import *
from message_helper import *
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

    if message.content.startswith(COMMAND_KEY):
        try:
            original_message, boss_name, actual_respawn_window = await process_input(message)
        except ValueError:
            return

        await countdown(original_message, boss_name, actual_respawn_window)

async def process_input(message):
    command = message.content.split(' ')
    if len(command) > CMD_TIME_INPUT_LENGTH:
        await message.channel.send(create_message(str(message.content), UNSUPPORTED_COMMAND))
        raise ValueError(UNSUPPORTED_COMMAND)

    if len(command) == CMD_TIME_INPUT_LENGTH:
        try:
            boss_name, actual_respawn_window = await handle_time_input(message, command)
        except ValueError:
            raise ValueError
    else:
        try:
            boss_name, actual_respawn_window = await handle_default_input(message)
        except ValueError:
            raise ValueError

    original_message = await send_initial_message(message, actual_respawn_window, boss_name)
    return original_message, boss_name, actual_respawn_window

async def handle_time_input(message, command):
    boss_name = get_boss_name(command[ARRAY_BOSS_NAME])
    respawn_window = get_respawn_window(boss_name)

    time_difference, error = get_respawn_offset(message, command)
    if error is not None:
        await message.channel.send(create_message(str(message.content), error))
        raise ValueError(error)

    actual_respawn_window = offset_respawn_window(respawn_window, time_difference)

    return boss_name, actual_respawn_window

async def handle_default_input(message):
    boss_name = get_boss_name(message.content)
    respawn_window = get_respawn_window(boss_name)

    try:
        actual_respawn_window = create_actual_timer(respawn_window)
    except ValueError:
        await message.channel.send(create_message(boss_name, BOSS_INPUT_ERROR))
        raise ValueError(BOSS_INPUT_ERROR)

    return boss_name, actual_respawn_window

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

client.run(os.environ.get('TOKEN'))
#client.run(SECRET_TOKEN)
