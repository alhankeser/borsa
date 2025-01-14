with

base as (select * from {{ ref("int__strategies") }}),

{{ get_simulated_trades(model = 'base') }}

-- Good for debugging
trades_raw as (select * from {{ union_trades() }}),

final as (
    select
        symbol,
        strategy_id,
        ts,
        epoch,
        last_buy_ts as buy_ts,
        last_buy_price as buy_price,
        last_buy_qty as buy_qty,
        last_buy_value as buy_value,
        max_price,
        sell_ts,
        sell_price,
        sell_qty,
        sell_value,
        sell_profit as profit
    from trades_raw
)

select *
from final
