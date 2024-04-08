import subprocess


class Backtest:

    def __init__(self, db) -> None:
        self.db = db

    def run(self):
        # @TODO: pass strategies to this and set as var
        self.db.close()
        subprocess.call(["dbt", "run", "--target", "dev"])
        self.db.restart()

    
