with

    -- Need to replace with actual hours
    final as (
        select
            ts_day,
            symbol,
            min(ts) as market_open_ts,
            max(ts) as market_close_ts,
        from {{ ref("int__stock_price") }}
        group by all
    )

select *
from final
