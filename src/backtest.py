import subprocess


class Backtest:

    def __init__(self, db) -> None:
        self.db = db

    def run(self):
        self.db.close()
        subprocess.call(["dbt", "run", "-m", "int__strategies+", "--target", "dev"])
        self.db.restart()

    
