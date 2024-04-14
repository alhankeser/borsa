## Trading Bot
A personal day-trading bot that relies on dbt and DuckDB for data transformations.

[Learn more](https://alhan.co/g/trading-bot-dbt-duckdb)

### Why

I'm publicly rewriting my day trading bot because: 
- **Improve maintainability:** the current codebase is hot garbage because of all of the changes I made on top of the original design without making incremental improvements to the design.
- **It's worth it:** my super-basic strategies work much better than expected (yes, trading bots _can_ make money), so it's worth making a more maintainable version of it.
- **Performance:** back-testing is super slow. I think it's due to the over-reliance on non-vectorized operations and lots of for-loops.
- **Shiny new toys:** I'm going to use this as an opportunity to try out dbt and DuckDB together to see if the combo is suitable in this context. I've seen it work well at my last job where we used DuckDB to transform fresh data on-the-fly for use in ML Models. 
