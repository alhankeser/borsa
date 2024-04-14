class Analyze:

    def __init__(self, db) -> None:
        self.db = db

    def _get_days(self, n, order):
        return self.db.query(
            f"""--sql
            select *
            from rpt__backtest_by_day
            qualify row_number() over 
                (partition by strategy_id 
                order by {order}) <= {n}
            """
        )

    def get_best_days(self, n=10):
        return self._get_days(n, "profit desc")
    
    def get_worst_days(self, n=10):
        return self._get_days(n, "profit asc")
