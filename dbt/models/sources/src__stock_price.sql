select distinct
    symbol as symbol,
    high::double as high,
    low::double as low,
    open::double as open,
    close::double as price,
    timestamp::datetime as ts,
    totalvolume::int as total_volume,
    downticks::int as down_ticks,
    downvolume::int as down_volume,
    openinterest::int as open_interest,
    isrealtime::boolean as is_realtime,
    isendofhistory::boolean as is_endofhistory,
    totalticks::int as total_ticks,
    unchangedticks::int as unchanged_ticks,
    unchangedvolume::int as unchanged_volume,
    upticks::int as up_ticks,
    upvolume::int as up_volume,
    epoch::int64 as epoch,
    barstatus as bar_status,

{% if target.name == 'prod' %}
    from {{ source("prod", "stock_price") }}
{% endif %}

{% if target.name == 'dev' %}
    from {{ source("dev", "stock_price") }}
{% endif %}
