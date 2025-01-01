import pytest
from datetime import datetime, timezone, timedelta
from ethioqen.unix_time_conversion import (
    ethiopian_to_unix, 
    unix_to_ethiopian,
    _convert_ethiopian_to_24h,
    _convert_24h_to_ethiopian
)
from ethioqen.exceptions import InvalidDateException

def test_ethiopian_12h_to_24h_conversion():
    """Test Ethiopian 12-hour to 24-hour conversion."""
    # Morning times
    assert _convert_ethiopian_to_24h(12, False) == 6  # 12 AM = 6:00
    assert _convert_ethiopian_to_24h(1, False) == 7   # 1 AM = 7:00
    assert _convert_ethiopian_to_24h(6, False) == 12  # 6 AM = 12:00
    
    # Afternoon/evening times
    assert _convert_ethiopian_to_24h(12, True) == 18  # 12 PM = 18:00
    assert _convert_ethiopian_to_24h(1, True) == 19   # 1 PM = 19:00
    assert _convert_ethiopian_to_24h(6, True) == 0    # 6 PM = 00:00

def test_24h_to_ethiopian_12h_conversion():
    """Test 24-hour to Ethiopian 12-hour conversion."""
    # Morning times
    assert _convert_24h_to_ethiopian(6) == (12, False)   # 6:00 = 12 AM
    assert _convert_24h_to_ethiopian(7) == (1, False)    # 7:00 = 1 AM
    assert _convert_24h_to_ethiopian(12) == (6, False)   # 12:00 = 6 AM
    
    # Afternoon/evening times
    assert _convert_24h_to_ethiopian(18) == (12, True)   # 18:00 = 12 PM
    assert _convert_24h_to_ethiopian(19) == (1, True)    # 19:00 = 1 PM
    assert _convert_24h_to_ethiopian(0) == (6, True)     # 00:00 = 6 PM

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
    assert eth_date == (2015, 1, 1, 12, 0, False)
    
    # 2022-09-11 19:00:00 UTC (Ethiopian 1:00 PM)
    greg_dt = datetime(2022, 9, 11, 19, 0, tzinfo=timezone.utc)
    eth_date = unix_to_ethiopian(int(greg_dt.timestamp()))
    assert eth_date == (2015, 1, 1, 1, 0, True)

def test_ethiopian_to_unix_basic():
    """Test basic Ethiopian to Unix timestamp conversion."""
    eth_timestamp = ethiopian_to_unix(2015, 1, 1)
    greg_dt = datetime(2022, 9, 11, 6, 0, tzinfo=timezone.utc)  # Default 12 AM = 6:00
    assert eth_timestamp == int(greg_dt.timestamp())

def test_ethiopian_to_unix_with_timezone():
    """Test conversion with timezone offsets."""
    # Ethiopian date with +3:00 timezone (Addis Ababa)
    eth_timestamp = ethiopian_to_unix(2015, 1, 1, 12, 0, False, 3)
    greg_dt = datetime(2022, 9, 11, 6, 0, 
                      tzinfo=timezone(timedelta(hours=3)))
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
    with pytest.raises(InvalidDateException):
        ethiopian_to_unix(2015, 1, 1, 13, 0)  # Invalid hour (>12)
    with pytest.raises(InvalidDateException):
        ethiopian_to_unix(2015, 1, 1, 0, 0)   # Invalid hour (<1)
    with pytest.raises(InvalidDateException):
        ethiopian_to_unix(2015, 1, 1, 12, 60) # Invalid minute

def test_invalid_timestamps():
    """Test error handling for invalid Unix timestamps."""
    with pytest.raises(InvalidDateException):
        unix_to_ethiopian(-62167219200)  # Too early
    with pytest.raises(InvalidDateException):
        unix_to_ethiopian(253402300800)  # Too late

def test_round_trip_conversion():
    """Test converting dates back and forth."""
    original_date = (2015, 1, 1, 1, 30, True)  # Ethiopian date/time (1:30 PM)
    # Convert to Unix timestamp
    unix_ts = ethiopian_to_unix(
        original_date[0], original_date[1], original_date[2],
        original_date[3], original_date[4], original_date[5]
    )
    # Convert back to Ethiopian
    result_date = unix_to_ethiopian(unix_ts)
    assert original_date == result_date