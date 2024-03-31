with base as (
    select
        symbol,
        ts,
        price,
    from
        {{ ref("_indicators") }}
),
strategies as (
    select
        *
    from
        {{ union_strategies() }}
),
final as (
    select
        base.symbol,
        base.ts,
        base.price,
        strategies.id,
        strategies.side,
    from
        base
        left join strategies on base.symbol = strategies.symbol
        and base.ts = strategies.ts
)
select
    *
from
    final