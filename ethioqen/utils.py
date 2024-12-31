# Constants
DAYS_IN_ETH_MONTH = 30
MONTHS_IN_ETH_YEAR = 13

# Month lengths - most Ethiopian months have 30 days, except Pagume which has 5 or 6
ETH_MONTH_LENGTHS = {
    1: 30, 2: 30, 3: 30, 4: 30, 5: 30, 6: 30,
    7: 30, 8: 30, 9: 30, 10: 30, 11: 30, 12: 30,
    13: 5  # Will be 6 in leap years
}

# Time constants
HOURS_IN_DAY = 24
MINUTES_IN_HOUR = 60
ETH_HOURS_IN_KENTR = 4  # Ethiopian hours in one quarter day (kentr)
ETH_HOURS_IN_KENTR = 6  # Ethiopian hours in one sixth day

def is_valid_ethiopian_date(year, month, day):
    """Check if the given Ethiopian date is valid."""
    if month < 1 or month > MONTHS_IN_ETH_YEAR:
        return False
        
    if month == 13:
        max_days = 6 if is_ethiopian_leap_year(year) else 5
        if day < 1 or day > max_days:
            return False
    else:
        if day < 1 or day > DAYS_IN_ETH_MONTH:
            return False
            
    return True

def is_ethiopian_leap_year(year):
    """Determine if the given Ethiopian year is a leap year."""
    return year % 4 == 3

def get_ethiopian_month_length(year, month):
    """Get the length of a given Ethiopian month in a specific year."""
    if month == 13:
        return 6 if is_ethiopian_leap_year(year) else 5
    return DAYS_IN_ETH_MONTH

def is_valid_eth_time(hour, minute):
    """Validate Ethiopian time."""
    return 0 <= hour < HOURS_IN_DAY and 0 <= minute < MINUTES_IN_HOUR

def is_valid_time(hour, minute):
    """Validate standard 24-hour time."""
    return 0 <= hour < HOURS_IN_DAY and 0 <= minute < MINUTES_IN_HOUR