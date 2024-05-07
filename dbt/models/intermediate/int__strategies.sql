with

    stock_price as (select * from {{ ref("int__stock_price") }}),

    optimal_strategy as (
        select
            stock_price.symbol,
            stock_price.ts,
            'optimal' as strategy_id,
            optimal_strategy.best_buy_ts is not null as buy,
        from stock_price
        left join
            {{ ref("int__optimal_strategy") }} optimal_strategy
            on stock_price.symbol = optimal_strategy.symbol
            and stock_price.ts = optimal_strategy.best_buy_ts
    ),

    strategies as (select * from {{ union_strategies() }}),

    final as (
        select stock_price.*, strategies.strategy_id, strategies.buy,
        from stock_price
        left join
            (
                select * from strategies
                {% if var("include_optimal_strategy") %}
                union all
                select * from optimal_strategy
                {% endif %}
            )
            strategies
            on stock_price.symbol = strategies.symbol
            and stock_price.ts = strategies.ts
    )

select *
from final
