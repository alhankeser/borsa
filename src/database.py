import os
import duckdb
import subprocess
from dotenv import load_dotenv
load_dotenv()


class Database:
    def __init__(self, env):
        self.env = env
        self.name = os.getenv("PROD_DATABASE") if self.env == "prod" else os.getenv("DEV_DATABASE")
        self.db_path = os.path.join(os.getenv("DATABASE_DIR"), self.name)
        self.con = duckdb.connect(self.db_path, read_only=True)
    
    def restart(self):
        self.con = duckdb.connect(self.db_path, read_only=True)

    def close(self):
        self.con.close()

    def query(self, query):
        return self.con.query(query)

    def get_one(self, symbol, col, date=None):
        if date is None:
            return self.query(f"""
                           select {col} from _indicators 
                           where symbol = '{symbol}'
                           order by ts desc
                           limit 1
                           """)
        else:
            return self.query(f"""
                           select {col} from _indicators 
                           where symbol = '{symbol}' 
                           and ts = '{date}'
                           """)

    def export(self, table):
        self.query(f"copy {table} to './storage/export/{table}.parquet' (format parquet)")
        return f"./storage/export/{table}.parquet"
