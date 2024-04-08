{% macro get_sma_columns(smas=var("smas"), model=ref("int__indicators")) %}
    {% for window in smas %}
       {{ model }}.sma{{ window }},
    {% endfor %}
{% endmacro %}