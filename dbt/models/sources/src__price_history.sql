select distinct
    Symbol as symbol,
    High::double as high,
    Low::double as low,
    Open::double as open,
    Close::double as close,
    TimeStamp,
    TimeStamp::datetime as timestamp,
    TotalVolume::int as total_volume,
    DownTicks::int as down_ticks,
    DownVolume::int as down_volume,
    OpenInterest::int as open_interest,
    IsRealtime::boolean as is_realtime,
    IsEndOfHistory::boolean as is_endofhistory,
    TotalTicks::int as total_ticks,
    UnchangedTicks::int as unchanged_ticks,
    UnchangedVolume::int as unchanged_volume,
    UpTicks::int as up_ticks,
    UpVolume::int as up_volume,
    Epoch::int64 as epoch,
    BarStatus as bar_status,
from {{ source("local", "stocks") }}

{% if target.name == 'dev' %}
    where timestamp > '2024-03-25'
{% endif %}