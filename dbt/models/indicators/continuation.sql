with

    continuation as (select *, {{ get_continuation() }} from {{ ref("smas") }}),

    continuation_lagged as (select *, {{ get_continuation_lags() }} from continuation),

    final as (select * from continuation_lagged)

select *
from final
