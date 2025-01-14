with

source as (select * from {{ source("stocks", "prices") }}),

final as (
    select
        source.symbol,
        candles.high::double as high,
        candles.low::double as low,
        candles.open::double as open,
        candles.close::double as price,
        candles.volume::int64 as total_volume,
        candles.datetime::int64 as epoch,
        make_timestamp(candles.datetime * 1000)::timestamp as ts,
        '{{ run_started_at }}'::timestamp as _dbt_run_started_at,
        _extracted_at::timestamp as _extracted_at
    from source
    where not empty
)

select * from final
