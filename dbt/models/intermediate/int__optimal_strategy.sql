with

indicators as (select * from {{ ref("int__indicators") }}),

optimal_strategy as (
    select
        i1.symbol,
        i1.price as best_buy_price,
        i1.ts as best_buy_ts,
        i2.price as best_sell_price,
        i2.ts as best_sell_ts,
        i2.price - i1.price as best_price_diff
    from indicators as i1
    left join
        indicators as i2
        on
            i1.ts = i2.ts
            and i1.symbol = i2.symbol
    where
        i2.price - i1.price > 0
    qualify
        row_number()
            over (
                partition by i1.symbol
                order by i2.price - i1.price desc
            )
        = 1
),

final as (
    select
        symbol,
        best_buy_price,
        best_buy_ts,
        best_sell_price,
        best_sell_ts,
        best_price_diff
    from optimal_strategy
)

select *
from final
