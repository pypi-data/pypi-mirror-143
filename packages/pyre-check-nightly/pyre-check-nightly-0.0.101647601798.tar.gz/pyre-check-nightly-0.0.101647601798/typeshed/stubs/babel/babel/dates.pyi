from datetime import date, datetime, time
from typing import Any

NO_INHERITANCE_MARKER: str
LC_TIME: Any
date_ = date
datetime_ = datetime
time_ = time

def get_timezone(zone: Any | None = ...): ...
def get_next_timezone_transition(zone: Any | None = ..., dt: Any | None = ...): ...

class TimezoneTransition:
    activates: Any
    from_tzinfo: Any
    to_tzinfo: Any
    reference_date: Any
    def __init__(self, activates, from_tzinfo, to_tzinfo, reference_date: Any | None = ...) -> None: ...
    @property
    def from_tz(self): ...
    @property
    def to_tz(self): ...
    @property
    def from_offset(self): ...
    @property
    def to_offset(self): ...

def get_period_names(width: str = ..., context: str = ..., locale=...): ...
def get_day_names(width: str = ..., context: str = ..., locale=...): ...
def get_month_names(width: str = ..., context: str = ..., locale=...): ...
def get_quarter_names(width: str = ..., context: str = ..., locale=...): ...
def get_era_names(width: str = ..., locale=...): ...
def get_date_format(format: str = ..., locale=...): ...
def get_datetime_format(format: str = ..., locale=...): ...
def get_time_format(format: str = ..., locale=...): ...
def get_timezone_gmt(datetime: Any | None = ..., width: str = ..., locale=..., return_z: bool = ...): ...
def get_timezone_location(dt_or_tzinfo: Any | None = ..., locale=..., return_city: bool = ...): ...
def get_timezone_name(
    dt_or_tzinfo: Any | None = ...,
    width: str = ...,
    uncommon: bool = ...,
    locale=...,
    zone_variant: Any | None = ...,
    return_zone: bool = ...,
): ...
def format_date(date: Any | None = ..., format: str = ..., locale=...): ...
def format_datetime(datetime: Any | None = ..., format: str = ..., tzinfo: Any | None = ..., locale=...): ...
def format_time(time: Any | None = ..., format: str = ..., tzinfo: Any | None = ..., locale=...): ...
def format_skeleton(skeleton, datetime: Any | None = ..., tzinfo: Any | None = ..., fuzzy: bool = ..., locale=...): ...

TIMEDELTA_UNITS: Any

def format_timedelta(
    delta, granularity: str = ..., threshold: float = ..., add_direction: bool = ..., format: str = ..., locale=...
): ...
def format_interval(start, end, skeleton: Any | None = ..., tzinfo: Any | None = ..., fuzzy: bool = ..., locale=...): ...
def get_period_id(time, tzinfo: Any | None = ..., type: Any | None = ..., locale=...): ...
def parse_date(string, locale=...): ...
def parse_time(string, locale=...): ...

class DateTimePattern:
    pattern: Any
    format: Any
    def __init__(self, pattern, format) -> None: ...
    def __unicode__(self): ...
    def __mod__(self, other): ...
    def apply(self, datetime, locale): ...

class DateTimeFormat:
    value: Any
    locale: Any
    def __init__(self, value, locale) -> None: ...
    def __getitem__(self, name): ...
    def extract(self, char): ...
    def format_era(self, char, num): ...
    def format_year(self, char, num): ...
    def format_quarter(self, char, num): ...
    def format_month(self, char, num): ...
    def format_week(self, char, num): ...
    def format_weekday(self, char: str = ..., num: int = ...): ...
    def format_day_of_year(self, num): ...
    def format_day_of_week_in_month(self): ...
    def format_period(self, char): ...
    def format_frac_seconds(self, num): ...
    def format_milliseconds_in_day(self, num): ...
    def format_timezone(self, char, num): ...
    def format(self, value, length): ...
    def get_day_of_year(self, date: Any | None = ...): ...
    def get_week_number(self, day_of_period, day_of_week: Any | None = ...): ...

PATTERN_CHARS: Any
PATTERN_CHAR_ORDER: str

def parse_pattern(pattern): ...
def tokenize_pattern(pattern): ...
def untokenize_pattern(tokens): ...
def split_interval_pattern(pattern): ...
def match_skeleton(skeleton, options, allow_different_fields: bool = ...): ...
