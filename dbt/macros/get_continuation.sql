{% macro get_continuation(
            smas=var("smas"),
            bars_ago=var("bars_ago")) 
            %}
    {% for window in smas %}
        {% for i in bars_ago %}
            (
                sma{{ window }} > sma{{ window }}lag{{ bars_ago|min }}
                {%- for j in range(0, i+2) %}
                    {%- if j-1 > 0 and j <= i %}
                        and sma{{ window }}lag{{ j-1 }} > sma{{ window }}lag{{ j }}
                    {%- endif %}
                    {%- set j = j-1 %}
                {%- endfor %}
            )::boolean as sma{{ window }}cntup{{ i }},
        {% endfor %}
        {% for i in bars_ago %}
            (
                sma{{ window }} < sma{{ window }}lag{{ bars_ago|min }}
                {%- for j in range(0, i+2) %}
                    {%- if j-1 > 0 and j <= i %}
                        and sma{{ window }}lag{{ j-1 }} < sma{{ window }}lag{{ j }}
                    {%- endif %}
                    {%- set j = j-1 %}
                {%- endfor %}
            )::boolean as sma{{ window }}cntdwn{{ i }},
        {% endfor %}
    {%- endfor %}
{% endmacro %}
