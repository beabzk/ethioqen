from .exceptions import InvalidDateException
from .utils import (
    is_ethiopian_leap_year,
    is_valid_ethiopian_date,
    is_valid_gregorian_date,
)

__all__ = [
    "is_ethiopian_leap_year",
    "is_gregorian_leap_year",
    "convert_ethiopian_to_gregorian",
    "convert_gregorian_to_ethiopian",
]

# JDN of the day before Meskerem 1, year 1 (29 Aug AD 8 Julian).
# Verified against Unix-epoch, millennium, and Enkutatash anchors
# in tests/test_calendar_conversion.py; do not change without re-verifying.
ETHIOPIAN_EPOCH = 1723856


def is_gregorian_leap_year(year: int) -> bool:
    """Determine if the given Gregorian year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _ethiopian_to_jdn(year: int, month: int, day: int) -> int:
    """Convert Ethiopian date to Julian Day Number."""
    if not is_valid_ethiopian_date(year, month, day):
        raise InvalidDateException(f"Invalid Ethiopian date: {year}-{month}-{day}")

    year_days = (year * 365) + (year // 4)
    month_days = (month - 1) * 30

    return ETHIOPIAN_EPOCH + year_days + month_days + day - 1


def _year_start_days(year: int) -> int:
    """Days from the epoch to Meskerem 1 of the given Ethiopian year."""
    return year * 365 + year // 4


def _jdn_to_ethiopian(jdn: int) -> tuple[int, int, int]:
    """Convert Julian Day Number to Ethiopian date (integer math only).

    Inverts _ethiopian_to_jdn exactly: finds the year whose
    [start, next start) interval contains the day, then splits the
    remainder into uniform 30-day months. Pagume needs no special
    casing: the remainder is always < 366, so month 13 holds at most
    6 days (leap years) or 5 (common years) by construction.
    """
    days_since_epoch = jdn - ETHIOPIAN_EPOCH

    # Estimate from the mean year length, then correct by at most one step.
    year = (4 * days_since_epoch) // 1461
    while _year_start_days(year + 1) <= days_since_epoch:
        year += 1
    while _year_start_days(year) > days_since_epoch:
        year -= 1

    remaining_days = days_since_epoch - _year_start_days(year)
    month = remaining_days // 30 + 1
    day = remaining_days % 30 + 1

    return year, month, day


def _gregorian_to_jdn(year: int, month: int, day: int) -> int:
    """Convert Gregorian date to Julian Day Number."""
    if month <= 2:
        year -= 1
        month += 12

    a = year // 100
    b = 2 - a + (a // 4)

    jdn = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524
    return jdn


def _jdn_to_gregorian(jdn: int) -> tuple[int, int, int]:
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


def convert_ethiopian_to_gregorian(
    eth_year: int, eth_month: int, eth_day: int
) -> tuple[int, int, int]:
    """Convert an Ethiopian date to Gregorian.

    Args:
        eth_year: Ethiopian year (>= 1).
        eth_month: Ethiopian month (1-13).
        eth_day: Ethiopian day (1-30; 1-5/6 for Pagume).

    Returns:
        Tuple (year, month, day) of the equivalent Gregorian date.

    Raises:
        InvalidDateException: If the Ethiopian date is invalid.

    Example:
        >>> convert_ethiopian_to_gregorian(2016, 1, 1)
        (2023, 9, 12)
    """
    if not is_valid_ethiopian_date(eth_year, eth_month, eth_day):
        raise InvalidDateException(
            f"Invalid Ethiopian date: {eth_year}-{eth_month}-{eth_day}"
        )

    jdn = _ethiopian_to_jdn(eth_year, eth_month, eth_day)
    return _jdn_to_gregorian(jdn)


def convert_gregorian_to_ethiopian(
    greg_year: int, greg_month: int, greg_day: int
) -> tuple[int, int, int]:
    """Convert a Gregorian date to Ethiopian.

    Args:
        greg_year: Gregorian year (>= 1).
        greg_month: Gregorian month (1-12).
        greg_day: Gregorian day (1-28/29/30/31 depending on month).

    Returns:
        Tuple (year, month, day) of the equivalent Ethiopian date.

    Raises:
        InvalidDateException: If the Gregorian date is invalid
            (e.g. 2023-02-29 or 2023-04-31).

    Example:
        >>> convert_gregorian_to_ethiopian(2023, 9, 12)
        (2016, 1, 1)
    """
    if not is_valid_gregorian_date(greg_year, greg_month, greg_day):
        raise InvalidDateException(
            f"Invalid Gregorian date: {greg_year}-{greg_month}-{greg_day}"
        )

    jdn = _gregorian_to_jdn(greg_year, greg_month, greg_day)
    return _jdn_to_ethiopian(jdn)
