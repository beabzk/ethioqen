Welcome to ethioqen's documentation
================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   calendar_conversion
   time_conversion
   unix_time_conversion
   utils
   exceptions

Ethiopian Calendar and Time Conversion
===================================

ethioqen is a Python library for converting between Ethiopian and Gregorian calendars,
Ethiopian and standard time formats, and handling Unix timestamps with timezone support.

Installation
-----------

.. code-block:: bash

   pip install ethioqen

Quick Start
----------

Calendar Conversion
^^^^^^^^^^^^^^^^

.. code-block:: python

   from ethioqen.calendar_conversion import convert_ethiopian_to_gregorian

   greg_year, greg_month, greg_day = convert_ethiopian_to_gregorian(2016, 7, 6)
   print(f"{greg_year}-{greg_month}-{greg_day}")  # 2024-3-15

Time Conversion
^^^^^^^^^^^

.. code-block:: python

   from ethioqen.time_conversion import convert_to_ethiopian_time

   eth_hour, eth_minute, is_day = convert_to_ethiopian_time(14, 30)
   print(f"{eth_hour}:{eth_minute} {'AM' if is_day else 'PM'}")  # 8:30 PM

Unix Time Conversion
^^^^^^^^^^^^^^^^^

.. code-block:: python

   from ethioqen.unix_time_conversion import ethiopian_to_unix

   timestamp = ethiopian_to_unix(2016, 7, 6, 8, 30, tz_offset=3)
   print(timestamp)  # Unix timestamp for Ethiopian date/time

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`