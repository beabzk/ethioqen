# ethioqen: Ethiopian Calendar, Time, and Unix Timestamp Conversion

> ⚠️ **Warning**: This library is in very early stages of development and should not be used in production. Contributions are crucial to make this production-ready.

[![PyPI version](https://badge.fury.io/py/ethioqen.svg)](https://badge.fury.io/py/ethioqen)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/beabzk/ethioqen/actions/workflows/main.yml/badge.svg)](https://github.com/beabzk/ethioqen/actions)

`ethioqen` is a Python library that provides accurate and efficient conversions between the Ethiopian calendar, the Gregorian calendar, Ethiopian local time (12-hour format), standard 24-hour local time, and Unix timestamps.

## Introduction

The Ethiopian calendar is a solar calendar used in Ethiopia and Eritrea. It differs significantly from the Gregorian calendar, which is the most widely used calendar system today.

**Key Differences:**

* **Year Offset:** The Ethiopian calendar is typically 7-8 years behind the Gregorian calendar.
* **Months:** It has 13 months: 12 months of 30 days each and a 13th month called *Pagume*, which has 5 days (6 days in a leap year).
* **New Year:** The Ethiopian New Year (*Enkutatash*) falls on September 11th (or 12th in a Gregorian leap year).
* **Leap Years:** Ethiopia follows a simple 4-year leap year cycle without the century exception found in the Gregorian calendar.

**Ethiopian Local Time:**

Ethiopian time uses a 12-hour clock that starts counting from dawn (around 6:00 AM standard time). This creates a 6-hour offset between Ethiopian and standard time:

* 12:00 AM Ethiopian = 6:00 AM standard time
* 1:00 AM Ethiopian = 7:00 AM standard time
* 12:00 PM Ethiopian = 6:00 PM standard time
* 6:00 PM Ethiopian = 12:00 AM standard time (next day)

## Installation

```bash
pip install ethioqen
```

## Usage Examples

### Calendar Conversions

```python
from ethioqen.calendar_conversion import convert_ethiopian_to_gregorian, convert_gregorian_to_ethiopian

# Convert from Ethiopian to Gregorian
greg_year, greg_month, greg_day = convert_ethiopian_to_gregorian(2016, 7, 6)
print(f"{greg_year}-{greg_month}-{greg_day}")  # Output: 2024-3-15

# Convert from Gregorian to Ethiopian
eth_year, eth_month, eth_day = convert_gregorian_to_ethiopian(2024, 3, 15)
print(f"{eth_year}-{eth_month}-{eth_day}")  # Output: 2016-7-6
```

### Time Conversions

```python
from ethioqen.time_conversion import convert_to_ethiopian_time, convert_from_ethiopian_time

# Convert standard time (14:30 / 2:30 PM) to Ethiopian time
eth_hour, eth_minute, is_day = convert_to_ethiopian_time(14, 30)
print(f"{eth_hour}:{eth_minute} {'AM' if is_day else 'PM'}")  # Output: 8:30 PM

# Convert Ethiopian time (8:30 PM) to standard time
std_hour, std_minute = convert_from_ethiopian_time(8, 30, is_am=False)
print(f"{std_hour:02d}:{std_minute:02d}")  # Output: 14:30
```

### Unix Timestamp Conversions

```python
from ethioqen.unix_time_conversion import ethiopian_to_unix, unix_to_ethiopian

# Convert Ethiopian date/time to Unix timestamp (UTC)
# 1:30 PM Ethiopian time
timestamp = ethiopian_to_unix(2016, 7, 6, eth_hour=1, minute=30, is_pm=True)
print(timestamp)  # Output: Unix timestamp

# Convert Unix timestamp to Ethiopian date/time (UTC)
eth_year, eth_month, eth_day, hour, minute, is_pm = unix_to_ethiopian(timestamp)
print(f"{eth_year}-{eth_month}-{eth_day} {hour}:{minute:02d} {'PM' if is_pm else 'AM'}")  
# Output: 2016-7-6 1:30 PM
```

### Timezone Support

```python
from ethioqen.unix_time_conversion import ethiopian_to_unix, unix_to_ethiopian

# Convert with timezone offset (UTC+3 for Ethiopia)
# 8:30 AM Ethiopian time
timestamp = ethiopian_to_unix(2016, 7, 6, eth_hour=8, minute=30, is_pm=False, tz_offset=3)
print(timestamp)  # Output: Unix timestamp adjusted for UTC+3

# Convert back with timezone offset
eth_date = unix_to_ethiopian(timestamp, tz_offset=3)
print(f"{eth_date[0]}-{eth_date[1]}-{eth_date[2]} {eth_date[3]}:{eth_date[4]:02d} {'PM' if eth_date[5] else 'AM'}")  
# Output: Ethiopian date/time in UTC+3
```

## Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs**
   * Open an issue in the [GitHub issue tracker](https://github.com/beabzk/ethioqen/issues)
   * Include a clear description and steps to reproduce

2. **Submit Pull Requests**
   * Fork the repository
   * Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
   * Make your changes
   * Write or update tests as needed
   * Update documentation if necessary
   * Submit a pull request

3. **Coding Style**
   * Follow PEP 8 guidelines
   * Include docstrings for new functions/classes
   * Add type hints where possible

4. **Testing**
   * Run the test suite: `pytest`
   * Add tests for new features
   * Ensure all tests pass before submitting

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
