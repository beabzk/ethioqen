from .exceptions import InvalidTimeException
from .utils import is_valid_eth_time, is_valid_time

def convert_to_ethiopian_time(hour, minute, period=None):
    """Convert 24-hour time to Ethiopian time."""
    if not is_valid_time(hour, minute):
        raise InvalidTimeException(f"Invalid time: {hour}:{minute}")

    # Handle 12-hour format with AM/PM
    if period:
        if period.upper() not in ["AM", "PM"]:
            raise InvalidTimeException("Period must be 'AM' or 'PM'")
        if period.upper() == "PM" and hour != 12:
            hour += 12
        elif period.upper() == "AM" and hour == 12:
            hour = 0

    # Ethiopian time starts 6 hours before standard time
    eth_hour = (hour - 6) % 12
    if eth_hour == 0:
        eth_hour = 12
        
    # Determine if it's morning/day (AM) or evening/night (PM)
    is_am = 6 <= hour < 18

    return eth_hour, minute, is_am

def convert_from_ethiopian_time(eth_hour, minute, is_am=True):
    """Convert Ethiopian time to 24-hour time."""
    if not (1 <= eth_hour <= 12) or not (0 <= minute <= 59):
        raise InvalidTimeException(f"Invalid Ethiopian time: {eth_hour}:{minute}")

    # Convert Ethiopian time to 24-hour format
    std_hour = eth_hour % 12  # Convert 12 to 0
    
    # Add 6 hours to align with standard time
    std_hour = (std_hour + 6) % 24
    
    # Adjust for AM/PM
    if not is_am:
        std_hour = (std_hour + 12) % 24
        
    return std_hour, minute