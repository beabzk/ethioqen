from datetime import datetime, timedelta, timezone

from .calendar_conversion import (
    convert_ethiopian_to_gregorian,
    convert_gregorian_to_ethiopian,
)
from .exceptions import InvalidDateException, InvalidTimeException
from .time_conversion import eth_to_24h, h24_to_eth
from .utils import is_valid_ethiopian_date

__all__ = ["ethiopian_to_unix", "unix_to_ethiopian"]


def ethiopian_to_unix(
    e_year: int,
    e_month: int,
    e_day: int,
    eth_hour: int = 12,
    minute: int = 0,
    is_pm: bool = False,
    tz_offset: float = 0,
    second: int = 0,
) -> int:
    """Convert Ethiopian date/time to Unix timestamp.

    Args:
        e_year: Ethiopian year.
        e_month: Ethiopian month (1-13).
        e_day: Ethiopian day.
        eth_hour: Hour in Ethiopian 12-hour time (1-12). Defaults to 12.
        minute: Minutes (0-59). Defaults to 0.
        is_pm: Whether the time is PM. Defaults to False.
        tz_offset: Timezone offset in hours, may be fractional
            (e.g. 5.5, 5.75). Defaults to 0 (UTC). Named zones
            (e.g. Africa/Addis_Ababa) are future work.
        second: Seconds (0-59). Defaults to 0.

    Returns:
        Unix timestamp (seconds since the Unix epoch).

    Raises:
        InvalidDateException: If the Ethiopian date is invalid.
        InvalidTimeException: If the time components are invalid.

    Example:
        >>> ethiopian_to_unix(2015, 1, 1, 12, 0, False)
        1662876000
    """
    if not is_valid_ethiopian_date(e_year, e_month, e_day):
        raise InvalidDateException(
            f"Invalid Ethiopian date: {e_year}-{e_month}-{e_day}"
        )
    if not 0 <= minute <= 59:
        raise InvalidTimeException(f"Invalid minute: {minute}")
    if not 0 <= second <= 59:
        raise InvalidTimeException(f"Invalid second: {second}")

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
            second,
            tzinfo=timezone(timedelta(hours=tz_offset)),
        )
        return int(dt.timestamp())
    except (ValueError, OSError, OverflowError) as e:
        raise InvalidDateException(str(e)) from e


def unix_to_ethiopian(timestamp, tz_offset: float = 0) -> tuple:
    """Convert Unix timestamp to Ethiopian date/time.

    Args:
        timestamp: Unix timestamp (seconds since the Unix epoch).
        tz_offset: Timezone offset in hours, may be fractional.
            Defaults to 0 (UTC).

    Returns:
        Tuple (year, month, day, eth_hour, minute, second, is_pm) with
        eth_hour in 12-hour format (1-12).

    Raises:
        InvalidDateException: If the timestamp is not representable
            as a datetime on this platform.
    """
    try:
        dt = datetime.fromtimestamp(timestamp, tz=timezone(timedelta(hours=tz_offset)))
    except (ValueError, OSError, OverflowError) as e:
        raise InvalidDateException(f"Invalid timestamp: {timestamp}") from e

    # Convert to Ethiopian date
    e_year, e_month, e_day = convert_gregorian_to_ethiopian(dt.year, dt.month, dt.day)

    # Convert 24-hour time to Ethiopian 12-hour time
    eth_hour, is_pm = h24_to_eth(dt.hour)

    return e_year, e_month, e_day, eth_hour, dt.minute, dt.second, is_pm
