with last_values as (
    select
        *,
        last_value(side ignore nulls) over (partition by id, symbol order by ts) as last_side
    from {{ ref("_strategies") }}
),

lagged as (
    select
        *,
        lag(last_side, 1) over (partition by id, symbol order by ts) as prev_side,
    from last_values
)

select
    *,
    case 
        when (prev_side is null or prev_side = -1) and last_side = 1 then price
    end as last_buy_price,
    case 
        when prev_side = 1 and last_side = -1 then price
    end as last_sell_price,
from lagged
where ts between '2018-12-18' and '2018-12-19'
and id = 'test1'