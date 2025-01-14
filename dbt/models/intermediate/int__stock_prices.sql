with

source as (select * from {{ ref("stg__stock_prices") }}),

final as (
    select
        symbol,
        ts,
        epoch,
        price,
        _extracted_at,
        _dbt_run_started_at
    from source
)

select *
from final
