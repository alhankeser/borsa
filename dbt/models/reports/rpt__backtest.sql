with

    indicators as (select * from {{ ref("int__indicators") }}),

    strategies as (select * from {{ ref("int__strategies") }}),

    backtest_results as (select * from {{ ref("int__backtest") }}),

    optimal_strategy as (select * from {{ ref("int__optimal_strategy") }}),

    final as (
        select
            i.symbol,
            i.ts,
            i.minutes_since_open,
            i.ts_day,
            i.price,
            {{ get_sma_columns(model="i") }}
            s.strategy_id,
            buys.buy_price,
            buys.buy_qty,
            buys.buy_value,
            sells.max_price,
            sells.sell_price,
            sells.sell_qty,
            sells.sell_value,
            sells.profit,
            sum(coalesce(sells.profit, 0)) over (
                partition by s.symbol, s.strategy_id
                order by s.ts
                rows between unbounded preceding and current row
            ) as profit_cumul,
            optimal_buy_window.symbol is not null as is_optimal_buy_window,
        from indicators as i
        left join strategies as s on i.ts = s.ts and i.symbol = s.symbol
        left join
            optimal_strategy as optimal_buy_window
            on i.symbol = optimal_buy_window.symbol
            and i.ts_day = optimal_buy_window.ts_day
            and i.ts between optimal_buy_window.best_buy_ts and date_add(
                optimal_buy_window.best_buy_ts, interval 10 minute
            )
        left join
            backtest_results as buys
            on buys.buy_ts = i.ts
            and buys.symbol = i.symbol
            and buys.strategy_id = s.strategy_id
        left join
            backtest_results as sells
            on sells.sell_ts = i.ts
            and sells.symbol = i.symbol
            and sells.strategy_id = s.strategy_id
    )

select *
from final
