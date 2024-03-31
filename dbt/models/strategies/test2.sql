with

final as (
    select
        symbol,
        ts,
        'test2' as id,
        case 
            when (sma5cntup3) then -1 
            when (sma40cntup5 and sma10cntdwn3) then 1 
        end as side,
    from {{ ref("_indicators") }}
)

select * from final
