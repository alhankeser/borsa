with micro_indicators as (
    select
        symbol,
        timestamp,
        close as price,
        {{ get_indicators() }}
    from {{ ref("src__price_history") }}
),

prep_meta_indicators as (
    select
        *,
        {{ get_lags() }}
    from micro_indicators
),

meta_indicators as (
    select
        *,
        {{ get_meta_indicators() }}
    from prep_meta_indicators
),

final as (
    select *
    from meta_indicators
)

select * from final
