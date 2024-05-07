with
    optimal_strategy as (select * from {{ ref("int__optimal_strategy") }}),

    indicators as (select * from {{ ref("int__indicators") }}),

    final as (
        select i.*, os.symbol is not null as is_optimal_buy_window,
        from indicators as i
        left join
            optimal_strategy as os
            on os.symbol = i.symbol
            and i.ts between os.best_buy_ts and date_add(
                os.best_buy_ts, interval 10 minute
            )
    )

select *
from final
