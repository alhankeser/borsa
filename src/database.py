import os
import duckdb
from dotenv import load_dotenv
load_dotenv()


class Database:
    def __init__(self, env):
        self.env = env
        self.name = os.getenv("PROD_DATABASE") if self.env == "prod" else os.getenv("DEV_DATABASE")
        self.con = duckdb.connect(os.path.join(os.getenv("DATABASE_DIR"), self.name), read_only=True)

    def query(self, query):
        return self.con.query(query)

    def get_one(self, symbol, col, date=None):
        if date is None:
            return self.con.query(f"""
                           select {col} from _indicators 
                           where symbol = '{symbol}'
                           order by ts desc
                           limit 1
                           """)
        else:
            return self.con.query(f"""
                           select {col} from _indicators 
                           where symbol = '{symbol}' 
                           and ts = '{date}'
                           """)