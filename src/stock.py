import os
import re
from datetime import datetime, timedelta
import pandas as pd
from database import Database
from utils import get_minute, get_day, as_datetime
from dotenv import load_dotenv
load_dotenv()


class Stock:
    def __init__(self, symbol, api, db) -> None:
        self.symbol = symbol
        self.api = api
        self.env = api.env
        self.db = db
        self.storage_subdir = "stocks"
        self.storage_path = os.path.join(
            os.getenv("STORAGE_DIR"), self.env, self.storage_subdir, self.symbol
        )
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def _save_to_db(self, data, filename=None):
        df = pd.DataFrame(data)
        min_date = df.head(1)["TimeStamp"].values[0]
        if not filename:
            max_date = df.tail(1)["TimeStamp"].values[0]
            filename = (
                re.sub(r"[:\-]", "_", min_date[:-1])
                + "__"
                + re.sub(r"[:\-]", "_", max_date[:-1])
                + ".parquet"
            )
        df["Symbol"] = self.symbol
        df.to_parquet(
            os.path.join(self.storage_path, filename),
            index=False,
            compression="snappy",
        )
        return min_date

    def reset_history(self, start_date, end_date):
        min_date = end_date
        while min_date > start_date:
            args = {
                "symbol": self.symbol,
                "interval": 1,
                "unit": "Minute",
                "barsback": self.api.config.max_bars,
                "end_date": min_date,
            }
            data = self.api.get_symbol_data(args)
            min_date = self._save_to_db(data)

    def get_latest(self, start_date=None, end_date=None):
        if not start_date:
            start_date = get_day
        
        args = {
            "symbol": self.symbol,
            "interval": 1,
            "unit": "Minute",
            "start_date": start_date,
        }
        if end_date:
            # Make end_date inclusive of this end_date minute
            args["end_date"] = (as_datetime(end_date) + timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:00Z")
        data = self.api.get_symbol_data(args)
        self._save_to_db(data, "latest.parquet")

    def price(self, date=None):
        return self.db.get_one(self.symbol, 'price', date)
