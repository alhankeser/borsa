with final as (select * from {{ ref("reversal") }}) select * from final
