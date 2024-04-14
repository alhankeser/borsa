with

    -- Need to replace with actual hours
    final as (
        select
            date_trunc('day', ts) as ts_day,
            symbol,
            min(ts) as market_open_ts,
            max(ts) as market_close_ts,
        from {{ ref("src__stock_price") }}
        group by all
    )

select *
from final
