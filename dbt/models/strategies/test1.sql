with

final as (
    select
        symbol,
        ts,
        price,
        'test1' as  id,
        case 
            when (sma5cntdwn3) then -1 
            when (sma1cntdwn5 and sma5cntup2) then 1 
        end as side,
    from {{ ref("_indicators") }}
)

select *
from final
