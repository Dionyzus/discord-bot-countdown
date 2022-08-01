from constants import *

def convert_timer_to_seconds(timer, unit):
    if unit == SECONDS:
        return timer
    if unit == MINUTES:
        return timer * SECONDS_IN_MINUTE

    return timer * SECONDS_IN_HOUR

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