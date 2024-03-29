{% macro get_continuation_lags(bars_ago=var("bars_ago"), smas=var("smas")) %}
    {% for window in smas %}
        {% for i in bars_ago %}
            {% for j in bars_ago %}
                lag(sma{{ window }}cntup{{ i }}, {{ j }}) over (
                    partition by symbol order by timestamp
                ) as sma{{ window }}cntup{{ i }}lag{{ j }},
                lag(sma{{ window }}cntdwn{{ i }}, {{ j }}) over (
                    partition by symbol order by timestamp
                ) as sma{{ window }}cntdwn{{ i }}lag{{ j }},
            {% endfor %}
        {% endfor %}
    {% endfor %}
{% endmacro %}
