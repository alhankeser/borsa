with

    stock_price as (select * from {{ ref("int__stock_price") }}),

    timing as (
        select
            s.*,
            datediff('minute', market_open_ts, ts) as minutes_since_open, 
        from stock_price as s
        left join {{ ref("temp__market_hours") }} as m
            on m.ts_day = s.ts_day
            and m.symbol = s.symbol
    ),

    smas as (select *, {{ get_smas() }} from timing),

    smas_lagged as (select *, {{ get_indicator_lags() }} from smas),

    continuation as (select *, {{ get_continuation() }} from smas_lagged),

    continuation_lagged as (
        select *, {{ get_continuation_lags() }} from continuation
    ),

    reversal as (select *, {{ get_reversal() }} from continuation_lagged),

    final as (select * from reversal)

select *
from final
