with

    final as (
        select distinct
            s.symbol,
            s.ts,
            s.epoch,
            date_trunc('day', s.ts) as ts_day,
            s.price,
            s.up_volume,
            s.down_volume,
            s.total_volume,
            floor({{ var("max_buy_value") }} / s.price) as max_qty,
            datediff('minute', m.market_open_ts, s.ts) as minutes_since_open, 
        from {{ ref("src__stock_price") }} s
        left join {{ ref("temp__market_hours") }} as m
            on m.ts_day = date_trunc('day', s.ts)
            and m.symbol = s.symbol
    )

select *
from final
