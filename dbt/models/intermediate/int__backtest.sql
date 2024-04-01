with

    base as (
        select
            strategies.*,
            market_hours.market_open_ts,
            market_hours.market_close_ts,
        from {{ ref("int__strategies") }} strategies
        left join
            {{ ref("temp__market_hours") }} market_hours
            on market_hours.symbol = strategies.symbol
            and market_hours.ts_day = strategies.ts_day
    ),

    {{ get_simulated_trades(model = 'base') }}

    -- Good for debugging
    trades_raw as (select * from {{ union_trades() }}),

    final as (
        select
            symbol,
            strategy_id,
            ts,
            ts_day,
            last_buy_ts as buy_ts,
            last_buy_price as buy_price,
            last_buy_qty as buy_qty,
            last_buy_value as buy_value,
            sell_ts,
            sell_price,
            sell_qty,
            sell_value,
            sell_profit as profit,
        from trades_raw
    )
select *
from final
