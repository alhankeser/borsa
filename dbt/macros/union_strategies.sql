{% macro union_strategies(strategies=["test1", "test2"]) %}
    (
    {% for strategy in strategies %}
        {% set model = ref(strategy) %}
        select
            symbol,
            ts,
            id,
            side,
        from {{ model }}
    {% if not loop.last %}
        union all
    {% endif %}
    {% endfor %}
    ) unioned_strategies
{% endmacro %}