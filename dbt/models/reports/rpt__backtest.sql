with

    final as (
        select
            *,
            sum(profit) over (
                partition by symbol, strategy_id
                order by ts
                rows between unbounded preceding and current row
            ) as strategy_profit
        from {{ ref("int__backtest") }}
    )

select *
from final
