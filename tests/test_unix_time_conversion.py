from datetime import datetime, timedelta, timezone

import pytest

from ethioqen.exceptions import InvalidDateException, InvalidTimeException
from ethioqen.unix_time_conversion import ethiopian_to_unix, unix_to_ethiopian


def test_ethiopian_to_unix_12h_format():
    """Test Ethiopian to Unix conversion with 12-hour format."""
    # Ethiopian date: 2015-01-01 12:00 AM (6:00 standard)
    eth_timestamp = ethiopian_to_unix(2015, 1, 1, 12, 0, False)
    greg_dt = datetime(2022, 9, 11, 6, 0, tzinfo=timezone.utc)
    assert eth_timestamp == int(greg_dt.timestamp())

    # Ethiopian date: 2015-01-01 1:00 PM (19:00 standard)
    eth_timestamp = ethiopian_to_unix(2015, 1, 1, 1, 0, True)
    greg_dt = datetime(2022, 9, 11, 19, 0, tzinfo=timezone.utc)
    assert eth_timestamp == int(greg_dt.timestamp())


def test_unix_to_ethiopian_12h_format():
    """Test Unix to Ethiopian conversion with 12-hour format."""
    # 2022-09-11 6:00:00 UTC (Ethiopian 12:00 AM)
    greg_dt = datetime(2022, 9, 11, 6, 0, tzinfo=timezone.utc)
    eth_date = unix_to_ethiopian(int(greg_dt.timestamp()))
    assert eth_date == (2015, 1, 1, 12, 0, 0, False)

    # 2022-09-11 19:00:00 UTC (Ethiopian 1:00 PM)
    greg_dt = datetime(2022, 9, 11, 19, 0, tzinfo=timezone.utc)
    eth_date = unix_to_ethiopian(int(greg_dt.timestamp()))
    assert eth_date == (2015, 1, 1, 1, 0, 0, True)


def test_ethiopian_to_unix_basic():
    """Test basic Ethiopian to Unix timestamp conversion."""
    eth_timestamp = ethiopian_to_unix(2015, 1, 1)
    greg_dt = datetime(2022, 9, 11, 6, 0, tzinfo=timezone.utc)  # Default 12 AM = 6:00
    assert eth_timestamp == int(greg_dt.timestamp())


def test_ethiopian_to_unix_with_timezone():
    """Test conversion with timezone offsets."""
    # Ethiopian date with +3:00 timezone (Addis Ababa)
    eth_timestamp = ethiopian_to_unix(2015, 1, 1, 12, 0, False, 3)
    greg_dt = datetime(2022, 9, 11, 6, 0, tzinfo=timezone(timedelta(hours=3)))
    assert eth_timestamp == int(greg_dt.timestamp())


def test_invalid_ethiopian_dates():
    """Test error handling for invalid Ethiopian dates."""
    with pytest.raises(InvalidDateException):
        ethiopian_to_unix(2015, 13, 7)  # Invalid Pagume day
    with pytest.raises(InvalidDateException):
        ethiopian_to_unix(2015, 14, 1)  # Invalid month
    with pytest.raises(InvalidDateException):
        ethiopian_to_unix(2015, 1, 31)  # Invalid day


def test_invalid_times():
    """Test error handling for invalid times."""
    with pytest.raises(InvalidTimeException):
        ethiopian_to_unix(2015, 1, 1, 13, 0)  # Invalid hour (>12)
    with pytest.raises(InvalidTimeException):
        ethiopian_to_unix(2015, 1, 1, 0, 0)  # Invalid hour (<1)
    with pytest.raises(InvalidTimeException):
        ethiopian_to_unix(2015, 1, 1, 12, 60)  # Invalid minute
    with pytest.raises(InvalidTimeException):
        ethiopian_to_unix(2015, 1, 1, 12, 0, second=60)  # Invalid second


def test_invalid_timestamps():
    """Test error handling for invalid Unix timestamps."""
    with pytest.raises(InvalidDateException):
        unix_to_ethiopian(-62167219200)  # Too early
    with pytest.raises(InvalidDateException):
        unix_to_ethiopian(253402300800)  # Too late


def test_round_trip_conversion():
    """Test converting dates back and forth."""
    # Ethiopian date/time (1:30:45 PM)
    unix_ts = ethiopian_to_unix(2015, 1, 1, 1, 30, True, second=45)
    assert unix_to_ethiopian(unix_ts) == (2015, 1, 1, 1, 30, 45, True)


def test_seconds_preserved():
    """Seconds survive Ethiopian -> Unix -> Ethiopian."""
    expected = datetime(2022, 9, 11, 19, 30, 45, tzinfo=timezone.utc)
    timestamp = ethiopian_to_unix(2015, 1, 1, 1, 30, True, second=45)
    assert timestamp == int(expected.timestamp())
    assert unix_to_ethiopian(timestamp) == (2015, 1, 1, 1, 30, 45, True)


def test_seconds_default_to_zero():
    """Omitting seconds behaves as :00 and round-trips losslessly."""
    timestamp = ethiopian_to_unix(2015, 1, 1, 1, 30, True)
    assert unix_to_ethiopian(timestamp) == (2015, 1, 1, 1, 30, 0, True)


def test_fractional_timezone_offset():
    """Half/three-quarter-hour offsets (e.g. +5:30, +5:45) convert exactly."""
    for tz_offset in (0, 3, 5.5, 5.75, -5):
        greg_dt = datetime(
            2022, 9, 11, 19, 30, 45, tzinfo=timezone(timedelta(hours=tz_offset))
        )
        timestamp = ethiopian_to_unix(
            2015, 1, 1, 1, 30, True, second=45, tz_offset=tz_offset
        )
        assert timestamp == int(greg_dt.timestamp())
        back = unix_to_ethiopian(timestamp, tz_offset=tz_offset)
        assert back == (2015, 1, 1, 1, 30, 45, True)


def test_out_of_range_timestamps():
    """Absurd timestamps raise on every platform, not just some."""
    with pytest.raises(InvalidDateException):
        unix_to_ethiopian(2**63 - 1)
    with pytest.raises(InvalidDateException):
        unix_to_ethiopian(-(2**63))
    with pytest.raises(InvalidDateException):
        unix_to_ethiopian(float("inf"))
