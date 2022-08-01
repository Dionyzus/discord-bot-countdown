SECRET_TOKEN = 'here-goes-token'

COMMAND_KEY = '$'
RS_STARTS_IN = 'respawn window starts in:'
RS_STARTED = 'respawn window started!'
BOSS_INPUT_ERROR = 'Wrong boss value'
TIME_INPUT_ERROR = 'Passed wrong time values, must be HH:MM format, e.g. 9:15 10:00'
UNSUPPORTED_COMMAND = 'Unsuppored command input, view README.md'

GOD_BOSSES = ['ogre', 'manti', 'bd', 'bapho', 'od', 'ds', 'behe']
DEMI_BOSSES = ['bKing', 'uwc1', 'uwc2', 'mandra', 'plant', 'yQueen', 'balze8', 'balze9', 'balze10']
MINI_BOSSES = ['gQueen', 'impKing', 'lizLead', 'tarenLead', 'kingC', 'tdl', 'eQueen', 'furAnt']
BOSSES = {
    '24h': GOD_BOSSES,
    '12h': DEMI_BOSSES,
    '40m': MINI_BOSSES
}

HOURS = 'h'
MINUTES = 'm'
SECONDS = 's'
HOURS_MINUTES_FORMAT = '%H:%M'

MINUTES_IN_HOUR = 60

HOURS_IN_DAY = 24
SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60
TEN_SECONDS = 10

BOSS_NAME_INDEX = 1
UNIT_INDEX = -1
TIME_INDEX = 2

ARRAY_BOSS_NAME = 0
ARRAY_KILLED_TIME = 1
ARRAY_CURRENT_TIME = 2

CMD_TIME_INPUT_LENGTH = 3