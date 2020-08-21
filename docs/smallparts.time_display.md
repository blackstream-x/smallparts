# smallparts.time_display

> Functions for displaying time.  
> Source: [smallparts/time_display.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/time_display.py)

## Module contents

### Functions

smallparts.time\_display.**as\_date**(*datetime\_object*)

> Returns the ISO 8601 date formatting of the given
> [datetime.datetime](https://docs.python.org/3/library/datetime.html#datetime-objects) instance.

smallparts.time\_display.**as\_datetime**(*datetime\_object, with\_msec=False, with\_usec=False*)

> Returns the ISO 8601 date and time (separated by a blank) formatting of the given
> [datetime.datetime](https://docs.python.org/3/library/datetime.html#datetime-objects) instance.
> If *with\_usec* is given as ```True```, microseconds are included.
> If *with\_msec* is given as ```True```, microseconds are included.

smallparts.time\_display.**as\_time**(*datetime\_object, with\_msec=False, with\_usec=False*)

> Returns the time formatting of the given
> [datetime.datetime](https://docs.python.org/3/library/datetime.html#datetime-objects) instance.
> If *with\_usec* is given as ```True```, microseconds are included.
> If *with\_msec* is given as ```True```, microseconds are included.

### Class:

*class* smallparts.time\_display.**LooseTimedeltaFormatter**(*seconds=3600, minutes=1440, hours=168, days=70*)

Instances of this class can be used to format print time deltas
while "forgetting" to mention components when the total value of that component
is bigger than the given limit.  
With the default settings, this means: 
seconds are not mentioned for time deltas bigger than one hour,
minutes are omitted for time deltas bigger than on day,
hours are omitted for time deltas of more than a week, and days are omitted
when the time delta is more than 10 weeks.  
By setting the limit for a component to ```None``` or ```0```, the limits
for that component and all bigger components are removed.

Example for creating an instance and formatting *timedelta\_object* in french:

```python
ltdf_instance = LooseTimedeltaFormatter()
formatted_timedelta = ltdf_instance(timedelta_object, lang='fr')
```

* *timedelta\_object* must be a
  [datetime.timedelta](https://docs.python.org/3/library/datetime.html#timedelta-objects) instance.
* *lang* can be any language defined in
  [smallparts.l10n.languages](./smallparts.l10n.languages.md).**SUPPORTED**.  
  When omitted, it defaults
  to ```'en'``` as defined in [smallparts.l10n.languages](./smallparts.l10n.languages.md).**DEFAULT**.

The function uses the [smallparts.l10n.enumerations](./smallparts.l10n.enumerations.md).enumeration()
and [smallparts.l10n.time_indications](./smallparts.l10n.time_indications.md).format_component()
functions internally.

#### Class method:

LooseTimedeltaFormatter**.get_components**(*timedelta\_object*)

> Returns a tuple of two dicts: totals and values for each component
> (weeks, days, hurs, minutes and seconds)
> determined from *timedelta_object*.


## Usage examples

```python
>>> from smallparts import time_display
>>> import datetime
>>> time_display.as_date(datetime.datetime(2020, 7, 3, 22, 5, 59, 23678))
'2020-07-03'
>>> time_display.as_datetime(datetime.datetime(2020, 7, 3, 22, 5, 59, 23678))
'2020-07-03 22:05:59'
>>> time_display.as_datetime(datetime.datetime(2020, 7, 3, 22, 5, 59, 23678), with_usec=True)
'2020-07-03 22:05:59.023678'
>>> time_display.as_time(datetime.datetime(2020, 7, 3, 22, 5, 59, 23678), with_msec=True)
'22:05:59.023'
>>> 
>>> ltdf_defaults = time_display.LooseTimedeltaFormatter()
>>> date_1 = datetime.datetime(2020, 8, 1)
>>> date_2 = datetime.datetime(2020, 8, 7, 14, 30, 7)
>>> date_3 = datetime.datetime(2020, 8, 20, 17, 12)
>>> time_display.as_datetime(date_1)
'2020-08-01 00:00:00'
>>> time_display.as_datetime(date_2)
'2020-08-07 14:30:07'
>>> time_display.as_datetime(date_3)
'2020-08-20 17:12:00'
>>> ltdf_defaults(date_2 - date_1)
'6 days and 14 hours'
>>> ltdf_defaults(date_3 - date_1, lang='es')
'2 semanas y 5 dias'
>>> 
>>> ltdf_with_minutes = time_display.LooseTimedeltaFormatter(minutes=None)
>>> ltdf_with_minutes(date_2 - date_1)
'6 days, 14 hours and 30 minutes'
>>> ltdf_with_minutes(date_3 - date_1)
'2 weeks, 5 days, 17 hours and 12 minutes'
>>> 
```

----
[(smallparts docs home)](./)

