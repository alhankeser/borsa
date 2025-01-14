import os
import time
import duckdb
import subprocess
from dotenv import load_dotenv
load_dotenv()

import logging

logger = logging.getLogger("db")
logging.basicConfig(level=logging.INFO)


class Database:
    def __init__(self, env):
        self.env = env
        self.name = os.getenv("PROD_DATABASE") if self.env == "prod" else os.getenv("DEV_DATABASE")
        self.db_path = os.path.join(os.getenv("DATABASE_DIR"), self.name)
        self.reconnect()

    def _run_dbt_command(self, args):
        output = subprocess.run(["dbt", *args], capture_output=True)
        try:
            output.check_returncode()
        except Exception as err:
            logger.error(err)
            logger.error(output.stdout.decode('utf-8'))
            exit(1)
    
    def build(self, args=[]):
        self.con.close()
        self._run_dbt_command(["build"] + args)
        self.reconnect()

    def reconnect(self):
        self.con = duckdb.connect(self.db_path, read_only=True)

    def health_check(self):
        failed = False
        try:
            if self.sql("select 1").fetchone()[0] != 1:
                raise Exception            
        except Exception as err:
            failed = True
            logger.error(f"health check failed")
            logger.error(err)
        self.con.close()
        output = subprocess.run(["dbt", "debug"], capture_output=True)
        try:
            output.check_returncode()
        except Exception as err:
            failed = True
            logger.error(f"health check failed")
            logger.error(err)
            logger.error(output.stdout.decode('utf-8'))
        if not failed:
            logger.info("health ok")
            self.reconnect()

    def sql(self, query):
        return self.con.sql(query)
        
    def get_one(self, symbol, col, date=None):
        if date is None:
            return self.sql(f"""
                           select {col} from _indicators 
                           where symbol = '{symbol}'
                           order by ts desc
                           limit 1
                           """)
        else:
            return self.sql(f"""
                           select {col} from _indicators 
                           where symbol = '{symbol}' 
                           and ts = '{date}'
                           """)

    def export(self, table):
        self.sql(f"copy {table} to './storage/export/{table}.parquet' (format parquet)")
        return f"./storage/export/{table}.parquet"
