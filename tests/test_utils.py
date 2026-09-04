"""Tests for ethioqen.utils validators and helpers."""

from ethioqen.utils import (
    get_ethiopian_month_length,
    is_ethiopian_leap_year,
    is_valid_ethiopian_date,
    is_valid_ethiopian_hour,
    is_valid_gregorian_date,
    is_valid_standard_time,
)


def test_ethiopian_leap_year_table():
    assert is_ethiopian_leap_year(2015) is True
    assert is_ethiopian_leap_year(2016) is False
    assert is_ethiopian_leap_year(2019) is True


def test_ethiopian_month_length():
    assert get_ethiopian_month_length(2016, 1) == 30
    assert get_ethiopian_month_length(2016, 12) == 30
    assert get_ethiopian_month_length(2015, 13) == 6  # leap year Pagume
    assert get_ethiopian_month_length(2016, 13) == 5  # common year Pagume


def test_valid_ethiopian_dates():
    assert is_valid_ethiopian_date(2015, 1, 1) is True
    assert is_valid_ethiopian_date(2015, 13, 6) is True  # leap Pagume 6
    assert is_valid_ethiopian_date(2016, 13, 5) is True  # common Pagume 5


def test_invalid_ethiopian_dates():
    assert is_valid_ethiopian_date(2015, 0, 1) is False
    assert is_valid_ethiopian_date(2015, 14, 1) is False
    assert is_valid_ethiopian_date(2015, 1, 0) is False
    assert is_valid_ethiopian_date(2015, 1, 31) is False
    assert is_valid_ethiopian_date(2016, 13, 6) is False  # Pagume 6, non-leap


def test_ethiopian_date_rejects_bad_years():
    """Year 0 / negative years are not valid Ethiopian dates."""
    assert is_valid_ethiopian_date(0, 1, 1) is False
    assert is_valid_ethiopian_date(-1, 1, 1) is False


def test_ethiopian_date_rejects_non_ints():
    """Non-integer components are invalid, not TypeErrors."""
    assert is_valid_ethiopian_date("2015", 1, 1) is False
    assert is_valid_ethiopian_date(2015, "1", 1) is False
    assert is_valid_ethiopian_date(2015, 1, "1") is False
    assert is_valid_ethiopian_date(2015.5, 1, 1) is False


def test_valid_gregorian_dates():
    assert is_valid_gregorian_date(2024, 2, 29) is True  # leap day
    assert is_valid_gregorian_date(2023, 9, 11) is True
    assert is_valid_gregorian_date(2000, 2, 29) is True  # div-400 leap
    assert is_valid_gregorian_date(2022, 12, 31) is True


def test_invalid_gregorian_dates():
    assert is_valid_gregorian_date(2023, 2, 29) is False  # non-leap Feb 29
    assert is_valid_gregorian_date(1900, 2, 29) is False  # div-100 non-leap
    assert is_valid_gregorian_date(2023, 4, 31) is False  # April has 30 days
    assert is_valid_gregorian_date(2023, 0, 10) is False
    assert is_valid_gregorian_date(2023, 13, 10) is False
    assert is_valid_gregorian_date(2023, 1, 0) is False
    assert is_valid_gregorian_date(2023, 1, 32) is False
    assert is_valid_gregorian_date(0, 1, 1) is False
    assert is_valid_gregorian_date("2023", 1, 1) is False
    assert is_valid_gregorian_date(2023, 1, None) is False


def test_ethiopian_hour_validation():
    assert is_valid_ethiopian_hour(1, 0) is True
    assert is_valid_ethiopian_hour(12, 59) is True
    assert is_valid_ethiopian_hour(0, 0) is False  # 0 is not an Eth hour
    assert is_valid_ethiopian_hour(13, 0) is False
    assert is_valid_ethiopian_hour(6, 60) is False
    assert is_valid_ethiopian_hour(6, -1) is False


def test_standard_time_validation():
    assert is_valid_standard_time(0, 0) is True
    assert is_valid_standard_time(23, 59) is True
    assert is_valid_standard_time(24, 0) is False
    assert is_valid_standard_time(-1, 0) is False
    assert is_valid_standard_time(12, 60) is False
