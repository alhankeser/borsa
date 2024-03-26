select *
from {{ source("local", "stocks") }}