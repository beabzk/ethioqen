from .exceptions import InvalidTimeException
from .utils import is_valid_ethiopian_hour, is_valid_standard_time

__all__ = [
    "eth_to_24h",
    "h24_to_eth",
    "convert_to_ethiopian_time",
    "convert_from_ethiopian_time",
]


def eth_to_24h(eth_hour: int, is_pm: bool) -> int:
    """Convert Ethiopian 12-hour time to 24-hour standard time.

    The Ethiopian clock runs 6 hours behind the standard clock:
    12:00 AM Ethiopian is 6:00 standard, 12:00 PM Ethiopian is 18:00.

    Args:
        eth_hour: Ethiopian hour (1-12).
        is_pm: Whether the time is PM (night) as opposed to AM (day).

    Returns:
        Hour in 24-hour format (0-23).

    Raises:
        InvalidTimeException: If eth_hour is outside 1-12.
    """
    if not is_valid_ethiopian_hour(eth_hour, 0):
        raise InvalidTimeException(f"Invalid Ethiopian hour: {eth_hour}")

    hour_24 = eth_hour % 12  # 12 -> 0
    if is_pm:
        hour_24 += 12
    return (hour_24 + 6) % 24


def h24_to_eth(hour_24: int) -> tuple[int, bool]:
    """Convert 24-hour standard time to Ethiopian 12-hour time.

    Args:
        hour_24: Standard hour (0-23).

    Returns:
        Tuple (eth_hour in 1-12, is_pm boolean).

    Raises:
        InvalidTimeException: If hour_24 is outside 0-23.
    """
    if not is_valid_standard_time(hour_24, 0):
        raise InvalidTimeException(f"Invalid standard hour: {hour_24}")

    eth_hour = (hour_24 - 6) % 24
    is_pm = eth_hour >= 12
    if is_pm:
        eth_hour -= 12
    if eth_hour == 0:
        eth_hour = 12
    return eth_hour, is_pm


def convert_to_ethiopian_time(
    hour: int, minute: int, period: str | None = None
) -> tuple[int, int, bool]:
    """Convert standard time to Ethiopian time.

    Args:
        hour: Standard hour. 0-23, or 1-12 when period is given.
        minute: Minutes (0-59).
        period: Optional "AM"/"PM" qualifying a 12-hour input hour.

    Returns:
        Tuple (eth_hour in 1-12, minute, is_pm boolean). 06:00-17:59
        standard is day (is_pm False), otherwise night (is_pm True).

    Raises:
        InvalidTimeException: On invalid time, bad period, or a 12-hour
            period combined with an hour outside 1-12.

    Example:
        >>> convert_to_ethiopian_time(14, 30)
        (8, 30, False)
    """
    if period is not None:
        if not isinstance(period, str) or period.upper() not in ("AM", "PM"):
            raise InvalidTimeException("Period must be 'AM' or 'PM'")
        if not is_valid_ethiopian_hour(hour, minute):
            raise InvalidTimeException(
                f"Hour must be 1-12 with a period: {hour}:{minute}"
            )
        if period.upper() == "PM" and hour != 12:
            hour += 12
        elif period.upper() == "AM" and hour == 12:
            hour = 0
    elif not is_valid_standard_time(hour, minute):
        raise InvalidTimeException(f"Invalid time: {hour}:{minute}")

    eth_hour = (hour - 6) % 12
    if eth_hour == 0:
        eth_hour = 12
    return eth_hour, minute, not 6 <= hour < 18


def convert_from_ethiopian_time(
    eth_hour: int, minute: int, is_pm: bool = False
) -> tuple[int, int]:
    """Convert Ethiopian time to 24-hour standard time.

    Args:
        eth_hour: Ethiopian hour (1-12).
        minute: Minutes (0-59).
        is_pm: Whether the time is PM (night). Defaults to False (day).

    Returns:
        Tuple (hour in 0-23, minute).

    Raises:
        InvalidTimeException: If the Ethiopian time is invalid.

    Example:
        >>> convert_from_ethiopian_time(8, 30, is_pm=False)
        (14, 30)
    """
    if not is_valid_ethiopian_hour(eth_hour, minute):
        raise InvalidTimeException(f"Invalid Ethiopian time: {eth_hour}:{minute}")
    return eth_to_24h(eth_hour, is_pm), minute
