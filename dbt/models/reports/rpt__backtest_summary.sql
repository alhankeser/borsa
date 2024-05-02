with

    backtest_results as (select * from {{ ref("rpt__backtest") }}),

    final as (
        select
            symbol,
            strategy_id,
            sum(profit) as profit,
            sum(
                case
                    when buy_qty > 0 and is_optimal_buy_window then 1 else 0
                end
            )
            / sum(case when buy_qty > 0 then 1 else 0 end) as optimalness,
        from backtest_results
        group by all
    )

select *
from final
