{% macro get_crosses(bars_ago=var("bars_ago"), smas=var("smas")) %}
    {% for bars in bars_ago %}
        {% for window1 in smas %}
            {% for window2 in smas %}
                {% if window1 != window2 and bars + 1 < bars_ago|max %}
                    (
                        sma{{ window1 }}lag{{ bars + 1 }}
                        <  sma{{ window2 }}lag{{ bars + 1 }}
                        and
                        sma{{ window1 }}lag{{ bars }}
                        >  sma{{ window2 }}lag{{ bars }}
                    ) as sma{{ window1 }}xsma{{ window2 }}lag{{ bars }},
                {% endif %}
            {% endfor %}    
        {% endfor %}
    {% endfor %}
{% endmacro %}
