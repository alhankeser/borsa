with
    smas as (
        select symbol, timestamp, close as price, {{ get_smas() }}
        from {{ ref("src__price_history") }}
    ),

    smas_lagged as (select *, {{ get_indicator_lags() }} from smas),

    final as (select * from smas_lagged)

select *
from final
