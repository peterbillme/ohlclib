"""
This file offer quotes related time functions
"""
from datetime import datetime

def week_end():
    """
    return True if time is between 19:00 on Friday and 14:00 on Sunday
    """
    # monday is 0, sunday is 6
    _weekday = datetime.today().weekday()
    _result = False
    if _weekday == 4:
        if datetime.today().hour >= 19:
            _result = True
    elif _weekday == 5:
        _result = True
    elif _weekday == 6:
        if datetime.today().hour <= 14:
            _result = True

    return _result
