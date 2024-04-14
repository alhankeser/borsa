import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Visualize:

    def __init__(self, db) -> None:
        self.db = db

    def _day(self, ts_day, strategy_id, symbol, ax):
        df = self.db.query(
            f"""--sql
            select distinct
                symbol,
                ts,
                minutes_since_open,
                price,
                sma5,
                sma10,
                sma20,
                sma40,
                buy_price,
                strategy_id,
            from rpt__backtest
            where ts_day = '{ts_day}'
            and strategy_id = '{strategy_id}'
            and symbol = '{symbol}'
            and minutes_since_open <= 120
            """
        ).df()
        melted = pd.melt(
            df,
            id_vars=["symbol", "ts", "minutes_since_open", "strategy_id"],
            value_vars=["price", "sma5", "sma10", "sma20", "sma40"],
        )
        sns.set_theme()
        sns.lineplot(melted, x="minutes_since_open", y="value", hue="variable", ax=ax)
        sns.scatterplot(df, x="minutes_since_open", y="buy_price", hue="strategy_id", ax=ax)

    def days(self, ts_days, strategy_id, symbol):
        fig, axes = plt.subplots(nrows=1, ncols=len(ts_days))
        for ax, ts_day in zip(axes, ts_days):
            self._day(ts_day, strategy_id, symbol, ax)
            ax.set_title(f"{symbol} {ts_day}")
        plt.show()

    def profit(self, ts_days, symbol):
        df = self.db.query(
            f"""--sql
            with profit_by_day_by_symbol as (
                select
                    ts_day,
                    strategy_id,
                    profit_cumul,
                    row_number() over (partition by ts_day, strategy_id, symbol order by minutes_since_open desc) as rk
                from rpt__backtest
                where ts_day between '{ts_days[0]}' and '{ts_days[1]}'
                    and symbol = '{symbol}'
            )
            select
                ts_day,
                strategy_id,
                sum(profit_cumul) as profit_cumul,
            from profit_by_day_by_symbol
            where rk = 1
            group by all
            """
        ).df()

        sns.set_theme()
        sns.lineplot(df, x="ts_day", y="profit_cumul", hue="strategy_id")
        plt.show()
    
    def profit_by_day(self, ts_days):
        df = self.db.query(
            f"""--sql
            select
                ts_day,
                strategy_id,
                profit,
                price_diff
            from rpt__backtest_by_day
            where ts_day between '{ts_days[0]}' and '{ts_days[1]}'
            """
        ).df()

        sns.set_theme()
        sns.scatterplot(df, x="ts_day", y="profit", hue="strategy_id")
        plt.show()



