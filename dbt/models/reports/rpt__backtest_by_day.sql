with

backtest_results as (
    select * from {{ ref("rpt__backtest") }}
    where minutes_since_open <= {{ var("sell_by_minutes") }}
),

profit_by_day as (
    select distinct
        symbol,
        ts_day,
        strategy_id,
        sum(coalesce(profit, 0)) as profit,
    from backtest_results
    group by all
),

price_range_by_day as (
    select
        symbol,
        ts_day,
        any_value(case when minutes_since_open = 1 then price end) as price_open,
        any_value(case when minutes_since_open = {{ var("sell_by_minutes") }} then price end) as price_close,
        price_close - price_open as price_diff,
        price_diff / price_open as price_diff_pct,
    from backtest_results
    group by all
),

final as (
    select
        price_range_by_day.*,
        profit_by_day.strategy_id,
        profit_by_day.profit
    from price_range_by_day
    left join profit_by_day
        on profit_by_day.ts_day = price_range_by_day.ts_day
)

select *
from final
order by ts_day