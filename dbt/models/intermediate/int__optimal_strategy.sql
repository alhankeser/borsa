with

    indicators as (select * from {{ ref("int__indicators") }}),

    optimal_strategy as (
        select
            i1.symbol,
            i1.ts_day,
            i1.price as best_buy_price,
            i1.ts as best_buy_ts,
            i1.minutes_since_open as best_buy_minutes_since_open,
            i2.price as best_sell_price,
            i2.ts as best_sell_ts,
            i2.minutes_since_open as best_sell_minutes_since_open,
            i2.price - i1.price as best_price_diff,
        from indicators as i1
        left join
            indicators as i2
            on i2.ts > i1.ts
            and i2.ts_day = i1.ts_day
            and i2.symbol = i1.symbol
        where i2.price - i1.price > 0
        and i1.minutes_since_open >= {{ var("buy_after_minutes") }}
        qualify
            row_number() over (
                partition by i1.symbol, i1.ts_day
                order by i2.price - i1.price desc
            )
            = 1
    ),

    final as (
        select
            symbol,
            ts_day,
            best_buy_price,
            best_buy_ts,
            best_buy_minutes_since_open,
            best_sell_price,
            best_sell_ts,
            best_sell_minutes_since_open,
            best_price_diff,
        from optimal_strategy
    )

select *
from final
