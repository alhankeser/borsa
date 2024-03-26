import os
import duckdb
from dotenv import load_dotenv
load_dotenv()


class Database:
    def __init__(self):
        self.con = duckdb.connect(os.path.join(os.getenv("DATABASE_DIR"), os.getenv("DEV_DATABASE")))

    def query(self, query):
        pass

    def get_row(self, symbol, col, date=None):
        if date is None:
            return self.con.query(f"""
                           select {col} from stocks 
                           where Symbol = '{symbol}'
                           order by TimeStamp desc
                           limit 1
                           """).fetchone()[0]
        else:
            return self.con.query(f"""
                           select {col} from stocks 
                           where Symbol = '{symbol}' 
                           and TimeStamp = '{date}'
                           """).fetchone()[0]