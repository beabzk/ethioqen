from datetime import datetime, timezone, timedelta
from .calendar_conversion import convert_ethiopian_to_gregorian, convert_gregorian_to_ethiopian
from .exceptions import InvalidDateException
from .utils import is_valid_ethiopian_date


def ethiopian_to_unix(e_year, e_month, e_day, eth_hour=0, minute=0, tz_offset=0):
    """Convert Ethiopian date/time to Unix timestamp.
    
    Args:
        e_year (int): Ethiopian year
        e_month (int): Ethiopian month (1-13)
        e_day (int): Ethiopian day
        eth_hour (int, optional): Hour in Ethiopian time (0-23). Defaults to 0.
        minute (int, optional): Minutes (0-59). Defaults to 0.
        tz_offset (int, optional): Timezone offset in hours. Defaults to 0 (UTC).
    
    Returns:
        int: Unix timestamp (seconds since Unix epoch)
    
    Raises:
        InvalidDateException: If the date/time is invalid
    """
    # Validate inputs
    if not is_valid_ethiopian_date(e_year, e_month, e_day):
        raise InvalidDateException(f"Invalid Ethiopian date: {e_year}-{e_month}-{e_day}")
    if not (0 <= eth_hour <= 23):
        raise InvalidDateException(f"Invalid hour: {eth_hour}")
    if not (0 <= minute <= 59):
        raise InvalidDateException(f"Invalid minute: {minute}")
    
    # Convert Ethiopian to Gregorian
    g_year, g_month, g_day = convert_ethiopian_to_gregorian(e_year, e_month, e_day)
    
    # Create datetime object
    try:
        dt = datetime(g_year, g_month, g_day, eth_hour, minute, 
                     tzinfo=timezone(timedelta(hours=tz_offset)))
        return int(dt.timestamp())
    except ValueError as e:
        raise InvalidDateException(str(e))


def unix_to_ethiopian(timestamp, tz_offset=0):
    """Convert Unix timestamp to Ethiopian date/time.
    
    Args:
        timestamp (int): Unix timestamp (seconds since Unix epoch)
        tz_offset (int, optional): Timezone offset in hours. Defaults to 0 (UTC).
    
    Returns:
        tuple: (year, month, day, hour, minute)
    """
    # Convert timestamp to datetime
    try:
        dt = datetime.fromtimestamp(timestamp, 
                                  tz=timezone(timedelta(hours=tz_offset)))
    except (ValueError, OSError) as e:
        raise InvalidDateException(f"Invalid timestamp: {timestamp}")
    
    # Convert Gregorian to Ethiopian
    e_year, e_month, e_day = convert_gregorian_to_ethiopian(
        dt.year, dt.month, dt.day)
    
    return e_year, e_month, e_day, dt.hour, dt.minute