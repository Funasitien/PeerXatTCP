import curses

class color:
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    reset = '\033[0m'

class theme:
    classic = (curses.COLOR_WHITE, curses.COLOR_BLACK)
    matrix = (curses.COLOR_GREEN, curses.COLOR_BLACK)