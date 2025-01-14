with

stock_prices as (select * from {{ ref("int__stock_prices") }}),

optimal_strategy as (
    select
        stock_prices.symbol,
        stock_prices.ts,
        'optimal' as strategy_id,
        optimal_strategy.best_buy_ts is not null as buy
    from stock_prices
    left join
        {{ ref("int__optimal_strategy") }} as optimal_strategy
        on
            stock_prices.symbol = optimal_strategy.symbol
            and stock_prices.ts = optimal_strategy.best_buy_ts
),

strategies as (select * from {{ union_strategies() }}),

final as (
    select
        stock_prices.*,
        strategies.strategy_id,
        strategies.buy
    from stock_prices
    left join
        (
            select * from strategies
            {% if var("include_optimal_strategy") %}
                union all
                select * from optimal_strategy
            {% endif %}
        )
            as strategies
        on
            stock_prices.symbol = strategies.symbol
            and stock_prices.ts = strategies.ts
)

select *
from final
