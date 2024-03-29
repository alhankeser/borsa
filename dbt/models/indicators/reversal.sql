with
    reversal as (select *, {{ get_reversal() }} from {{ ref("continuation") }}),

    final as (select * from reversal)

select *
from final
