with

backtest_results as (select * from {{ ref("backtest") }}),

profit_by_day as (
    select distinct
        symbol,
        ts,
        strategy_id,
        sum(coalesce(profit, 0)) as profit
    from backtest_results
    group by all
),

price_range_by_day as (
    select
        symbol,
        ts,
        any_value(price) as price_open,
        any_value(price) as price_close,
        price_close - price_open as price_diff,
        price_diff / price_open as price_diff_pct
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
        on price_range_by_day.ts = profit_by_day.ts
)

select *
from final
order by ts
