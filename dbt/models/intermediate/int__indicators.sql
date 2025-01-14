with

stock_prices as (select * from {{ ref("int__stock_prices") }}),

smas as (select
    *, {{ get_smas() }} from stock_prices),

smas_lagged as (select
    *, {{ get_indicator_lags() }} from smas),

continuation as (select
    *, {{ get_continuation() }} from smas_lagged),

continuation_lagged as (
    select
        *, {{ get_continuation_lags() }}        {{ get_continuation_lags() }} from continuation
),

reversal as (select
    *, {{ get_reversal() }} from continuation_lagged),

crosses as (select
    *, {{ get_crosses() }} from reversal),

final as (select * from crosses)

select *
from final
