# Constants
import calendar

DAYS_IN_ETH_MONTH = 30
MONTHS_IN_ETH_YEAR = 13

# Month lengths - most Ethiopian months have 30 days, except Pagume which has 5 or 6
ETH_MONTH_LENGTHS = {
    1: 30,
    2: 30,
    3: 30,
    4: 30,
    5: 30,
    6: 30,
    7: 30,
    8: 30,
    9: 30,
    10: 30,
    11: 30,
    12: 30,
    13: 5,  # 6 in leap years; see get_ethiopian_month_length
}

# Time constants
HOURS_IN_DAY = 24
MINUTES_IN_HOUR = 60
ETH_HOURS_IN_DAY = 12  # Ethiopian clock face: hours 1-12, twice per day


def _is_int(value: object) -> bool:
    """Strict int check: bools are not valid date/time components."""
    return isinstance(value, int) and not isinstance(value, bool)


def is_ethiopian_leap_year(year: int) -> bool:
    """Determine if the given Ethiopian year is a leap year."""
    if not _is_int(year):
        return False
    return year % 4 == 3


def get_ethiopian_month_length(year: int, month: int) -> int:
    """Get the length of a given Ethiopian month in a specific year."""
    if month == 13:
        return 6 if is_ethiopian_leap_year(year) else 5
    return ETH_MONTH_LENGTHS[month]


def is_valid_ethiopian_date(year: int, month: int, day: int) -> bool:
    """Check if the given Ethiopian date is valid."""
    if not _is_int(year) or year < 1:
        return False
    if not _is_int(month) or month < 1 or month > MONTHS_IN_ETH_YEAR:
        return False
    if not _is_int(day):
        return False
    return 1 <= day <= get_ethiopian_month_length(year, month)


def is_valid_gregorian_date(year: int, month: int, day: int) -> bool:
    """Check if the given Gregorian (proleptic) date is valid."""
    if not _is_int(year) or year < 1:
        return False
    if not _is_int(month) or month < 1 or month > 12:
        return False
    if not _is_int(day):
        return False
    return 1 <= day <= calendar.monthrange(year, month)[1]


def is_valid_ethiopian_hour(hour: int, minute: int) -> bool:
    """Validate Ethiopian clock time (hour 1-12, minute 0-59)."""
    return (
        _is_int(hour)
        and 1 <= hour <= ETH_HOURS_IN_DAY
        and _is_int(minute)
        and 0 <= minute < MINUTES_IN_HOUR
    )


def is_valid_standard_time(hour: int, minute: int) -> bool:
    """Validate standard 24-hour time."""
    return (
        _is_int(hour)
        and 0 <= hour < HOURS_IN_DAY
        and _is_int(minute)
        and 0 <= minute < MINUTES_IN_HOUR
    )


def is_valid_time(hour: int, minute: int) -> bool:
    """Validate standard 24-hour time (alias of is_valid_standard_time)."""
    return is_valid_standard_time(hour, minute)
