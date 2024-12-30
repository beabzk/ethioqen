# Constants
DAYS_IN_ETH_MONTH = 30
MONTHS_IN_ETH_YEAR = 13

# Month lengths - most Ethiopian months have 30 days, except Pagume which has 5 or 6
ETH_MONTH_LENGTHS = {
    1: 30, 2: 30, 3: 30, 4: 30, 5: 30, 6: 30,
    7: 30, 8: 30, 9: 30, 10: 30, 11: 30, 12: 30,
    13: 5  # Will be 6 in leap years
}

def is_valid_ethiopian_date(year, month, day):
    """
    Check if the given Ethiopian date is valid.
    
    Args:
        year (int): Ethiopian year
        month (int): Ethiopian month (1-13)
        day (int): Ethiopian day
        
    Returns:
        bool: True if date is valid, False otherwise
    """
    # Basic range checks
    if month < 1 or month > MONTHS_IN_ETH_YEAR:
        return False
        
    # Handle Pagume (13th month) separately
    if month == 13:
        max_days = 6 if is_ethiopian_leap_year(year) else 5
        if day < 1 or day > max_days:
            return False
    else:
        # All other months have 30 days
        if day < 1 or day > DAYS_IN_ETH_MONTH:
            return False
            
    return True

def is_ethiopian_leap_year(year):
    """
    Determine if the given Ethiopian year is a leap year.
    Ethiopian leap years follow a simple rule: if the year divided by 4 has remainder 3.
    """
    return year % 4 == 3

def get_ethiopian_month_length(year, month):
    """
    Get the length of a given Ethiopian month in a specific year.
    
    Args:
        year (int): Ethiopian year
        month (int): Ethiopian month (1-13)
        
    Returns:
        int: Number of days in the month
    """
    if month == 13:
        return 6 if is_ethiopian_leap_year(year) else 5
    return DAYS_IN_ETH_MONTH