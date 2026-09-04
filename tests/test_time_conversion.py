import pytest

from ethioqen.exceptions import InvalidTimeException
from ethioqen.time_conversion import (
    convert_from_ethiopian_time,
    convert_to_ethiopian_time,
)


def test_12hour_format_conversion():
    """Test conversion using 12-hour format with AM/PM."""
    assert convert_to_ethiopian_time(7, 0, "AM") == (
        1,
        0,
        False,
    )  # 7:00 AM -> 1:00 AM ET
    assert convert_to_ethiopian_time(12, 0, "PM") == (
        6,
        0,
        False,
    )  # 12:00 PM -> 6:00 AM ET
    assert convert_to_ethiopian_time(7, 0, "PM") == (
        1,
        0,
        True,
    )  # 7:00 PM -> 1:00 PM ET
    assert convert_to_ethiopian_time(12, 0, "AM") == (
        6,
        0,
        True,
    )  # 12:00 AM -> 6:00 PM ET


def test_minutes_preserved():
    """Test that minutes are preserved in conversion."""
    assert convert_to_ethiopian_time(6, 30) == (12, 30, False)
    assert convert_to_ethiopian_time(18, 45) == (12, 45, True)
    assert convert_from_ethiopian_time(12, 30, is_pm=False) == (6, 30)
    assert convert_from_ethiopian_time(12, 45, is_pm=True) == (18, 45)


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
        convert_from_ethiopian_time(13, 0, is_pm=False)
    with pytest.raises(InvalidTimeException):
        convert_from_ethiopian_time(0, 0, is_pm=False)
    with pytest.raises(InvalidTimeException):
        convert_from_ethiopian_time(6, 60, is_pm=False)
    with pytest.raises(InvalidTimeException):
        convert_from_ethiopian_time(6, -1, is_pm=True)


def test_round_trip_conversion():
    """Test converting times back and forth."""
    test_cases = [
        (6, 0),  # 6:00 AM / 12:00 AM ET
        (7, 0),  # 7:00 AM / 1:00 AM ET
        (12, 0),  # 12:00 PM / 6:00 AM ET
        (18, 0),  # 6:00 PM / 12:00 PM ET
        (0, 0),  # 12:00 AM / 6:00 PM ET
        (3, 0),  # 3:00 AM / 9:00 PM ET
    ]

    for hour, minute in test_cases:
        eth_hour, eth_minute, is_pm = convert_to_ethiopian_time(hour, minute)
        std_hour, std_minute = convert_from_ethiopian_time(eth_hour, eth_minute, is_pm)
        assert (hour, minute) == (std_hour, std_minute)


def test_canonical_helpers():
    """Single shared 6-hour shift used by both time modules."""
    from ethioqen.time_conversion import eth_to_24h, h24_to_eth

    assert eth_to_24h(12, False) == 6
    assert eth_to_24h(1, False) == 7
    assert eth_to_24h(6, False) == 12
    assert eth_to_24h(12, True) == 18
    assert eth_to_24h(1, True) == 19
    assert eth_to_24h(6, True) == 0
    assert h24_to_eth(6) == (12, False)
    assert h24_to_eth(7) == (1, False)
    assert h24_to_eth(12) == (6, False)
    assert h24_to_eth(18) == (12, True)
    assert h24_to_eth(19) == (1, True)
    assert h24_to_eth(0) == (6, True)


def test_is_pm_convention():
    """Third return value / keyword is is_pm: day is False, night is True."""
    assert convert_to_ethiopian_time(6, 0) == (12, 0, False)
    assert convert_to_ethiopian_time(7, 0) == (1, 0, False)
    assert convert_to_ethiopian_time(12, 0) == (6, 0, False)
    assert convert_to_ethiopian_time(14, 30) == (8, 30, False)
    assert convert_to_ethiopian_time(18, 0) == (12, 0, True)
    assert convert_to_ethiopian_time(19, 0) == (1, 0, True)
    assert convert_to_ethiopian_time(0, 0) == (6, 0, True)
    assert convert_to_ethiopian_time(3, 0) == (9, 0, True)

    assert convert_from_ethiopian_time(12, 0, is_pm=False) == (6, 0)
    assert convert_from_ethiopian_time(1, 0, is_pm=False) == (7, 0)
    assert convert_from_ethiopian_time(6, 0, is_pm=False) == (12, 0)
    assert convert_from_ethiopian_time(12, 0, is_pm=True) == (18, 0)
    assert convert_from_ethiopian_time(1, 0, is_pm=True) == (19, 0)
    assert convert_from_ethiopian_time(6, 0, is_pm=True) == (0, 0)
    assert convert_from_ethiopian_time(9, 0, is_pm=True) == (3, 0)


def test_period_with_24h_hour_raises():
    """A period with an out-of-1-12 hour is misuse, not silent garbage."""
    with pytest.raises(InvalidTimeException):
        convert_to_ethiopian_time(14, 30, "PM")
    with pytest.raises(InvalidTimeException):
        convert_to_ethiopian_time(0, 30, "AM")
    with pytest.raises(InvalidTimeException):
        convert_to_ethiopian_time(13, 0, "PM")
    with pytest.raises(InvalidTimeException):
        convert_to_ethiopian_time(24, 0, "AM")


def test_24h_sweep_round_trip():
    """Every hour of the day survives standard -> Ethiopian -> standard."""
    for hour in range(24):
        eth_hour, minute, is_pm = convert_to_ethiopian_time(hour, 0)
        assert minute == 0
        assert convert_from_ethiopian_time(eth_hour, minute, is_pm) == (hour, 0)
