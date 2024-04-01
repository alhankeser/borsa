{% macro union_strategies(strategies=var("strategies"), model=ref("int__indicators")) %}
    (
        {% for strategy in strategies %}
            select
                symbol,
                ts,
                '{{ strategy[' id '] }}' as strategy_id,
                {{ strategy['buy'] }} as buy,
            from {{ model }}
            {% if not loop.last %}
                union all
            {% endif %}
        {% endfor %}
    ) unioned_strategies
{% endmacro %}
