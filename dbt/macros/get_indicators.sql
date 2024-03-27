{% macro get_indicators(smas=var("smas")) %} 
    {% for window in smas %} 
    round(
        avg(close) over (
            partition by symbol
            order by
                timestamp rows between {{ window }} preceding
                and current row
    ), 2)::double as sma{{ window }},
    {% endfor %} 
{% endmacro %}