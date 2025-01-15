with

indicators as (select * from {{ ref("int__indicators") }}),

diffs_by_ts as (
    select
        i1.symbol,
        i1.ts,
        i1.price as buy_price,
        i1.ts as buy_ts,
        i2.price as sell_price,
        i2.ts as sell_ts,
        i2.price - i1.price as price_diff,
        price_diff / i1.price as price_diff_rate
    from indicators as i1
    left join
        indicators as i2
        on
            i1.ts < i2.ts
            and i1.symbol = i2.symbol
    where
        i2.price - i1.price > 0
        and i1.ts > '2021-01-01'
    qualify
        row_number()
            over (
                partition by i1.symbol, i1.ts
                order by i2.price - i1.price desc
            )
        = 1
),

optimal_strategy as (
    select
        symbol,
        ts,
        buy_price as best_buy_price,
        buy_ts as best_buy_ts,
        sell_price as best_sell_price,
        sell_ts as best_sell_ts,
        price_diff as best_price_diff,
        price_diff_rate as best_price_diff_rate
    from diffs_by_ts
    qualify
        row_number()
            over(
                partition by symbol
                order by price_diff_rate desc
            )
        <= 3
),

all_optimal_indicators as (
    select
        optimal_strategy.symbol,
        optimal_strategy.ts,
        optimal_strategy.best_buy_price,
        optimal_strategy.best_buy_ts,
        optimal_strategy.best_sell_price,
        optimal_strategy.best_sell_ts,
        optimal_strategy.best_price_diff,
        optimal_strategy.best_price_diff_rate,
        
        {{ dbt_utils.star(from=ref("int__indicators"), relation_alias="buy_indicators", except=["symbol", "ts"], prefix="buy_", quote_identifiers=False) }},
        {{ dbt_utils.star(from=ref("int__indicators"), relation_alias="sell_indicators", except=["symbol", "ts"], prefix="sell_", quote_identifiers=False) }}

    from optimal_strategy
    left join indicators as buy_indicators
        on optimal_strategy.best_buy_ts = buy_indicators.ts
        and optimal_strategy.symbol = buy_indicators.symbol
    left join indicators as sell_indicators
        on optimal_strategy.best_sell_ts = sell_indicators.ts
        and optimal_strategy.symbol = sell_indicators.symbol
),

final as (
    select 
        symbol,
        ts,
        best_buy_price,
        best_buy_ts,
        best_sell_price,
        best_sell_ts,
        best_price_diff,
        best_price_diff_rate,
        buy_sma0,
        buy_sma5,
        buy_sma10,
        buy_sma20,
        buy_sma40,
        buy_sma0cntdwn1,
        buy_sma0cntdwn2,
        buy_sma0cntdwn3,
        buy_sma0cntdwn4,
        buy_sma0cntdwn5,
        buy_sma5cntdwn1,
        buy_sma5cntdwn2,
        buy_sma5cntdwn3,
        buy_sma5cntdwn4,
        buy_sma5cntdwn5,
        buy_sma10cntdwn1,
        buy_sma10cntdwn2,
        buy_sma10cntdwn3,
        buy_sma10cntdwn4,
        buy_sma10cntdwn5,
        buy_sma20cntdwn1,
        buy_sma20cntdwn2,
        buy_sma20cntdwn3,
        buy_sma20cntdwn4,
        buy_sma20cntdwn5,
        buy_sma40cntdwn1,
        buy_sma40cntdwn2,
        buy_sma40cntdwn3,
        buy_sma40cntdwn4,
        buy_sma40cntdwn5
    from all_optimal_indicators
)

select *
from final
