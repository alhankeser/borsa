{% macro union_trades(cte_name="trades", iterations=var("max_buys_per_day")) %}
    (
        {% for i in range(iterations) %}
            select *
            from {{ cte_name }}_{{ i }}
            where ts <= first_sell_ts
            {% if not loop.last %}
                union all
            {% endif %}
        {% endfor %}
    )
{% endmacro %}
