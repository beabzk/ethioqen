Migration Guide
===============

This guide covers breaking changes between releases.

0.2.x to 0.3.0
--------------

Day/night flag renamed
^^^^^^^^^^^^^^^^^^^^^^

`is_am` (and the documented-but-never-implemented `is_day`) is now `is_pm`
everywhere. Day is `is_pm=False`, night is `is_pm=True`.

.. code-block:: python

   # Before (0.2.x)
   eth_hour, eth_minute, is_am = convert_to_ethiopian_time(14, 30)
   std_hour, std_minute = convert_from_ethiopian_time(8, 30, is_am=False)

   # After (0.3.0)
   eth_hour, eth_minute, is_pm = convert_to_ethiopian_time(14, 30)
   std_hour, std_minute = convert_from_ethiopian_time(8, 30, is_pm=False)

Unix conversions gained seconds
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`unix_to_ethiopian` returns a 7-tuple with seconds inserted before `is_pm`;
`ethiopian_to_unix` accepts a matching `second` parameter (default 0).

.. code-block:: python

   # Before (0.2.x)
   year, month, day, hour, minute, is_pm = unix_to_ethiopian(timestamp)

   # After (0.3.0)
   year, month, day, hour, minute, second, is_pm = unix_to_ethiopian(timestamp)
   timestamp = ethiopian_to_unix(2015, 1, 1, 1, 30, True, second=45)

Parameter and exception changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `ethiopian_to_unix` parameters `e_year`, `e_month`, `e_day` are now
  `eth_year`, `eth_month`, `eth_day`. Positional callers are unaffected.
* Invalid hours/minutes/seconds now raise `InvalidTimeException` instead of
  `InvalidDateException`. Catch sites matching on the old type need updating.
* The ``is_valid_eth_time`` helper was removed (it validated the wrong
  range). Use ``is_valid_ethiopian_hour`` or ``is_valid_standard_time``.
* Prefer top-level imports: ``from ethioqen import ethiopian_to_unix``.
  Deep module paths keep working.
