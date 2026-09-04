from datetime import datetime, timedelta, timezone

from .calendar_conversion import (
    convert_ethiopian_to_gregorian,
    convert_gregorian_to_ethiopian,
)
from .exceptions import InvalidDateException
from .time_conversion import eth_to_24h, h24_to_eth
from .utils import is_valid_ethiopian_date


def ethiopian_to_unix(
    e_year, e_month, e_day, eth_hour=12, minute=0, is_pm=False, tz_offset=0
):
    """Convert Ethiopian date/time to Unix timestamp.

    Args:
        e_year (int): Ethiopian year
        e_month (int): Ethiopian month (1-13)
        e_day (int): Ethiopian day
        eth_hour (int, optional): Hour in Ethiopian 12-hour time (1-12). Defaults to 12.
        minute (int, optional): Minutes (0-59). Defaults to 0.
        is_pm (bool, optional): Whether the time is PM. Defaults to False.
        tz_offset (int, optional): Timezone offset in hours. Defaults to 0 (UTC).

    Returns:
        int: Unix timestamp (seconds since Unix epoch)
    """
    if not is_valid_ethiopian_date(e_year, e_month, e_day):
        raise InvalidDateException(
            f"Invalid Ethiopian date: {e_year}-{e_month}-{e_day}"
        )
    if not (0 <= minute <= 59):
        raise InvalidDateException(f"Invalid minute: {minute}")

    # Convert Ethiopian 12-hour time to 24-hour time
    hour_24 = eth_to_24h(eth_hour, is_pm)

    # Convert to Gregorian and create timestamp
    g_year, g_month, g_day = convert_ethiopian_to_gregorian(e_year, e_month, e_day)
    try:
        dt = datetime(
            g_year,
            g_month,
            g_day,
            hour_24,
            minute,
            tzinfo=timezone(timedelta(hours=tz_offset)),
        )
        return int(dt.timestamp())
    except ValueError as e:
        raise InvalidDateException(str(e)) from e


def unix_to_ethiopian(timestamp, tz_offset=0):
    """Convert Unix timestamp to Ethiopian date/time.

    Args:
        timestamp (int): Unix timestamp (seconds since Unix epoch)
        tz_offset (int, optional): Timezone offset in hours. Defaults to 0 (UTC).

    Returns:
        tuple: (year, month, day, hour, minute, is_pm)
            hour will be in 12-hour format (1-12)
            is_pm indicates whether the time is PM
    """
    try:
        dt = datetime.fromtimestamp(timestamp, tz=timezone(timedelta(hours=tz_offset)))
    except (ValueError, OSError) as e:
        raise InvalidDateException(f"Invalid timestamp: {timestamp}") from e

    # Convert to Ethiopian date
    e_year, e_month, e_day = convert_gregorian_to_ethiopian(dt.year, dt.month, dt.day)

    # Convert 24-hour time to Ethiopian 12-hour time
    eth_hour, is_pm = h24_to_eth(dt.hour)

    return e_year, e_month, e_day, eth_hour, dt.minute, is_pm
