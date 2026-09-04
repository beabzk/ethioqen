# Changelog

All notable changes to this project are documented here. Versioning follows
Semantic Versioning: breaking changes ship as minor releases, fixes as patches.

## [Unreleased]

### Breaking

- `time_conversion`: `is_am`/`is_day` renamed to `is_pm` across
  `convert_to_ethiopian_time` and `convert_from_ethiopian_time`.
  Day is `is_pm=False`, night is `is_pm=True`.
- `unix_time_conversion`: `unix_to_ethiopian` returns a 7-tuple
  `(year, month, day, eth_hour, minute, second, is_pm)`; seconds are no
  longer truncated. `ethiopian_to_unix` accepts a matching `second`
  parameter (default 0).
- `utils`: removed `is_valid_eth_time` (validated the wrong 0–23 range for
  a 1–12 clock and was unused). Use `is_valid_ethiopian_hour` or
  `is_valid_standard_time`.
- `unix_time_conversion`: invalid hours/minutes now raise
  `InvalidTimeException` instead of `InvalidDateException`.

### Added

- `utils.is_valid_gregorian_date`: real Gregorian validation via
  `calendar.monthrange` (Feb 29, 30-day months, non-integer rejection).
- `utils.is_valid_ethiopian_hour` and `utils.is_valid_standard_time`
  with strict integer guards.
- `time_conversion.eth_to_24h` / `h24_to_eth`: single shared 6-hour-shift
  helpers, reused by `unix_time_conversion`.
- `unix_time_conversion`: fractional `tz_offset` support (e.g. 5.5, 5.75);
  portable out-of-range timestamp errors on all platforms.
- Top-level API: `from ethioqen import ...` now works for all converters
  and both exception types (`__all__` defined).

### Fixed

- `convert_gregorian_to_ethiopian` rejects impossible dates (e.g.
  2023-02-29, 2023-04-31) instead of converting them silently.
- `convert_to_ethiopian_time` with a 12-hour `period` rejects hours
  outside 1–12 instead of producing silent garbage.
- `_jdn_to_ethiopian` rewritten with integer math; Pagume handling falls
  out by construction.

## [0.2.2] — 2026-09-04

Tooling modernization, no behavior changes:

- `requires-python >=3.10` (classifiers through 3.14), hatchling build
  backend, single-source metadata in `pyproject.toml`.
- `uv` dependency groups + committed `uv.lock`; `ruff` replaces
  black/flake8/isort; `bump-my-version` replaces `bumpversion`.
- CI matrix (3.10–3.14), official GitHub Pages artifact flow, trusted
  PyPI publishing, weekly Dependabot.

## [0.2.1] and earlier

See git history.
