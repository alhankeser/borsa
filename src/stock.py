import os
import re
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class Stock:
    def __init__(self, symbol, api, db) -> None:
        self.symbol = symbol
        self.api = api
        self.db = db
        self.storage_subdir = "stocks"
        self.storage_path = os.path.join(
            os.getenv("STORAGE_DIR"), self.storage_subdir, self.symbol
        )
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

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
            bars = self.api.get_symbol_data(args)
            df = pd.DataFrame(bars)
            min_date = df.head(1)["TimeStamp"].values[0]
            max_date = df.tail(1)["TimeStamp"].values[0]
            filename = (
                re.sub(r"[:\-]", "_", min_date[:-1])
                + "__"
                + re.sub(r"[:\-]", "_", max_date[:-1])
                + ".parquet"
            )
            df.to_parquet(
                os.path.join(self.storage_path, filename),
                index=False,
                compression="snappy",
            )

    def get_recent_history(self):
        pass

    def get_history_before(self, start_date, end_date):
        pass

    def close(self, date):
        pass
