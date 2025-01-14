import os
import re
from datetime import datetime, timedelta, timezone
import pandas as pd
from database import Database
import utils
from dotenv import load_dotenv
import pytz
load_dotenv()


class Stock:
    def __init__(self, symbol, api, db) -> None:
        self.symbol = symbol
        self.api = api
        self.env = api.env
        self.db = db
        self.storage_subdir = "stocks"
        self.storage_path = self.get_storage_path()

    def get_storage_path(self):
        storage_path = os.path.join(
            os.getenv("STORAGE_DIR", ""),
            self.env,
            self.storage_subdir
        )
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
        return storage_path

    def _save_as_parquet(self, data, filename=None):
        df = pd.DataFrame(data)
        df["_extracted_at"] = datetime.now()
        filename = f"{self.symbol}.parquet"
        df.to_parquet(
            os.path.join(self.storage_path, filename),
            index=False,
            compression="snappy",
        )

    def get_history(self, start_date, end_date):
        start_date_unix = utils.as_unix(utils.as_date(start_date))
        end_date_unix = utils.as_unix(utils.as_date(end_date))
        args = {
            "symbol": self.symbol,
            "period": 10,
            "period_type": "year",
            "frequency": "daily",
            "start_date_unix": start_date_unix,
            "end_date_unix": end_date_unix,
        }
        res = self.api.get_symbol_data(args)
        data = res.json()
        self._save_as_parquet(data)

    def price(self, date=None):
        return self.db.get_one(self.symbol, 'price', date)
