from .exceptions import InvalidDateException
from .utils import is_valid_ethiopian_date, DAYS_IN_ETH_MONTH

def is_ethiopian_leap_year(year):
    return year % 4 == 3

def is_gregorian_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def _ethiopian_to_jdn(year, month, day):
    """Convert Ethiopian date to Julian Day Number."""
    if not is_valid_ethiopian_date(year, month, day):
        raise InvalidDateException(f"Invalid Ethiopian date: {year}-{month}-{day}")
    
    ethiopian_epoch = 1723856
    year_days = (year * 365) + (year // 4)
    month_days = (month - 1) * 30
    
    return ethiopian_epoch + year_days + month_days + day - 1

def _jdn_to_ethiopian(jdn):
    """Convert Julian Day Number to Ethiopian date."""
    ethiopian_epoch = 1723856
    days_since_epoch = jdn - ethiopian_epoch

    # Calculate initial year estimate
    year = int((days_since_epoch - 0.25) // 365.25)
    
    # Calculate remaining days
    year_days = year * 365 + year // 4
    remaining_days = days_since_epoch - year_days
    
    # If we're past the end of the year, increment
    if remaining_days >= 366 or (remaining_days >= 365 and not is_ethiopian_leap_year(year)):
        year += 1
        year_days = year * 365 + year // 4
        remaining_days = days_since_epoch - year_days
    
    # Calculate month and day
    month = int(remaining_days // 30) + 1
    day = int(remaining_days % 30) + 1
    
    # Handle pagume
    if month > 13:
        month = 13
        day = remaining_days - 360 + 1
        
    # Handle year transitions
    max_pagume_days = 6 if is_ethiopian_leap_year(year) else 5
    if month == 13 and day > max_pagume_days:
        year += 1
        month = 1
        day = day - max_pagume_days
    
    return int(year), int(month), int(day)

def _gregorian_to_jdn(year, month, day):
    """Convert Gregorian date to Julian Day Number."""
    if month <= 2:
        year -= 1
        month += 12
    
    a = year // 100
    b = 2 - a + (a // 4)
    
    jdn = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524
    return jdn

def _jdn_to_gregorian(jdn):
    """Convert Julian Day Number to Gregorian date."""
    y = 4716
    j = 1401
    m = 2
    n = 12
    r = 4
    p = 1461
    v = 3
    u = 5
    s = 153
    w = 2
    B = 274277
    C = -38

    f = jdn + j + (((4 * jdn + B) // 146097) * 3) // 4 + C
    e = r * f + v
    g = (e % p) // r
    h = u * g + w
    
    day = (h % s) // u + 1
    month = ((h // s + m) % n) + 1
    year = (e // p) - y + (n + m - month) // n
    
    return year, month, day

def convert_ethiopian_to_gregorian(eth_year, eth_month, eth_day):
    """Convert an Ethiopian date to Gregorian."""
    if not is_valid_ethiopian_date(eth_year, eth_month, eth_day):
        raise InvalidDateException(f"Invalid Ethiopian date: {eth_year}-{eth_month}-{eth_day}")
    
    jdn = _ethiopian_to_jdn(eth_year, eth_month, eth_day)
    return _jdn_to_gregorian(jdn)

def convert_gregorian_to_ethiopian(greg_year, greg_month, greg_day):
    """Convert a Gregorian date to Ethiopian."""
    if greg_month < 1 or greg_month > 12:
        raise InvalidDateException(f"Invalid Gregorian month: {greg_month}")
    if greg_day < 1 or greg_day > 31:
        raise InvalidDateException(f"Invalid Gregorian day: {greg_day}")
        
    jdn = _gregorian_to_jdn(greg_year, greg_month, greg_day)
    return _jdn_to_ethiopian(jdn)