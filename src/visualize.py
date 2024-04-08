import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Visualize:

    def __init__(self, db) -> None:
        self.db = db

    def day(self, ts_day):
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
            and minutes_since_open <= 120
            """
        ).df()
        melted = pd.melt(
            df,
            id_vars=["symbol", "ts", "minutes_since_open", "strategy_id"],
            value_vars=["price", "sma5", "sma10", "sma20", "sma40"],
        )
        sns.set_theme()
        sns.lineplot(melted, x="minutes_since_open", y="value", hue="variable")
        sns.scatterplot(df, x="minutes_since_open", y="buy_price", hue="strategy_id")
        plt.show()

    def profit(self, ts_days):
        df = self.db.query(
            f"""--sql
            select
                ts_day,
                strategy_id,
                profit_cumul
            from rpt__backtest
            where ts_day between '{ts_days[0]}' and '{ts_days[1]}'
            qualify row_number() over (partition by ts_day, strategy_id order by minutes_since_open desc) = 1
            """
        ).df()

        sns.set_theme()
        sns.lineplot(df, x="ts_day", y="profit_cumul", hue="strategy_id")
        plt.show()
