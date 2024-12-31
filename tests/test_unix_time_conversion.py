import pytest
from datetime import datetime, timezone, timedelta
from ethioqen.unix_time_conversion import ethiopian_to_unix, unix_to_ethiopian
from ethioqen.exceptions import InvalidDateException

def test_ethiopian_to_unix_basic():
    """Test basic Ethiopian to Unix timestamp conversion."""
    # Ethiopian date: 2015-01-01 00:00 (2022-09-11 Gregorian)
    eth_timestamp = ethiopian_to_unix(2015, 1, 1)
    greg_dt = datetime(2022, 9, 11, tzinfo=timezone.utc)
    assert eth_timestamp == int(greg_dt.timestamp())

def test_ethiopian_to_unix_with_time():
    """Test conversion with specific times."""
    # Ethiopian date: 2015-01-01 15:30 (2022-09-11 Gregorian)
    eth_timestamp = ethiopian_to_unix(2015, 1, 1, 15, 30)
    greg_dt = datetime(2022, 9, 11, 15, 30, tzinfo=timezone.utc)
    assert eth_timestamp == int(greg_dt.timestamp())

def test_ethiopian_to_unix_with_timezone():
    """Test conversion with timezone offsets."""
    # Ethiopian date with +3:00 timezone (Addis Ababa)
    eth_timestamp = ethiopian_to_unix(2015, 1, 1, 12, 0, 3)
    greg_dt = datetime(2022, 9, 11, 12, 0, 
                      tzinfo=timezone(timedelta(hours=3)))
    assert eth_timestamp == int(greg_dt.timestamp())

def test_unix_to_ethiopian_basic():
    """Test basic Unix timestamp to Ethiopian conversion."""
    # 2022-09-11 00:00:00 UTC (Ethiopian 2015-01-01)
    greg_dt = datetime(2022, 9, 11, tzinfo=timezone.utc)
    eth_date = unix_to_ethiopian(int(greg_dt.timestamp()))
    assert eth_date == (2015, 1, 1, 0, 0)

def test_unix_to_ethiopian_with_time():
    """Test conversion of timestamp with specific time."""
    # 2022-09-11 15:30:00 UTC
    greg_dt = datetime(2022, 9, 11, 15, 30, tzinfo=timezone.utc)
    eth_date = unix_to_ethiopian(int(greg_dt.timestamp()))
    assert eth_date == (2015, 1, 1, 15, 30)

def test_unix_to_ethiopian_with_timezone():
    """Test conversion with timezone offset."""
    # 2022-09-11 12:00:00 +03:00
    greg_dt = datetime(2022, 9, 11, 12, 0, 
                      tzinfo=timezone(timedelta(hours=3)))
    eth_date = unix_to_ethiopian(int(greg_dt.timestamp()), 3)
    assert eth_date == (2015, 1, 1, 12, 0)

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
    with pytest.raises(InvalidDateException):
        ethiopian_to_unix(2015, 1, 1, 24, 0)  # Invalid hour
    with pytest.raises(InvalidDateException):
        ethiopian_to_unix(2015, 1, 1, 0, 60)  # Invalid minute

def test_invalid_timestamps():
    """Test error handling for invalid Unix timestamps."""
    with pytest.raises(InvalidDateException):
        unix_to_ethiopian(-62167219200)  # Too early
    with pytest.raises(InvalidDateException):
        unix_to_ethiopian(253402300800)  # Too late

def test_round_trip_conversion():
    """Test converting dates back and forth."""
    original_date = (2015, 1, 1, 12, 30)  # Ethiopian date/time
    # Convert to Unix timestamp
    unix_ts = ethiopian_to_unix(*original_date[:3], original_date[3], original_date[4])
    # Convert back to Ethiopian
    result_date = unix_to_ethiopian(unix_ts)
    assert original_date == result_date