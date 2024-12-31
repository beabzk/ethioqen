import pytest
from ethioqen.time_conversion import convert_to_ethiopian_time, convert_from_ethiopian_time
from ethioqen.exceptions import InvalidTimeException

def test_standard_to_ethiopian():
    """Test key Ethiopian time conversions."""
    # Morning/Day hours
    assert convert_to_ethiopian_time(6, 0) == (12, 0, True)   # 6:00 AM -> 12:00 AM ET
    assert convert_to_ethiopian_time(7, 0) == (1, 0, True)    # 7:00 AM -> 1:00 AM ET
    assert convert_to_ethiopian_time(12, 0) == (6, 0, True)   # 12:00 PM -> 6:00 AM ET
    
    # Evening/Night hours
    assert convert_to_ethiopian_time(18, 0) == (12, 0, False) # 6:00 PM -> 12:00 PM ET
    assert convert_to_ethiopian_time(19, 0) == (1, 0, False)  # 7:00 PM -> 1:00 PM ET
    assert convert_to_ethiopian_time(0, 0) == (6, 0, False)   # 12:00 AM -> 6:00 PM ET
    assert convert_to_ethiopian_time(3, 0) == (9, 0, False)   # 3:00 AM -> 9:00 PM ET

def test_ethiopian_to_standard():
    """Test key standard time conversions."""
    # Morning/Day hours (is_am=True)
    assert convert_from_ethiopian_time(12, 0, True) == (6, 0)  # 12:00 AM ET -> 6:00 AM
    assert convert_from_ethiopian_time(1, 0, True) == (7, 0)   # 1:00 AM ET -> 7:00 AM
    assert convert_from_ethiopian_time(6, 0, True) == (12, 0)  # 6:00 AM ET -> 12:00 PM
    
    # Evening/Night hours (is_am=False)
    assert convert_from_ethiopian_time(12, 0, False) == (18, 0) # 12:00 PM ET -> 6:00 PM
    assert convert_from_ethiopian_time(1, 0, False) == (19, 0)  # 1:00 PM ET -> 7:00 PM
    assert convert_from_ethiopian_time(6, 0, False) == (0, 0)   # 6:00 PM ET -> 12:00 AM
    assert convert_from_ethiopian_time(9, 0, False) == (3, 0)   # 9:00 PM ET -> 3:00 AM

def test_12hour_format_conversion():
    """Test conversion using 12-hour format with AM/PM."""
    assert convert_to_ethiopian_time(7, 0, "AM") == (1, 0, True)    # 7:00 AM -> 1:00 AM ET
    assert convert_to_ethiopian_time(12, 0, "PM") == (6, 0, True)   # 12:00 PM -> 6:00 AM ET
    assert convert_to_ethiopian_time(7, 0, "PM") == (1, 0, False)   # 7:00 PM -> 1:00 PM ET
    assert convert_to_ethiopian_time(12, 0, "AM") == (6, 0, False)  # 12:00 AM -> 6:00 PM ET

def test_minutes_preserved():
    """Test that minutes are preserved in conversion."""
    assert convert_to_ethiopian_time(6, 30) == (12, 30, True)
    assert convert_to_ethiopian_time(18, 45) == (12, 45, False)
    assert convert_from_ethiopian_time(12, 30, True) == (6, 30)
    assert convert_from_ethiopian_time(12, 45, False) == (18, 45)

def test_invalid_standard_time():
    """Test error handling for invalid standard times."""
    with pytest.raises(InvalidTimeException):
        convert_to_ethiopian_time(24, 0)
    with pytest.raises(InvalidTimeException):
        convert_to_ethiopian_time(-1, 0)
    with pytest.raises(InvalidTimeException):
        convert_to_ethiopian_time(12, 60)
    with pytest.raises(InvalidTimeException):
        convert_to_ethiopian_time(12, -1)
    with pytest.raises(InvalidTimeException):
        convert_to_ethiopian_time(7, 0, "invalid")

def test_invalid_ethiopian_time():
    """Test error handling for invalid Ethiopian times."""
    with pytest.raises(InvalidTimeException):
        convert_from_ethiopian_time(13, 0, True)
    with pytest.raises(InvalidTimeException):
        convert_from_ethiopian_time(0, 0, True)
    with pytest.raises(InvalidTimeException):
        convert_from_ethiopian_time(6, 60, True)
    with pytest.raises(InvalidTimeException):
        convert_from_ethiopian_time(6, -1, False)

def test_round_trip_conversion():
    """Test converting times back and forth."""
    test_cases = [
        (6, 0),   # 6:00 AM / 12:00 AM ET
        (7, 0),   # 7:00 AM / 1:00 AM ET
        (12, 0),  # 12:00 PM / 6:00 AM ET
        (18, 0),  # 6:00 PM / 12:00 PM ET
        (0, 0),   # 12:00 AM / 6:00 PM ET
        (3, 0),   # 3:00 AM / 9:00 PM ET
    ]
    
    for hour, minute in test_cases:
        eth_hour, eth_minute, is_am = convert_to_ethiopian_time(hour, minute)
        std_hour, std_minute = convert_from_ethiopian_time(eth_hour, eth_minute, is_am)
        assert (hour, minute) == (std_hour, std_minute)