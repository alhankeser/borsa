{% macro get_simulated_trades(
            model=ref('int__strategies'),
            output_cte_name="trades",
            iteration=0,
            max_iterations=var("max_buys_per_day"),
            cols="symbol, ts, epoch, ts_day, minutes_since_open, market_open_ts, market_close_ts, price, max_qty, strategy_id, buy",
            partition_cols="strategy_id, symbol, ts_day")
        %}

    potential_buys_{{ iteration }} as (
        select
            {{ cols }},
            case
                when buy
                then
                    row_number() over (
                        partition by {{ partition_cols }}, buy order by ts
                    )
            end as buy_rank
        from {{ model }}
        {% if iteration > 0 %} where ts > first_sell_ts {% endif %}
    ),

    simulate_buy_{{ iteration }} as (
        select
            {{ cols }},
            case when buy_rank = 1 then ts end as buy_ts,
            case when buy_rank = 1 then price end as buy_price,
            case when buy_rank = 1 then max_qty end as buy_qty,
            case when buy_rank = 1 then (max_qty * price) end as buy_value,
        from potential_buys_{{ iteration }}
    ),

    simulate_hold_{{ iteration }} as (
        select
            {{ cols }},
            buy_ts,
            buy_price,
            buy_qty,
            buy_value,
            last_value(buy_ts ignore nulls) over (
                partition by {{ partition_cols }} order by ts
            ) as last_buy_ts,
            last_value(buy_price ignore nulls) over (
                partition by {{ partition_cols }} order by ts
            ) as last_buy_price,
            last_value(buy_qty ignore nulls) over (
                partition by {{ partition_cols }} order by ts
            ) as last_buy_qty,
            last_value(buy_value ignore nulls) over (
                partition by {{ partition_cols }} order by ts
            ) as last_buy_value,
            (price * last_buy_qty) - last_buy_value as open_profit,
            ((price * last_buy_qty) - last_buy_value)
            / last_buy_value as open_profit_perc,
            case
                when
                    last_value(buy_ts ignore nulls) over (
                        partition by {{ partition_cols }} order by ts
                    )
                    is not null
                then price
            end as hold_price,
        from simulate_buy_{{ iteration }}
    ),

    simulate_trailstop_{{ iteration }} as (
        select
            {{ cols }},
            buy_ts,
            buy_price,
            buy_qty,
            buy_value,
            last_buy_ts,
            last_buy_price,
            last_buy_qty,
            last_buy_value,
            open_profit,
            open_profit_perc,
            hold_price,
            max(hold_price) over (
                partition by {{ partition_cols }}
                order by ts
                rows between unbounded preceding and current row
            ) as max_price,
        from simulate_hold_{{ iteration }}
    ),

    simulate_sell_{{ iteration }} as (
        select
            {{ cols }},
            buy_ts,
            buy_price,
            buy_qty,
            buy_value,
            last_buy_ts,
            last_buy_price,
            last_buy_qty,
            last_buy_value,
            open_profit,
            open_profit_perc,
            hold_price,
            max_price,
            hold_price / max_price - 1 as trail_perc,
            case
                when
                    (
                        {{ var("sell_conditions") }}
                        or trail_perc < {{ var("trailstop") }}
                        or open_profit_perc > {{ var("target_profit") }}
                        or minutes_since_open >= {{ var("sell_by_minutes") }}
                    )
                    and last_buy_qty > 0
                then true
                else false
            end as sell_decision,
            case when sell_decision then price end as sell_price,
            case when sell_decision then last_buy_qty end as sell_qty,
            case
                when sell_decision then (sell_price * sell_qty)
            end as sell_value,
            case when sell_decision then open_profit end as sell_profit,
            case when sell_decision then ts end as sell_ts,
        from simulate_trailstop_{{ iteration }}
    ),

    {{ output_cte_name }}_{{ iteration }} as (
        select
            {{ cols }},
            buy_ts,
            buy_price,
            buy_qty,
            buy_value,
            last_buy_ts,
            last_buy_price,
            last_buy_qty,
            last_buy_value,
            open_profit,
            open_profit_perc,
            hold_price,
            max_price,
            sell_price,
            sell_qty,
            sell_value,
            sell_profit,
            sell_ts,
            first_value(sell_ts ignore nulls) over (
                partition by {{ partition_cols }} order by ts
            ) as first_sell_ts,
        from simulate_sell_{{ iteration }}
    ),

    {% if iteration < max_iterations %}
        {% set model_name = output_cte_name + '_' + iteration|string %}
        {% set iteration = iteration + 1 %}
        {{ get_simulated_trades(model=model_name, iteration=iteration) }}
    {% endif %}
{% endmacro %}
