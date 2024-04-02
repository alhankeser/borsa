with

    final as (
        select
            symbol,
            ts,
            epoch,
            date_trunc('day', ts) as ts_day,
            price, 
            floor({{ var("max_buy_value") }} / price) as max_qty,
        from {{ ref("src__stock_price") }}
    )

select *
from final
