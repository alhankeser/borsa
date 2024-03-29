{% macro get_reversal(
            smas=var("smas"),
            bars_ago=var("bars_ago")) 
            %}
    {%- for window in smas -%}
        {%- for i in bars_ago -%}
            {%- for j in bars_ago -%}
                {% if i+1 <= bars_ago|max and j+1 <= bars_ago|max %}
                    (
                        sma{{ window }}cntup{{ i+1 }}lag{{ j }}
                        and sma{{ window }}cntdwn{{ j }}
                    ) as sma{{ window }}up{{ i+1 }}rvsdwn{{ j }}ago,
                    (
                        sma{{ window }}cntdwn{{ i+1 }}lag{{ j }}
                        and sma{{ window }}cntup{{ j }}
                    ) as sma{{ window }}dwn{{ i+1 }}rvsup{{ j }}ago,
                {%- endif -%}
            {%- endfor -%}
        {%- endfor -%}
    {%- endfor %}
{% endmacro %}
