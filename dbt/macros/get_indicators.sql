{% macro get_smas(smas=var("smas")) %}
    {% for window in smas %}
        round(
            avg(close) over (
                partition by symbol
                order by ts rows between {{ window }} preceding and current row
            ),
            2
        )::double as sma{{ window }},
    {% endfor %}
{% endmacro %}
