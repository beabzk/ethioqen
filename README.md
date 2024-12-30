# ethioqen: Ethiopian Calendar, Time, and Unix Timestamp Conversion

<!-- [![PyPI version](https://badge.fury.io/py/ethioqen.svg)](https://badge.fury.io/py/ethioqen)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/<your-username>/ethioqen/actions/workflows/main.yml/badge.svg)](https://github.com/<your-username>/ethioqen/actions) -->

`ethioqen` is a Python library that provides accurate and efficient conversions between the Ethiopian calendar, the Gregorian calendar, Ethiopian local time, standard 24-hour local time, and Unix timestamps (seconds since the Unix epoch).

## Introduction

The Ethiopian calendar is a solar calendar used in Ethiopia and Eritrea. It differs significantly from the Gregorian calendar, which is the most widely used calendar system today.

**Key Differences:**

* **Year Offset:** The Ethiopian calendar is typically 7-8 years behind the Gregorian calendar.
* **Months:** It has 13 months: 12 months of 30 days each and a 13th month called *Pagume*, which has 5 days (6 days in a leap year).
* **New Year:** The Ethiopian New Year (*Enkutatash*) falls on September 11th (or 12th in a Gregorian leap year).
* **Leap Years:**  Ethiopia follows a simple 4-year leap year cycle without the century exception found in the Gregorian calendar.

**Ethiopian Local Time:**

Ethiopian local time is traditionally counted from sunrise (around 6:00 AM in standard local time). This means there's roughly a 6-hour offset between Ethiopian local time and standard 24-hour time.

**Example:**

* 1:00 Ethiopian local time ≈ 7:00 AM standard local time
* 12:00 Ethiopian local time (noon) ≈ 6:00 PM standard local time

**Unix Time:**

Unix time represents a point in time as the number of seconds that have elapsed since January 1, 1970, at 00:00:00 Coordinated Universal Time (UTC), not counting leap seconds. `ethioqen` facilitates conversions between Unix time and Ethiopian date/time, taking time zone offsets into account.

<!-- ## Installation

```bash
pip install ethioqen -->
