from datetime import datetime

from constants import *
from time_util import *

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

def get_respawn_offset(message, command):
    killed_time = command[ARRAY_KILLED_TIME]
    current_time = command[ARRAY_CURRENT_TIME]

    try:
        dt_killed_time = datetime.strptime(killed_time, HOURS_MINUTES_FORMAT)
        dt_current_time = datetime.strptime(current_time, HOURS_MINUTES_FORMAT)
    except ValueError:
        return None, TIME_INPUT_ERROR

    hours_difference = (dt_current_time.hour - dt_killed_time.hour) - 1
    minutes_difference =  (MINUTES_IN_HOUR - dt_killed_time.minute) + dt_current_time.minute

    return (hours_difference * MINUTES_IN_HOUR) + minutes_difference, None

def offset_respawn_window(respawn_window, offset):
    unit = respawn_window[UNIT_INDEX]
    timer = int(respawn_window[:TIME_INDEX])

    timer_in_seconds = convert_timer_to_seconds(timer, unit)
    offset_in_seconds = offset * SECONDS_IN_MINUTE

    return timer_in_seconds - offset_in_seconds

def create_actual_timer(respawn_window):
    unit = respawn_window[UNIT_INDEX]
    timer = int(respawn_window[:TIME_INDEX])

    return convert_timer_to_seconds(timer, unit)