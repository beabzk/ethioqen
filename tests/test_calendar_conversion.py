import pytest
from ethioqen.calendar_conversion import (
    convert_ethiopian_to_gregorian,
    convert_gregorian_to_ethiopian,
    is_ethiopian_leap_year,
    is_gregorian_leap_year
)
from ethioqen.exceptions import InvalidDateException

def test_ethiopian_leap_year():
    """Test Ethiopian leap year calculation."""
    assert is_ethiopian_leap_year(2015) == True   # 2015 E.C. is a leap year
    assert is_ethiopian_leap_year(2016) == False  # 2016 E.C. is not a leap year
    assert is_ethiopian_leap_year(2019) == True   # 2019 E.C. is a leap year

def test_gregorian_leap_year():
    """Test Gregorian leap year calculation."""
    assert is_gregorian_leap_year(2020) == True   # 2020-01-01 is start of a leap year
    assert is_gregorian_leap_year(2021) == False  # 2021-01-01 is not a leap year
    assert is_gregorian_leap_year(2000) == True   # 2000-01-01 is a leap year (divisible by 400)
    assert is_gregorian_leap_year(1900) == False  # 1900-01-01 is not a leap year (divisible by 100 but not 400)

def test_ethiopian_to_gregorian():
    """Test conversion from Ethiopian to Gregorian calendar."""
    # Test some known dates
    assert convert_ethiopian_to_gregorian(2015, 1, 1) == (2022, 9, 11)  # Ethiopian New Year
    assert convert_ethiopian_to_gregorian(2015, 13, 6) == (2023, 9, 11)  # Last day of 2015 (leap year)
    assert convert_ethiopian_to_gregorian(2015, 5, 1) == (2023, 1, 9)    # Regular date

def test_ethiopian_to_gregorian_year_boundaries():
    """Test Ethiopian to Gregorian conversion around year boundaries."""
    # Year end tests (Pagume)
    assert convert_ethiopian_to_gregorian(2015, 13, 1) == (2023, 9, 6)    # Start of Pagume 2015
    assert convert_ethiopian_to_gregorian(2015, 13, 2) == (2023, 9, 7)    # Pagume 2
    assert convert_ethiopian_to_gregorian(2015, 13, 3) == (2023, 9, 8)    # Pagume 3
    assert convert_ethiopian_to_gregorian(2015, 13, 4) == (2023, 9, 9)    # Pagume 4
    assert convert_ethiopian_to_gregorian(2015, 13, 5) == (2023, 9, 10)   # Pagume 5
    assert convert_ethiopian_to_gregorian(2015, 13, 6) == (2023, 9, 11)   # Last day of 2015 (leap)
    
    # Year start tests (Meskerem)
    assert convert_ethiopian_to_gregorian(2016, 1, 1) == (2023, 9, 12)    # New Year 2016
    assert convert_ethiopian_to_gregorian(2016, 1, 2) == (2023, 9, 13)    # Meskerem 2
    assert convert_ethiopian_to_gregorian(2016, 1, 3) == (2023, 9, 14)    # Meskerem 3
    assert convert_ethiopian_to_gregorian(2016, 1, 4) == (2023, 9, 15)    # Meskerem 4
    assert convert_ethiopian_to_gregorian(2016, 1, 5) == (2023, 9, 16)    # Meskerem 5

    # Previous year tests
    assert convert_ethiopian_to_gregorian(2014, 13, 1) == (2022, 9, 6)    # Start of Pagume 2014
    assert convert_ethiopian_to_gregorian(2014, 13, 5) == (2022, 9, 10)   # Last day of 2014 (non-leap)
    assert convert_ethiopian_to_gregorian(2015, 1, 1) == (2022, 9, 11)    # New Year 2015

def test_gregorian_to_ethiopian():
    """Test conversion from Gregorian to Ethiopian calendar."""
    # Year end tests (different from eth_to_greg tests)
    assert convert_gregorian_to_ethiopian(2023, 9, 6) == (2015, 13, 1)    # Start of Pagume
    assert convert_gregorian_to_ethiopian(2023, 9, 7) == (2015, 13, 2)    # Pagume 2
    assert convert_gregorian_to_ethiopian(2023, 9, 8) == (2015, 13, 3)    # Pagume 3
    assert convert_gregorian_to_ethiopian(2023, 9, 9) == (2015, 13, 4)    # Pagume 4
    assert convert_gregorian_to_ethiopian(2023, 9, 10) == (2015, 13, 5)   # Pagume 5
    assert convert_gregorian_to_ethiopian(2023, 9, 11) == (2015, 13, 6)   # Last day of 2015

    # Year start tests
    assert convert_gregorian_to_ethiopian(2023, 9, 12) == (2016, 1, 1)    # Ethiopian New Year
    assert convert_gregorian_to_ethiopian(2023, 9, 13) == (2016, 1, 2)    # Meskerem 2
    assert convert_gregorian_to_ethiopian(2023, 9, 14) == (2016, 1, 3)    # Meskerem 3
    assert convert_gregorian_to_ethiopian(2023, 9, 15) == (2016, 1, 4)    # Meskerem 4
    assert convert_gregorian_to_ethiopian(2023, 9, 16) == (2016, 1, 5)    # Meskerem 5

    # Previous year boundary
    assert convert_gregorian_to_ethiopian(2022, 9, 6) == (2014, 13, 1)    # Start of Pagume 2014
    assert convert_gregorian_to_ethiopian(2022, 9, 10) == (2014, 13, 5)   # Last day of 2014
    assert convert_gregorian_to_ethiopian(2022, 9, 11) == (2015, 1, 1)    # Start of 2015

def test_invalid_dates():
    """Test handling of invalid dates."""
    # Test invalid Ethiopian month
    with pytest.raises(InvalidDateException):
        convert_ethiopian_to_gregorian(2015, 14, 1)
    
    # Test invalid Ethiopian day
    with pytest.raises(InvalidDateException):
        convert_ethiopian_to_gregorian(2015, 1, 31)
    
    # Test invalid Pagume day in non-leap year
    with pytest.raises(InvalidDateException):
        convert_ethiopian_to_gregorian(2016, 13, 6)  # 2016 E.C. is not a leap year

def test_round_trip_conversion():
    """Test converting dates back and forth."""
    # Test several dates to ensure they convert back correctly
    test_dates = [
        (2015, 1, 1),    # Ethiopian New Year
        (2015, 7, 15),   # Middle of the year
        (2015, 13, 5),   # Pagume 5
        (2015, 13, 6),   # Pagume 6 (leap year)
        (2016, 1, 1),    # New Year after leap year
    ]
    
    for eth_year, eth_month, eth_day in test_dates:
        # Convert to Gregorian
        greg_year, greg_month, greg_day = convert_ethiopian_to_gregorian(eth_year, eth_month, eth_day)
        # Convert back to Ethiopian
        eth_year2, eth_month2, eth_day2 = convert_gregorian_to_ethiopian(greg_year, greg_month, greg_day)
        # Should get the original date back
        assert (eth_year, eth_month, eth_day) == (eth_year2, eth_month2, eth_day2)