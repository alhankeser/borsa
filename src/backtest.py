import subprocess


class Backtest:

    def __init__(self, db) -> None:
        self.db = db

    def run(self, refresh=False):
        self.db.close()
        if refresh:
            subprocess.call(["dbt", "run", "-m", "int__strategies+"])
        else:
            subprocess.call(["dbt", "run"])
        self.db.restart()
