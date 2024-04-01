with

    stock_price as (select * from {{ ref("int__stock_price") }}),

    strategies as (select * from {{ union_strategies() }}),
    final as (
        select stock_price.*, strategies.strategy_id, strategies.buy,
        from stock_price
        left join
            strategies
            on stock_price.symbol = strategies.symbol
            and stock_price.ts = strategies.ts
    )
select *
from final
