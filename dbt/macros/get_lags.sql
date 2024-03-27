{% macro get_lags(bars_ago=var("bars_ago"), smas=var("smas")) %} 
    {% for window in smas %} 
        {% for bars in bars_ago %}
            lag(sma{{ window }}, {{ bars }}) over (partition by symbol order by timestamp) as sma{{ window }}lag{{ bars }},
        {% endfor %}
    {% endfor %} 
{% endmacro %}