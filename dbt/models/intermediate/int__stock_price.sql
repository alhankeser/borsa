with

    final as (
        select
            symbol,
            ts,
            date_trunc('day', ts) as ts_day,
            close as price,
            floor({{ var("max_buy_value") }} / price) as max_qty,
        from {{ ref("src__stock_price") }}
    )

select *
from final
